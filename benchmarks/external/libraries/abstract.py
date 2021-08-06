from abc import ABC, abstractmethod


class AbstractBackend(ABC):

    @abstractmethod
    def from_qasm(self, qasm):
        raise NotImplementedError

    @abstractmethod
    def __call__(self, circuit):
        raise NotImplementedError

    def transpose_state(self, x):
        return x


class ParserBackend(AbstractBackend):

    QASM_GATES = {"h": "H", "x": "X", "y": "Y", "z": "Z",
                  "rx": "RX", "ry": "RY", "rz": "RZ",
                  "u1": "U1", "u2": "U2", "u3": "U3",
                  "cx": "CNOT", "swap": "SWAP", "cz": "CZ",
                  "crx": "CRX", "cry": "CRY", "crz": "CRZ",
                  "cu1": "CU1", "cu3": "CU3",
                  "ccx": "TOFFOLI", "id": "I"}
    PARAMETRIZED_GATES = {"rx", "ry", "rz", "u1", "u2", "u3",
                          "crx", "cry", "crz", "cu1", "cu3"}

    def parse(self, qasm_code):
        """Extracts circuit information from QASM script.

        Args:
            qasm_code: String with the QASM code to parse.

        Returns:
            nqubits: The total number of qubits in the circuit.
            gate_list: List that specifies the gates of the circuit.
                Contains tuples of the form
                (Qibo gate name, qubit IDs, optional additional parameter).
                The additional parameter is the ``register_name`` for
                measurement gates or ``theta`` for parametrized gates.
        """
        import re
        def read_args(args):
            _args = iter(re.split(r"[\[\],]", args))
            for name in _args:
                if name:
                    index = next(_args)
                    if not index.isdigit():
                        raise_error(ValueError, "Invalid QASM qubit arguments:", args)
                    yield name, int(index)

        # Remove comment lines
        lines = "".join(line for line in qasm_code.split("\n")
                        if line and line[:2] != "//")
        lines = (line for line in lines.split(";") if line)

        if next(lines) != "OPENQASM 2.0":
            raise_error(ValueError, "QASM code should start with 'OPENQASM 2.0'.")

        qubits = {} # Dict[Tuple[str, int], int]: map from qubit tuple to qubit id
        cregs_size = {} # Dict[str, int]: map from `creg` name to its size
        registers = {} # Dict[str, List[int]]: map from register names to target qubit ids
        gate_list = [] # List[Tuple[str, List[int]]]: List of (gate name, list of target qubit ids)
        for line in lines:
            command, args = line.split(None, 1)
            # remove spaces
            command = command.replace(" ", "")
            args = args.replace(" ", "")

            if command == "include":
                pass

            elif command == "qreg":
                for name, nqubits in read_args(args):
                    for i in range(nqubits):
                        qubits[(name, i)] = len(qubits)

            elif command == "creg":
                for name, nqubits in read_args(args):
                    cregs_size[name] = nqubits

            elif command == "measure":
                args = args.split("->")
                if len(args) != 2:
                    raise_error(ValueError, "Invalid QASM measurement:", line)
                qubit = next(read_args(args[0]))
                if qubit not in qubits:
                    raise_error(ValueError, "Qubit {} is not defined in QASM code."
                                            "".format(qubit))

                register, idx = next(read_args(args[1]))
                if register not in cregs_size:
                    raise_error(ValueError, "Classical register name {} is not defined "
                                            "in QASM code.".format(register))
                if idx >= cregs_size[register]:
                    raise_error(ValueError, "Cannot access index {} of register {} "
                                            "with {} qubits."
                                            "".format(idx, register, cregs_size[register]))
                if register in registers:
                    if idx in registers[register]:
                        raise_error(KeyError, "Key {} of register {} has already "
                                              "been used.".format(idx, register))
                    registers[register][idx] = qubits[qubit]
                else:
                    registers[register] = {idx: qubits[qubit]}
                    gate_list.append(("M", register))

            else:
                pieces = [x for x in re.split("[()]", command) if x]
                if len(pieces) == 1:
                    gatename, params = pieces[0], None
                    if gatename not in self.QASM_GATES:
                        raise_error(ValueError, "QASM command {} is not recognized."
                                                "".format(command))
                    if gatename in self.PARAMETRIZED_GATES:
                        raise_error(ValueError, "Missing parameters for QASM "
                                                "gate {}.".format(gatename))

                elif len(pieces) == 2:
                    gatename, params = pieces
                    if gatename not in self.PARAMETRIZED_GATES:
                        raise_error(ValueError, "Invalid QASM command {}."
                                                "".format(command))
                    params = params.replace(" ", "").split(",")
                    try:
                        for i, p in enumerate(params):
                            if 'pi' in p:
                                import math
                                from operator import mul
                                from functools import reduce
                                s = p.replace('pi', str(math.pi)).split('*')
                                p = reduce(mul, [float(j) for j in s], 1)
                            params[i] = float(p)
                    except ValueError:
                        raise_error(ValueError, "Invalid value {} for gate parameters."
                                                "".format(params))

                else:
                    raise_error(ValueError, "QASM command {} is not recognized."
                                            "".format(command))

                # Add gate to gate list
                qubit_list = []
                for qubit in read_args(args):
                    if qubit not in qubits:
                        raise_error(ValueError, "Qubit {} is not defined in QASM "
                                                "code.".format(qubit))
                    qubit_list.append(qubits[qubit])
                if params is not None:
                    qubit_list.extend(params)
                gate_list.append((self.QASM_GATES[gatename], list(qubit_list)))
        return len(qubits), gate_list
