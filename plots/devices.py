"""Scaling plots with performance comparison of qibojit backend run on different CPU and GPU devices."""
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['font.family'] = 'STIXGeneral'


class Line:

    def __init__(self, label, data, color, marker):
        self.label = label
        self.data = data
        self.color = color
        self.marker = marker


def plot_devices(lines, circuit, quantity, precision="double", 
                 fontsize=30, legendfont=None, save=False):
    matplotlib.rcParams["font.size"] = fontsize
    # Filter data
    for line in lines:
        condition = (line.data["circuit"] == circuit) & (line.data["precision"] == precision)
        line.data = line.data[condition]

    plt.figure(figsize=(14, 8))
    for line in lines:
        plt.semilogy(line.data["nqubits"], line.data[quantity], color=line.color, 
                     linewidth=3.0, marker=line.marker, markersize=10, label=line.label)

    plt.title(f"qibojit, {circuit}, {precision} precision")
    plt.xlabel("Number of qubits")
    if quantity == "total_dry_time":
        plt.ylabel("Total dry run time (sec)")
    elif quantity == "total_simulation_time":
        plt.ylabel("Total simulation time (sec)")

    if legendfont is not None:
        plt.legend(loc="upper left", fontsize=legendfont)
    if save:
        plt.savefig(f"devices_{circuit}_{quantity}_{precision}.pdf", bbox_inches="tight")
    else:
        plt.show()