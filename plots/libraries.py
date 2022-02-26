import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Patch
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['font.family'] = 'STIXGeneral'


class Library:
    """Defines color, hatch and label for each library."""

    def __init__(self, name, color, hatch, label, has_double=True, has_single=True, alpha=None):
        self.name = name
        self.color = color
        self.hatch = hatch
        self.label = label
        self.has_double = has_double
        self.has_single = has_single
        if alpha is None:
            self.alpha = 1.0 if "GPU" in self.name else 0.5
        else:
            self.alpha = alpha

    def has(self, precision):
        return getattr(self, f"has_{precision}")


def plot_libraries(libraries, cpu_data, gpu_data, quantity, nqubits, 
                   precision="double", width=0.07, fontsize=45, 
                   legend=False, save=False):
    matplotlib.rcParams["font.size"] = fontsize
    # Process data
    gpu_data = gpu_data.copy()
    gpu_data["library"] += " GPU"
    data = pd.concat([cpu_data, gpu_data])

    circuits = ["qft", "variational", "supremacy", "qv", "bv"]
    # create widths list for bar positioning
    n = len([library for library in libraries if library.has(precision)])
    ws = np.arange(n)
    ws = iter((ws - ws[n // 2]) * width)

    # Plot the results
    xvalues = np.array(range(len(circuits)))
    plt.figure(figsize=(25, 9))
    base_condition = (data["nqubits"] == nqubits) & (data["precision"] == precision)
    for library in libraries:
        if library.has(precision):
            condition = base_condition & (data["library"] == library.name)
            height = np.array([float(data[condition & (data["circuit"] == c)][quantity]) for c in circuits])
            plt.bar(xvalues + next(ws), height, color=library.color, align="center", 
                    width=width, alpha=library.alpha, label=library.label, 
                    log=True, edgecolor='w', hatch=library.hatch)

    plt.title(f"{nqubits} qubits - {precision} precision")
    if quantity == "total_dry_time":
        plt.ylabel("Total dry time (sec)")
    elif quantity == "total_simulation_time":
        plt.ylabel("Total simulation time (sec)")

    plt.xticks(xvalues, circuits)
    if legend:
        plt.legend(fontsize="small", bbox_to_anchor=(1,1))
    if save:
        plt.savefig(f"libraries_{precision}_{nqubits}qubits_{quantity}.pdf", bbox_inches="tight")
    else:
        plt.show()
