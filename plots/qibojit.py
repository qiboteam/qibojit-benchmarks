"""Generates dry run vs simulation barplot for qibojit backend."""
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Patch
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['font.family'] = 'STIXGeneral'


def breakdown_barplot_nqubits(data, circuit, precision="double", width=0.1, fontsize=30, save=False):
    matplotlib.rcParams["font.size"] = fontsize

    # Set plot params
    hatches = ['/', '\\', 'o', '-', 'x', '.', '*']
    quantities = ["import_time", "creation_time", "dry_run_time", "simulation_times_mean",
                  "total_simulation_time", "total_dry_time"]
    
    nqubits = [18, 20, 22, 24, 26, 28]
    widths = [-5 * width / 2, - 3 * width / 2, -width / 2, width / 2, 3 * width / 2, 5 * width / 2]
    oranges = sns.color_palette("Oranges", 2)
    purples = sns.color_palette("Purples", 2)
    greens = sns.color_palette("Greens", 2)
    blues = sns.color_palette("Blues", 2)
    
    # Plot the results
    plt.figure(figsize=(25, 9))
    plt.title(f"qibojit - Dry run vs simulation - {circuit}")
    
    xvalues = np.array(range(len(nqubits)))
    plt.xticks(xvalues, nqubits)
    
    base_condition = ((data["precision"] == precision) & (data["circuit"] == circuit))
    condition = base_condition & (data["library_options"] == "backend=qibojit,platform=numba")
    heights_numba = {q: np.array([float(data[condition & (data["nqubits"] == n)][q]) for n in nqubits])
                     for q in quantities}
    condition = base_condition & (data["library_options"] == "backend=qibojit,platform=cupy")
    heights_cupy = {q: np.array([float(data[condition & (data["nqubits"] == n)][q]) for n in nqubits])
                    for q in quantities}
    condition = base_condition & (data["library_options"] == "backend=qibojit,platform=cuquantum")
    heights_cuquantum = {q: np.array([float(data[condition & (data["nqubits"] == n)][q]) for n in nqubits])
                         for q in quantities}
    
    plt.bar(xvalues + widths[0], heights_numba["import_time"],
            color=oranges[0], align="center", width=width, alpha=1, hatch=hatches[0],
            edgecolor='w')
    plt.bar(xvalues + widths[1], heights_numba["import_time"],
            color=oranges[1], align="center", width=width, alpha=1, hatch=hatches[1],
            edgecolor='w')
    
    plt.bar(xvalues + widths[2], heights_cupy["import_time"],
            color=oranges[0], align="center", width=width, alpha=1, hatch=hatches[0],
            edgecolor='w')
    plt.bar(xvalues + widths[3], heights_cupy["import_time"],
            color=oranges[1], align="center", width=width, alpha=1, hatch=hatches[1],
            edgecolor='w')
    
    plt.bar(xvalues + widths[4], heights_cuquantum["import_time"],
            color=oranges[0], align="center", width=width, alpha=1, hatch=hatches[0],
            edgecolor='w')
    plt.bar(xvalues + widths[5], heights_cuquantum["import_time"],
            color=oranges[1], align="center", width=width, alpha=1, hatch=hatches[1],
            edgecolor='w')
    
    plt.bar(xvalues + widths[0], heights_numba["total_dry_time"],
            color=blues[0], align="center", width=width, alpha=1, hatch=hatches[0],
            edgecolor='w', bottom=heights_numba["import_time"] + heights_numba["creation_time"])
    plt.bar(xvalues + widths[1], heights_numba["total_simulation_time"],
            color=blues[1], align="center", width=width, alpha=1, hatch=hatches[1],
            edgecolor='w', bottom=heights_numba["import_time"] + heights_numba["creation_time"])
    
    plt.bar(xvalues + widths[2], heights_cupy["total_dry_time"],
            color=purples[0], align="center", width=width, alpha=1, hatch=hatches[0],
            edgecolor='w', bottom=heights_cupy["import_time"] + heights_cupy["creation_time"])
    plt.bar(xvalues + widths[3], heights_cupy["total_simulation_time"],
            color=purples[1], align="center", width=width, alpha=1, hatch=hatches[1],
            edgecolor='w', bottom=heights_cupy["import_time"] + heights_cupy["creation_time"])
    
    plt.bar(xvalues + widths[4], heights_cuquantum["total_dry_time"],
            color=greens[0], align="center", width=width, alpha=1, hatch=hatches[0],
            edgecolor='w', bottom=heights_cuquantum["import_time"] + heights_cuquantum["creation_time"])
    plt.bar(xvalues + widths[5], heights_cuquantum["total_simulation_time"],
            color=greens[1], align="center", width=width, alpha=1, hatch=hatches[1],
            edgecolor='w', bottom=heights_cuquantum["import_time"] + heights_cuquantum["creation_time"])

    plt.xlabel("Number of qubits")
    plt.ylabel("Execution time (sec)")
    
    legend_elements = [
        Patch(facecolor="w", edgecolor="k", hatch=hatches[0], label="Dry run time"),
        Patch(facecolor="w", edgecolor="k", hatch=hatches[1], label="Simulation time"),
        Patch(color=oranges[1], label="Import time"),
        Patch(color=blues[1], label="numba"),
        Patch(color=purples[1], label="cupy"),
        Patch(color=greens[1], label="cuquantum"),
    ]
    plt.legend(handles=legend_elements)
    if save:
        plt.savefig(f"qibojit_dry_vs_simulation_{precision}_{circuit}.pdf", bbox_inches="tight")
    else:
        plt.show()


def breakdown_barplot_circuits(data, nqubits, precision="double", width=0.1, fontsize=30, save=False):
    matplotlib.rcParams["font.size"] = fontsize
    # Set plot params
    hatches = ['/', '\\', 'o', '-', 'x', '.', '*']
    width = 0.1
    quantities = ["import_time", "creation_time", "dry_run_time", "simulation_times_mean",
                  "total_simulation_time", "total_dry_time"]
    
    circuits = ["qft", "variational", "supremacy", "qv", "bv"]
    oranges = sns.color_palette("Oranges", 2)
    purples = sns.color_palette("Purples", 2)
    greens = sns.color_palette("Greens", 2)

    plt.figure(figsize=(25, 9))
    plt.title(f"qibojit - Dry run vs simulation - {nqubits} qubits")
    
    xvalues = np.array(range(len(circuits)))
    plt.xticks(xvalues, circuits)

    base_condition = ((data["precision"] == precision) & (data["nqubits"] == nqubits))    
    condition = base_condition & (data["library_options"] == "backend=qibojit,platform=cupy")
    heights_cupy = {q: np.array([float(data[condition & (data["circuit"] == circ)][q]) for circ in circuits])
                    for q in quantities}
    condition = base_condition & (data["library_options"] == "backend=qibojit,platform=cuquantum")
    heights_cuquantum = {q: np.array([float(data[condition & (data["circuit"] == circ)][q]) for circ in circuits])
                         for q in quantities}
    
    plt.bar(xvalues - 3 * width / 2, heights_cupy["import_time"],
            color=oranges[0], align="center", width=width, alpha=1, hatch=hatches[0],
            edgecolor='w')
    plt.bar(xvalues - width / 2, heights_cupy["import_time"],
            color=oranges[1], align="center", width=width, alpha=1, hatch=hatches[1],
            edgecolor='w')
    
    plt.bar(xvalues + width / 2, heights_cuquantum["import_time"],
            color=oranges[0], align="center", width=width, alpha=1, hatch=hatches[0],
            edgecolor='w')
    plt.bar(xvalues + 3 * width / 2, heights_cuquantum["import_time"],
            color=oranges[1], align="center", width=width, alpha=1, hatch=hatches[1],
            edgecolor='w')
    
    plt.bar(xvalues - 3 * width / 2, heights_cupy["total_dry_time"],
            color=purples[0], align="center", width=width, alpha=1, hatch=hatches[0],
            edgecolor='w', bottom=heights_cupy["import_time"] + heights_cupy["creation_time"])
    plt.bar(xvalues - width / 2, heights_cupy["total_simulation_time"],
            color=purples[1], align="center", width=width, alpha=1, hatch=hatches[1],
            edgecolor='w', bottom=heights_cupy["import_time"] + heights_cupy["creation_time"])
    
    plt.bar(xvalues + width / 2, heights_cuquantum["total_dry_time"],
            color=greens[0], align="center", width=width, alpha=1, hatch=hatches[0],
            edgecolor='w', bottom=heights_cuquantum["import_time"] + heights_cuquantum["creation_time"])
    plt.bar(xvalues + 3 * width / 2, heights_cuquantum["total_simulation_time"],
            color=greens[1], align="center", width=width, alpha=1, hatch=hatches[1],
            edgecolor='w', bottom=heights_cuquantum["import_time"] + heights_cuquantum["creation_time"])

    plt.ylabel("Execution time (sec)")
    
    legend_elements = [
        Patch(facecolor="w", edgecolor="k", hatch=hatches[0], label="Dry run time"),
        Patch(facecolor="w", edgecolor="k", hatch=hatches[1], label="Simulation time"),
        Patch(color=oranges[1], label="Import time"),
        Patch(color=purples[1], label="cupy"),
        Patch(color=greens[1], label="cuquantum"),
        
    ]
    plt.legend(handles=legend_elements, bbox_to_anchor=(1,1))
    
    if save:
        plt.savefig(f"qibojit_dry_vs_simulation_{precision}_{nqubits}qubits.pdf", bbox_inches="tight")
    else:
        plt.show()