def parse(options):
    kwargs = {}
    if options is not None:
        for parameter in options.split(","):
            if "=" in parameter:
                k, v = parameter.split("=")
                kwargs[k] = v
            else:
                raise ValueError(f"Cannot parse parameter {parameter}.")
    return kwargs


def get(circuit_name, nqubits, options=None, qibo=False):
    if qibo:
        from benchmarks.circuits import qibo as module
    else:
        from benchmarks.circuits import qasm as module

    if circuit_name == "qft" or circuit_name == "QFT":
        circuit = module.QFT
    elif circuit_name == "one-qubit-gate":
        circuit = module.OneQubitGate
    elif circuit_name == "two-qubit-gate":
        circuit = module.TwoQubitGate
    elif circuit_name == "variational" or circuit_name == "variational-circuit":
        circuit = module.VariationalCircuit
    elif circuit_name == "bernstein-vazirani" or circuit_name == "bv":
        circuit = module.BernsteinVazirani
    elif circuit_name == "hidden-shift" or circuit_name == "hs":
        circuit = module.HiddenShift
    elif circuit_name == "qaoa":
        circuit = module.QAOA
    elif circuit_name == "supremacy":
        circuit = module.SupremacyCircuit
    elif circuit_name == "basis-change" or circuit_name == "bc":
        circuit = module.BasisChange
    elif circuit_name == "quantum-volume" or circuit_name == "qv":
        circuit = module.QuantumVolume
    else:
        raise NotImplementedError(f"Cannot find circuit {circuit_name}.")

    kwargs = parse(options)
    return circuit(nqubits, **kwargs)
