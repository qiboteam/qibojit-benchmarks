import os
import datetime
import logging
import json


class CustomHandler(logging.StreamHandler):
    """Custom handler for stdout logging."""

    def format(self, record):
        """Format the record with specific format."""
        fmt = f'[qibojit-benchmarks|%(levelname)s|%(asctime)s]: %(message)s'
        return logging.Formatter(fmt, datefmt='%Y-%m-%d %H:%M:%S').format(record)


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
log.addHandler(CustomHandler())


class JsonLogger(list):

    def __init__(self, filename=None, **kwargs):
        self.filename = filename
        if filename is not None:
            if os.path.isfile(filename):
                with open(filename, "r") as file:
                    super().__init__(json.load(file))
                log.info("Extending existing logs from {}.".format(filename))
            else:
                log.info("Creating new logs in {}.".format(filename))
                super().__init__()
        else:
            log.warning("Filename was not provided and logs will not be saved.")
            super().__init__()
        self.append(kwargs)
        now = datetime.datetime.now()
        self[-1]["datetime"] = now.strftime("%Y-%m-%d %H:%M:%S")

    def __getitem__(self, x):
        if isinstance(x, str):
            return self[-1].get(x)
        return super().__getitem__(x)

    def __str__(self):
        return "\n" + "\n".join(f"{k}: {v}" for k, v in self[-1].items())

    def dump(self):
        if self.filename is not None:
            with open(self.filename, "w") as file:
                json.dump(self, file)
