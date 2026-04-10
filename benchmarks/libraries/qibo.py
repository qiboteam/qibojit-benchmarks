from benchmarks.libraries import abstract
from benchmarks.logger import log


class Qibo(abstract.AbstractBackend):

    def __init__(
        self,
        max_qubits="0",
        backend="qibojit",
        platform=None,
        accelerators="",
        expectation=None,
        computation_settings=None,
    ):
        import qibo

        runcard = None

        if computation_settings is not None:
            import json

            try:
                with open(computation_settings, "r") as f:
                    runcard = json.load(f)

            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON in file '{computation_settings}': {e}")

            except FileNotFoundError:
                raise FileNotFoundError(f"File not found: {computation_settings}")

            if runcard["expectation_enabled"] == True:
                expectation = True

            qibo.set_backend(backend=backend, platform=platform, runcard=runcard)

            # For qibotn/quimb, apply TN simulation options from runcard when present.
            if backend == "qibotn" and platform == "quimb":
                quimb_backend = qibo.get_backend()
                use_mps = runcard.get("use_mps", runcard.get("MPS_enabled", True))
                max_bond_dimension = runcard.get(
                    "max_bond_dimension", runcard.get("max_bond", None)
                )
                svd_cutoff = runcard.get("svd_cutoff", 1e-10)
                mpi_enabled = runcard.get("MPI_enabled", False)
                quimb_backend.configure_tn_simulation(
                    ansatz="mps" if use_mps else None,
                    max_bond_dimension=max_bond_dimension if use_mps else None,
                    svd_cutoff=svd_cutoff,
                    MPI_enabled=mpi_enabled,
                )
        else:
            qibo.set_backend(backend=backend, platform=platform)

        from qibo import models

        self.name = "qibo"
        self.qibo = qibo
        self.models = models
        self.__version__ = qibo.__version__
        self.max_qubits = int(max_qubits)
        self.accelerators = self._parse_accelerators(accelerators)
        self.expectation_flag = expectation
        self.backend_name_str = backend
        self.platform_str = platform
        self.runcard = runcard

    def from_qasm(self, qasm):
        circuit = self.models.Circuit.from_qasm(qasm, accelerators=self.accelerators)
        if self.max_qubits > 1:
            if self.max_qubits > 2:
                log.warn(
                    "Fusion with {} qubits is not yet supported by Qibo. "
                    "Using max_qubits=2.".format(self.max_qubits)
                )
            circuit = circuit.fuse()
        return circuit

    """
    def __call__(self, circuit):
        # transfer final state to numpy array because that's what happens
        # for all backends
        return circuit().state(numpy=True)
    """

    def __call__(self, circuit):
        # transfer final state to numpy array because that's what happens
        # for all backends
        if self.backend_name_str == "qibojit" and self.expectation_flag is not None:
            from qibo.symbols import X, Y, Z, I
            from qibo.hamiltonians import SymbolicHamiltonian
            import numpy as np

            # from qibo.backends import GlobalBackend
            from qibo import construct_backend

            backend = construct_backend(self.backend_name_str)
            # self.expectation_flag must contain pauli string pattern for it to work
            list_of_objects = []
            gate_mapping = {"I": I, "X": X, "Y": Y, "Z": Z}

            for i in range(circuit.nqubits):
                gate = gate_mapping[
                    self.expectation_flag[i % len(self.expectation_flag)]
                ]
                list_of_objects.append(gate(i))
            obs = np.prod(list_of_objects)
            obs = SymbolicHamiltonian(obs, backend=backend)

            # Noise-free expected value
            return obs.expectation(circuit)
        else:
            if self.expectation_flag:
                if self.backend_name_str == "qibotn" and self.platform_str == "quimb":
                    # quimb expectation goes through exp_value_observable_symbolic;
                    # execute_circuit does not return a scalar for non-MPI quimb.
                    import numpy as np
                    nq = circuit.nqubits

                    # If pauli_pattern is set in the JSON config (e.g. "XIIII"),
                    # each non-I character becomes a single-site term with coeff 1.0.
                    # "X" on site i means X_i ⊗ I elsewhere.
                    pauli_pattern = (
                        self.runcard.get("pauli_pattern") if self.runcard else None
                    )
                    if pauli_pattern:
                        operators, sites, coeffs = [], [], []
                        for i, ch in enumerate(pauli_pattern.upper()):
                            if ch != "I" and i < nq:
                                operators.append(ch.lower())
                                sites.append((i,))
                                coeffs.append(1.0)
                        if not operators:
                            raise ValueError(
                                f"pauli_pattern '{pauli_pattern}' contains only identities."
                            )
                    else:
                        # Default observable mirrors test_mpi_quimb.py:
                        #   z@0, x@1, zz@(2,3), yy@(3,4), xyz@(0,1,2)
                        operators = ["z", "x"]
                        sites     = [(0,), (min(1, nq - 1),)]
                        coeffs    = [1.0, 0.5]
                        if nq >= 4:
                            operators += ["zz", "yy"]
                            sites     += [(min(2, nq - 2), min(3, nq - 1)),
                                          (min(3, nq - 2), min(4, nq - 1))]
                            coeffs    += [0.8, 0.3]
                        if nq >= 3:
                            operators += ["xyz"]
                            sites     += [(0, min(1, nq - 2), min(2, nq - 1))]
                            coeffs    += [0.2]

                    return np.real(
                        self.qibo.get_backend().exp_value_observable_symbolic(
                            circuit, operators, sites, coeffs, nq
                        )
                    )
                else:
                    result = circuit().real
                    return result.get() if hasattr(result, "get") else result
            else:
                if self.backend_name_str == "qibotn":
                    if self.platform_str == "quimb":
                        # quimb only populates statevector when return_array=True
                        result = self.qibo.get_backend().execute_circuit(
                            circuit, return_array=True
                        )
                        return result.statevector.flatten()
                    else:
                        return circuit().statevector.flatten()
                else:
                    return circuit().state(numpy=True)

    def transpose_state(self, x):
        return x

    def get_precision(self):
        return self.qibo.get_dtype()

    def set_precision(self, precision):
        self.qibo.set_dtype(precision)

    def get_device(self):
        return self.qibo.get_device()

    @staticmethod
    def _parse_accelerators(accelerators):
        """Transforms string that specifies accelerators to dictionary.

        The string that is parsed has the following format:
            n1device1+n2device2+n3device3,...
        and is transformed to the dictionary:
            {'device1': n1, 'device2': n2, 'device3': n3, ...}

        Example:
            2/GPU:0+2/GPU:1 --> {'/GPU:0': 2, '/GPU:1': 2}
        """
        if not accelerators or accelerators is None:
            return None

        def read_digit(x):
            i = 0
            while x[i].isdigit():
                i += 1
            return x[i:], int(x[:i])

        accelerator_dict = {}
        for entry in accelerators.split("+"):
            device, n = read_digit(entry)
            if device in accelerator_dict:
                accelerator_dict[device] += n
            else:
                accelerator_dict[device] = n
        return accelerator_dict
