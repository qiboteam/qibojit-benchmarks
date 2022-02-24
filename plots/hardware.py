"""Scaling plots with performance comparison of qibojit backend run on different CPU and GPU devices."""
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['font.family'] = 'STIXGeneral'


def plot_hardware(data, circuit, quantity, precision="double", fontsize=30, legend=False, save=False):
    matplotlib.rcParams["font.size"] = fontsize
    # Filter data
    data = {k: d[(d["circuit"] == circuit) & (d["precision"] == precision)]
            for k, d in data.items()}
        
    # Plot data
    oranges = sns.color_palette("Oranges", 2)
    blues = sns.color_palette("Blues", 3)

    colors = {
        "NVIDIA RTX A6000": blues[2],
        "NVIDIA DGX V100": blues[1],
        "NVIDIA GTX 1650": blues[0],
        "AMD EPYC 7742": oranges[1]
    }
    markers = {
        "NVIDIA RTX A6000": "^",
        "NVIDIA DGX V100": "s",
        "NVIDIA GTX 1650": "v",
        "AMD EPYC 7742": "o"
    }

    plt.figure(figsize=(14, 8))
    for k, d in data.items():
        plt.semilogy(d["nqubits"], d[quantity], color=colors[k], linewidth=3.0, 
                    marker=markers[k], markersize=10, label=k)

    plt.title(f"qibojit, {circuit}, {precision} precision")
    plt.xlabel("Number of qubits")
    if quantity == "total_dry_time":
        plt.ylabel("Total dry run time (sec)")
    elif quantity == "total_simulation_time":
        plt.ylabel("Total simulation time (sec)")

    if legend:
        plt.legend(loc="upper left")
    if save:
        plt.savefig(f"devices_{circuit}_{quantity}_{precision}.pdf", bbox_inches="tight")
    else:
        plt.show()