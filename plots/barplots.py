"""Generates bar plots for qibojit breakdowns and multigpu comparisons."""
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Patch
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['font.family'] = 'STIXGeneral'


def plot_breakdown_nqubits(data, circuit, precision="double", width=0.1, fontsize=30, save=False):
    """Creates dry run vs simulation barplot with import time breakdown for given circuit varying the number of qubits."""
    matplotlib.rcParams["font.size"] = fontsize

    # Set plot params
    hatches = ['/', '\\', 'o', '-', 'x', '.', '*']
    quantities = ["import_time", "creation_time", "dry_run_time", "simulation_times_mean"]
    
    nqubits = [22, 24, 26, 28, 30]
    widths = [-5 * width / 2, - 3 * width / 2, -width / 2, width / 2, 3 * width / 2, 5 * width / 2]
    oranges = sns.color_palette("Oranges", 2)
    purples = sns.color_palette("Purples", 2)
    greens = sns.color_palette("Greens", 2)
    greys = sns.color_palette("Greys", 2)
    
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
            color=greys[0], align="center", width=width, alpha=1, hatch=hatches[0],
            edgecolor='w')
    plt.bar(xvalues + widths[1], heights_numba["import_time"],
            color=greys[1], align="center", width=width, alpha=1, hatch=hatches[1],
            edgecolor='w')
    
    plt.bar(xvalues + widths[2], heights_cupy["import_time"],
            color=greys[0], align="center", width=width, alpha=1, hatch=hatches[0],
            edgecolor='w')
    plt.bar(xvalues + widths[3], heights_cupy["import_time"],
            color=greys[1], align="center", width=width, alpha=1, hatch=hatches[1],
            edgecolor='w')
    
    plt.bar(xvalues + widths[4], heights_cuquantum["import_time"],
            color=greys[0], align="center", width=width, alpha=1, hatch=hatches[0],
            edgecolor='w')
    plt.bar(xvalues + widths[5], heights_cuquantum["import_time"],
            color=greys[1], align="center", width=width, alpha=1, hatch=hatches[1],
            edgecolor='w')
    
    plt.bar(xvalues + widths[0], heights_numba["dry_run_time"],
            color=oranges[0], align="center", width=width, alpha=1, hatch=hatches[0],
            edgecolor='w', bottom=heights_numba["import_time"] + heights_numba["creation_time"])
    plt.bar(xvalues + widths[1], heights_numba["simulation_times_mean"],
            color=oranges[1], align="center", width=width, alpha=1, hatch=hatches[1],
            edgecolor='w', bottom=heights_numba["import_time"] + heights_numba["creation_time"])
    
    plt.bar(xvalues + widths[2], heights_cupy["dry_run_time"],
            color=purples[0], align="center", width=width, alpha=1, hatch=hatches[0],
            edgecolor='w', bottom=heights_cupy["import_time"] + heights_cupy["creation_time"])
    plt.bar(xvalues + widths[3], heights_cupy["simulation_times_mean"],
            color=purples[1], align="center", width=width, alpha=1, hatch=hatches[1],
            edgecolor='w', bottom=heights_cupy["import_time"] + heights_cupy["creation_time"])
    
    plt.bar(xvalues + widths[4], heights_cuquantum["dry_run_time"],
            color=greens[0], align="center", width=width, alpha=1, hatch=hatches[0],
            edgecolor='w', bottom=heights_cuquantum["import_time"] + heights_cuquantum["creation_time"])
    plt.bar(xvalues + widths[5], heights_cuquantum["simulation_times_mean"],
            color=greens[1], align="center", width=width, alpha=1, hatch=hatches[1],
            edgecolor='w', bottom=heights_cuquantum["import_time"] + heights_cuquantum["creation_time"])

    plt.xlabel("Number of qubits")
    plt.ylabel("Execution time (sec)")
    
    legend_elements = [
        Patch(facecolor="w", edgecolor="k", hatch=hatches[0], label="Dry run time"),
        Patch(facecolor="w", edgecolor="k", hatch=hatches[1], label="Simulation time"),
        Patch(color=greys[1], label="Import time"),
        Patch(color=oranges[1], label="numba"),
        Patch(color=purples[1], label="cupy"),
        Patch(color=greens[1], label="cuquantum"),
    ]
    plt.legend(handles=legend_elements)
    if save:
        plt.savefig(f"qibojit_dry_vs_simulation_{circuit}_{precision}.pdf", bbox_inches="tight")
    else:
        plt.show()


def plot_breakdown_circuits(data, nqubits, precision="double", width=0.1, fontsize=30, save=False):
    """Creates dry run vs simulation barplot with import time breakdown for given number of qubits varying the circuit."""
    matplotlib.rcParams["font.size"] = fontsize
    # Set plot params
    hatches = ['/', '\\', 'o', '-', 'x', '.', '*']
    width = 0.1
    quantities = ["import_time", "creation_time", "dry_run_time", "simulation_times_mean"]
    
    circuits = ["qft", "variational", "supremacy", "qv", "bv"]
    greys = sns.color_palette("Greys", 2)
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
            color=greys[0], align="center", width=width, alpha=1, hatch=hatches[0],
            edgecolor='w')
    plt.bar(xvalues - width / 2, heights_cupy["import_time"],
            color=greys[1], align="center", width=width, alpha=1, hatch=hatches[1],
            edgecolor='w')
    
    plt.bar(xvalues + width / 2, heights_cuquantum["import_time"],
            color=greys[0], align="center", width=width, alpha=1, hatch=hatches[0],
            edgecolor='w')
    plt.bar(xvalues + 3 * width / 2, heights_cuquantum["import_time"],
            color=greys[1], align="center", width=width, alpha=1, hatch=hatches[1],
            edgecolor='w')
    
    plt.bar(xvalues - 3 * width / 2, heights_cupy["dry_run_time"],
            color=purples[0], align="center", width=width, alpha=1, hatch=hatches[0],
            edgecolor='w', bottom=heights_cupy["import_time"] + heights_cupy["creation_time"])
    plt.bar(xvalues - width / 2, heights_cupy["simulation_times_mean"],
            color=purples[1], align="center", width=width, alpha=1, hatch=hatches[1],
            edgecolor='w', bottom=heights_cupy["import_time"] + heights_cupy["creation_time"])
    
    plt.bar(xvalues + width / 2, heights_cuquantum["dry_run_time"],
            color=greens[0], align="center", width=width, alpha=1, hatch=hatches[0],
            edgecolor='w', bottom=heights_cuquantum["import_time"] + heights_cuquantum["creation_time"])
    plt.bar(xvalues + 3 * width / 2, heights_cuquantum["simulation_times_mean"],
            color=greens[1], align="center", width=width, alpha=1, hatch=hatches[1],
            edgecolor='w', bottom=heights_cuquantum["import_time"] + heights_cuquantum["creation_time"])

    plt.ylabel("Execution time (sec)")
    
    legend_elements = [
        Patch(facecolor="w", edgecolor="k", hatch=hatches[0], label="Dry run time"),
        Patch(facecolor="w", edgecolor="k", hatch=hatches[1], label="Simulation time"),
        Patch(color=greys[1], label="Import time"),
        Patch(color=purples[1], label="cupy"),
        Patch(color=greens[1], label="cuquantum"),
        
    ]
    plt.legend(handles=legend_elements, bbox_to_anchor=(1,1))
    
    if save:
        plt.savefig(f"qibojit_dry_vs_simulation_{nqubits}qubits_{precision}.pdf", bbox_inches="tight")
    else:
        plt.show()


def plot_multigpu(data, nqubits, quantity, precision="double", fontsize=45, legend=False, save=False):
    matplotlib.rcParams["font.size"] = fontsize
    # Set plot params
    hatches = ['/', '\\', 'o', '-', 'x', '.', '*']
    width = 0.1
    quantities = ["import_time", "creation_time", "dry_run_time", "simulation_times_mean",
                  "total_simulation_time", "total_dry_time"]
    circuits = ["qft", "variational", "supremacy", "qv", "bv"]

    widths = [-5 * width / 2, - 3 * width / 2, -width / 2, width / 2, 3 * width / 2, 5 * width / 2]
    oranges = sns.color_palette("Oranges", 3)
    purples = sns.color_palette("Purples", 3)
    greens = sns.color_palette("Greens", 3)

    # Plot the results
    plt.figure(figsize=(25, 9))

    xvalues = np.array(range(len(circuits)))
    plt.xticks(xvalues, circuits)

    base_condition = ((data["precision"] == precision) & (data["nqubits"] == nqubits))
    heights1 = {}
    heights2 = {}
    heights4 = {}
    for backend in ["qibojit", "qibotf"]:    
        condition = base_condition & (data["library_options"] == f"backend={backend},accelerators=4/GPU:3")
        heights1[backend] = {q: np.array([float(data[condition & (data["circuit"] == c)][q]) for c in circuits])
                             for q in quantities}
        condition = base_condition & (data["library_options"] == f"backend={backend},accelerators=2/GPU:2+2/GPU:3")
        heights2[backend] = {q: np.array([float(data[condition & (data["circuit"] == c)][q]) for c in circuits])
                             for q in quantities}
        condition = base_condition & (data["library_options"] == f"backend={backend},accelerators=1/GPU:0+1/GPU:1+1/GPU:2+1/GPU:3")
        heights4[backend] = {q: np.array([float(data[condition & (data["circuit"] == c)][q]) for c in circuits])
                            for q in quantities}

    plt.bar(xvalues + widths[0], heights1["qibojit"][quantity],
            color=purples[0], align="center", width=width, alpha=1, hatch=hatches[0], edgecolor='w')
    plt.bar(xvalues + widths[1], heights1["qibotf"][quantity],
            color=greens[0], align="center", width=width, alpha=1, hatch=hatches[1], edgecolor='w')

    plt.bar(xvalues + widths[2], heights2["qibojit"][quantity],
            color=purples[1], align="center", width=width, alpha=1, hatch=hatches[0], edgecolor='w')
    plt.bar(xvalues + widths[3], heights2["qibotf"][quantity],
            color=greens[1], align="center", width=width, alpha=1, hatch=hatches[1], edgecolor='w')

    plt.bar(xvalues + widths[4], heights4["qibojit"][quantity],
            color=purples[2], align="center", width=width, alpha=1, hatch=hatches[0], edgecolor='w')
    plt.bar(xvalues + widths[5], heights4["qibotf"][quantity],
            color=greens[2], align="center", width=width, alpha=1, hatch=hatches[1], edgecolor='w')

    plt.title(f"Multi-GPU - {nqubits} qubits")
    if quantity == "total_dry_time":
        plt.ylabel("Total dry run time (sec)")
    elif quantity == "dry_run_time":
        plt.ylabel("Dry run time (sec)")
    elif quantity == "total_simulation_time":
        plt.ylabel("Total simulation time (sec)")
    elif quantity == "simulation_times_mean":
        plt.ylabel("Simulation time (sec)")

    legend_elements = [
        Patch(facecolor=purples[2], edgecolor="w", hatch=hatches[0], label="qibojit"),
        Patch(facecolor=greens[2], edgecolor="w", hatch=hatches[1], label="qibotf"),
        Patch(color=purples[0], label="1x GPU"),
        Patch(color=purples[1], label="2x GPUs"),
        Patch(color=purples[2], label="4x GPUs"),
    ]
    if legend:
        plt.legend(handles=legend_elements, bbox_to_anchor=(1,1))
    if save:
        plt.savefig(f"multigpu_{nqubits}qubits_{quantity}_{precision}.pdf", bbox_inches="tight")
    else:
        plt.show()
