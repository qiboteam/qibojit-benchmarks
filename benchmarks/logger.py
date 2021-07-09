import os
import time
import json


class JsonLogger(list):

    def __init__(self, filename=None):
        self.filename = filename
        if filename is not None:
            if os.path.isfile(filename):
                with open(filename, "r") as file:
                    super().__init__(json.load(file))
                print("Extending existing logs from {}.".format(filename))
                return
            else:
                print("Creating new logs in {}.".format(filename))
        super().__init__()

    def __getitem__(self, x):
        if isinstance(x, str):
            return self[-1].get(x)
        return super().__getitem__(x)

    def __str__(self):
        return "\n".join(f"{k}: {v}" for k, v in self[-1].items())

    def dump(self):
        if self.filename is not None:
            with open(self.filename, "w") as file:
                json.dump(self, file)
