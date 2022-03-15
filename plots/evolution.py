import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Patch
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['font.family'] = 'STIXGeneral'


def plot_dense(data, quantity, nqubits, fontsize=30, legend=True, save=False):
    matplotlib.rcParams["font.size"] = fontsize

    cpu_cp = sns.color_palette("Oranges", 4)
    gpu_cp = sns.color_palette("Purples", 4)

    data["is_gpu"] = data["device"].apply(lambda x: "GPU" in x)
    base_condition = (data["nqubits"] == nqubits) & (data["dense"] == True)

    plt.figure(figsize=(16, 9))    
    condition = base_condition & (data["backend"] == "numpy")
    plt.semilogy(data[condition]["dt"], data[condition][quantity], marker="^", markersize=10,
                 color=cpu_cp[3], linewidth=3.0, label="numpy")
    condition = base_condition & (data["backend"] == "tensorflow") & (data["is_gpu"] == False)
    plt.semilogy(data[condition]["dt"], data[condition][quantity], marker="o", markersize=10,
                 color=cpu_cp[1], linewidth=3.0, label="tensorflow cpu")

    condition = base_condition & (data["backend"] == "qibojit") & (data["platform"] == "cuquantum")
    plt.semilogy(data[condition]["dt"], data[condition][quantity], marker="^", markersize=10,
                     color=gpu_cp[3], linewidth=3.0, label="cupy")
    condition = base_condition & (data["backend"] == "tensorflow") & (data["is_gpu"] == True)
    plt.semilogy(data[condition]["dt"], data[condition][quantity], marker="o", markersize=10,
                     color=gpu_cp[1], linewidth=3.0, label="tensorflow gpu")

    plt.title(f"Dense adiabatic evolution, {nqubits} qubits, double precision")
    plt.xlabel("$\delta t$")
    if quantity == "total_dry_time":
        plt.ylabel("Total dry run time (sec)")
    elif quantity == "total_simulation_time":
        plt.ylabel("Total simulation time (sec)")

    if legend:
        plt.legend()

    if save:
        plt.savefig(f"evolution_dense_{nqubits}qubits_{quantity}.pdf", bbox_inches="tight")
    else:
        plt.show()


def plot_trotter(data, quantity, nqubits, fontsize=30, legend=False, save=False):
    matplotlib.rcParams["font.size"] = fontsize
    
    cpu_cp = sns.color_palette("Oranges", 4)
    gpu_cp = sns.color_palette("Purples", 4)
    
    data["is_gpu"] = data["device"].apply(lambda x: "GPU" in x)
    base_condition = (data["nqubits"] == nqubits) & (data["dense"] == False)

    plt.figure(figsize=(16, 9))
    condition = base_condition & (data["backend"] == "numpy")
    plt.semilogy(data[condition]["dt"], data[condition][quantity], marker="s", markersize=10,
                     color=cpu_cp[0], linewidth=3.0, label="numpy")
    condition = base_condition & (data["backend"] == "tensorflow") & (data["is_gpu"] == False)
    plt.semilogy(data[condition]["dt"], data[condition][quantity], marker="o", markersize=10,
                 color=cpu_cp[1], linewidth=3.0, label="tensorflow cpu")
    condition = base_condition & (data["backend"] == "qibotf") & (data["is_gpu"] == False)
    plt.semilogy(data[condition]["dt"], data[condition][quantity], marker="D", markersize=10,
                     color=cpu_cp[2], linewidth=3.0, label="qibotf cpu")
    condition = base_condition & (data["backend"] == "qibojit") & (data["platform"] == "numba")
    plt.semilogy(data[condition]["dt"], data[condition][quantity], marker="^", markersize=10,
                     color=cpu_cp[3], linewidth=3.0, label="qibojit (numba) cpu")

    condition = base_condition & (data["backend"] == "tensorflow") & (data["is_gpu"] == True)
    plt.semilogy(data[condition]["dt"], data[condition][quantity], marker="o", markersize=10,
                     color=gpu_cp[1], linewidth=3.0, label="tensorflow gpu")
    condition = base_condition & (data["backend"] == "qibotf") & (data["is_gpu"] == True)
    plt.semilogy(data[condition]["dt"], data[condition][quantity], marker="D", markersize=10,
                     color=gpu_cp[2], linewidth=3.0, label="qibotf gpu")
    condition = base_condition & (data["backend"] == "qibojit") & (data["platform"] == "cupy")
    plt.semilogy(data[condition]["dt"], data[condition][quantity], marker="^", markersize=10,
                     color=gpu_cp[3], linewidth=3.0, label="qibojit (cupy) gpu")
    condition = base_condition & (data["backend"] == "qibojit") & (data["platform"] == "cuquantum")
    plt.semilogy(data[condition]["dt"], data[condition][quantity], marker="v", markersize=10, linestyle="--",
                     color=gpu_cp[3], linewidth=3.0, label="qibojit (cuquantum) gpu")

    plt.title(f"Trotter adiabatic evolution, {nqubits} qubits, double precision")
    plt.xlabel("$\delta t$")
    if quantity == "total_dry_time":
        plt.ylabel("Total dry run time (sec)")
    elif quantity == "total_simulation_time":
        plt.ylabel("Total simulation time (sec)")

    if legend:
        plt.legend(fontsize="small")
    
    if save:
        plt.savefig(f"evolution_trotter_{nqubits}qubits_{quantity}.pdf", bbox_inches="tight")
    else:
        plt.show()
