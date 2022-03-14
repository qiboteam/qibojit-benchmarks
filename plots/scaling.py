"""Generates qubit scaling plots for different qibo backends."""
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Patch
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['font.family'] = 'STIXGeneral'


def plot_scaling(cpu_data, gpu_data, circuit, quantity, precision="double", fontsize=30, legend=True, save=False):
    matplotlib.rcParams["font.size"] = fontsize
    # Prepare GPU data
    condition = (gpu_data["circuit"] == circuit) & (gpu_data["precision"] == precision)
    backends = ["tensorflow", "qibotf"]
    data = {f"{k} GPU": gpu_data[(gpu_data["library_options"] == f"backend={k}") & condition] for k in backends}
    data["qibojit cupy GPU"] = gpu_data[(gpu_data["library_options"] == "backend=qibojit,platform=cupy") & condition]
    data["qibojit cuquantum GPU"] = gpu_data[(gpu_data["library_options"] == "backend=qibojit,platform=cuquantum") & condition]

    # Prepare CPU data
    backends = ["numpy", "tensorflow", "qibotf", "qibojit"]
    condition = (cpu_data["circuit"] == circuit) & (cpu_data["precision"] == precision)
    data.update({k: cpu_data[(cpu_data["library_options"] == f"backend={k}") & condition] for k in backends})

    # Plot data
    cpu_cp = sns.color_palette("Oranges", 4)
    gpu_cp = sns.color_palette("Purples", 4)
    plt.figure(figsize=(16, 9))
    plt.semilogy(data["numpy"]["nqubits"], data["numpy"][quantity], marker="s", markersize=10,
                 color=cpu_cp[0], linewidth=3.0, label="numpy")
    plt.semilogy(data["tensorflow"]["nqubits"], data["tensorflow"][quantity], marker="o", markersize=10,
                 color=cpu_cp[1], linewidth=3.0, label="tensorflow cpu")
    plt.semilogy(data["qibotf"]["nqubits"], data["qibotf"][quantity], marker="D", markersize=10,
                 color=cpu_cp[2], linewidth=3.0, label="qibotf cpu")
    plt.semilogy(data["qibojit"]["nqubits"], data["qibojit"][quantity],
                 color=cpu_cp[3], linewidth=3.0, label="qibojit (numba) cpu", marker="^", markersize=10)
    plt.semilogy(data["tensorflow GPU"]["nqubits"], data["tensorflow GPU"][quantity], marker="o", markersize=10,
                 color=gpu_cp[1], linewidth=3.0, label="tensorflow gpu")
    plt.semilogy(data["qibotf GPU"]["nqubits"], data["qibotf GPU"][quantity], marker="D", markersize=10,
                 color=gpu_cp[2], linewidth=3.0, label="qibotf gpu")
    plt.semilogy(data["qibojit cupy GPU"]["nqubits"], data["qibojit cupy GPU"][quantity],
                 color=gpu_cp[3], linewidth=3.0, label="qibojit (cupy) gpu", marker="^", markersize=10)
    plt.semilogy(data["qibojit cuquantum GPU"]["nqubits"], data["qibojit cuquantum GPU"][quantity],
                 color=gpu_cp[3], linewidth=3.0, linestyle="--", label="qibojit (cuquantum) gpu", marker="v", markersize=10)

    plt.title(f"{circuit}, {precision} precision")
    plt.xlabel("Number of qubits")
    if quantity == "total_dry_time":
        plt.ylabel("Total dry run time (sec)")
    elif quantity == "total_simulation_time":
        plt.ylabel("Total simulation time (sec)")
    if legend:
        plt.legend(fontsize="small")
    if save:
        plt.savefig(f"qibo_scaling_{circuit}_{quantity}_{precision}.pdf", bbox_inches="tight")
    else:
        plt.show()
