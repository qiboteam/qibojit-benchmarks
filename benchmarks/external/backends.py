from abc import abstractmethod


class Qibo:

    def __init__(self):
        from qibo import models
        self.models = models

    def from_qasm(self, qasm):
        return self.models.Circuit.from_qasm(qasm)

    def __call__(self, circuit):
        return circuit()
