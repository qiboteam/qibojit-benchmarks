import json
import pandas as pd


def load_data(filename):
    with open(filename, "r") as file:
        data = pd.DataFrame(json.load(file))
    data["total_dry_time"]        = data["dry_run_time"]          + data["creation_time"] + data["import_time"]
    data["total_simulation_time"] = data["simulation_times_mean"] + data["creation_time"] + data["import_time"]
    return data