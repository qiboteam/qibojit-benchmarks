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


def load_data_multigpu(filename, qibojit_only=False):
    data = load_data(filename, qibojit_only)
    data["backend"] = data["library_options"].apply(lambda x: x.split(",")[0].split("=")[-1])
    data["accelerators"] = data["library_options"].apply(lambda x: x.split(",")[1].split("=")[-1])
    data["nqubits (accelerators)"] = data.apply(lambda x: f"{x.nqubits} ({x.accelerators})", axis=1)
    return data


def load_evolution_data(filename):
    with open(filename, "r") as file:
        data = pd.DataFrame(json.load(file))
    
    data["creation_time"] = data["hamiltonian_creation_time"] + data["evolution_creation_time"]
    data["total_dry_time"] = data["dry_run_time"] + data["creation_time"] + data["import_time"]
    #if "simulation_times_mean" not in data.columns:
    #    data["simulation_times_mean"] = data["simulation_times"].apply(lambda x: np.mean(x))
    data["total_simulation_time"] = data["simulation_times_mean"] + data["creation_time"] + data["import_time"]
    return data