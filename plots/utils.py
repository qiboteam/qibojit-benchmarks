import json
import pandas as pd


def load_data(filename, qibojit_only=False):
    with open(filename, "r") as file:
        data = pd.DataFrame(json.load(file))

    # filter data for qibojit
    if qibojit_only:
        is_qibojit = data["library_options"].apply(lambda x: "qibojit" in x)
        data = data[is_qibojit]

    data["total_dry_time"]        = data["dry_run_time"]          + data["creation_time"] + data["import_time"]
    data["total_simulation_time"] = data["simulation_times_mean"] + data["creation_time"] + data["import_time"]
    return data