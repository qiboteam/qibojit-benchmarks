from abc import abstractmethod


class AbstractCircuit:

    def __init__(self, nqubits):
        self.nqubits = nqubits
        self.parameters = {}

    @abstractmethod
    def __iter__(self):
        raise NotImplementedError

    def to_qasm(self):
        code = ['OPENQASM 2.0;', 'include "qelib1.inc";',
                f'qreg q[{self.nqubits}];', f'creg m[{self.nqubits}];']
        code.extend(iter(self))
        return "\n".join(code)

    def __str__(self):
        return ", ".join(f"{k}={v}" for k, v in self.parameters.items())


class AbstractConstructor:

    circuit_map = {}

    def __new__(cls, circuit_name, nqubits, options=None):
        if circuit_name not in cls.circuit_map:
            raise NotImplementedError(f"Cannot find circuit {circuit_name}.")
        kwargs = cls.parse(options)
        return cls.circuit_map.get(circuit_name)(nqubits, **kwargs)

    @staticmethod
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
