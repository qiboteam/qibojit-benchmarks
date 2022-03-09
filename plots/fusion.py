"""Generates bar plots for gate fusion comparisons."""
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Patch
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['font.family'] = 'STIXGeneral'


def plot_fusion_nqubits(data, circuit, quantity, precision="double", width=0.1, fontsize=30, legend=False, logscale=False, save=False):
    matplotlib.rcParams["font.size"] = fontsize

    # Set plot params
    hatches = ['/', '\\', 'o', '-', 'x', '.', '*']

    nqubits = [20, 22, 24, 26, 28]
    widths = [-5 * width / 2, - 3 * width / 2, -width / 2, width / 2, 3 * width / 2, 5 * width / 2]
    oranges = sns.color_palette("Oranges", 2)
    purples = sns.color_palette("Purples", 2)
    greens = sns.color_palette("Greens", 2)

    # Plot the results
    plt.figure(figsize=(25, 9))
    plt.title(f"qibojit - Gate fusion - {circuit}")
    
    xvalues = np.array(range(len(nqubits)))
    plt.xticks(xvalues, nqubits)
    
    base_condition = ((data["precision"] == precision) & (data["circuit"] == circuit))
    
    condition = base_condition & (data["library_options"] == "backend=qibojit,platform=numba")
    heights = np.array([float(data[condition & (data["nqubits"] == n)][quantity]) for n in nqubits])
    plt.bar(xvalues + widths[0], heights, color=oranges[0], align="center", width=width, 
            log=logscale, alpha=1, hatch=hatches[0], edgecolor='w')
    condition = base_condition & (data["library_options"] == "backend=qibojit,platform=numba,max_qubits=2")
    heights = np.array([float(data[condition & (data["nqubits"] == n)][quantity]) for n in nqubits])
    plt.bar(xvalues + widths[1], heights, color=oranges[1], align="center", width=width, 
            log=logscale, alpha=1, hatch=hatches[1], edgecolor='w')

    condition = base_condition & (data["library_options"] == "backend=qibojit,platform=cupy")
    heights = np.array([float(data[condition & (data["nqubits"] == n)][quantity]) for n in nqubits])
    plt.bar(xvalues + widths[2], heights, color=purples[0], align="center", width=width, 
            log=logscale, alpha=1, hatch=hatches[0], edgecolor='w')
    condition = base_condition & (data["library_options"] == "backend=qibojit,platform=cupy,max_qubits=2")
    heights = np.array([float(data[condition & (data["nqubits"] == n)][quantity]) for n in nqubits])
    plt.bar(xvalues + widths[3], heights, color=purples[1], align="center", width=width, 
            log=logscale, alpha=1, hatch=hatches[1], edgecolor='w')

    condition = base_condition & (data["library_options"] == "backend=qibojit,platform=cuquantum")
    heights = np.array([float(data[condition & (data["nqubits"] == n)][quantity]) for n in nqubits])
    plt.bar(xvalues + widths[4], heights, color=greens[0], align="center", width=width, 
            log=logscale, alpha=1, hatch=hatches[0], edgecolor='w')
    condition = base_condition & (data["library_options"] == "backend=qibojit,platform=cuquantum,max_qubits=2")
    heights = np.array([float(data[condition & (data["nqubits"] == n)][quantity]) for n in nqubits])
    plt.bar(xvalues + widths[5], heights, color=greens[1], align="center", width=width, 
            log=logscale, alpha=1, hatch=hatches[1], edgecolor='w')

    plt.xlabel("Number of qubits")
    if quantity == "total_dry_time":
        plt.ylabel("Total dry run time (sec)")
    elif quantity == "total_simulation_time":
        plt.ylabel("Total simulation time (sec)")
    
    if legend:
        legend_elements = [
            Patch(facecolor="w", edgecolor="k", hatch=hatches[0], label="No fusion"),
            Patch(facecolor="w", edgecolor="k", hatch=hatches[1], label="Two-qubit fusion"),
            Patch(color=oranges[1], label="numba"),
            Patch(color=purples[1], label="cupy"),
            Patch(color=greens[1], label="cuquantum")
        ]
        plt.legend(handles=legend_elements)
    if save:
        plt.savefig(f"qibojit_fusion_{precision}_{circuit}_{quantity}.pdf", bbox_inches="tight")
    else:
        plt.show()


def plot_fusion_circuits(data, nqubits, quantity, precision="double", width=0.1, fontsize=30, legend=False, logscale=False, save=False):
    matplotlib.rcParams["font.size"] = fontsize

    # Set plot params
    hatches = ['/', '\\', 'o', '-', 'x', '.', '*']
    
    circuits = ["qft", "variational", "supremacy", "qv", "bv"]
    widths = [-5 * width / 2, - 3 * width / 2, -width / 2, width / 2, 3 * width / 2, 5 * width / 2]
    oranges = sns.color_palette("Oranges", 2)
    purples = sns.color_palette("Purples", 2)
    greens = sns.color_palette("Greens", 2)

    # Plot the results
    plt.figure(figsize=(25, 9))
    plt.title(f"qibojit - Gate fusion - {nqubits} qubits")
    
    xvalues = np.array(range(len(circuits)))
    plt.xticks(xvalues, circuits)
    
    base_condition = ((data["precision"] == precision) & (data["nqubits"] == nqubits))
    
    condition = base_condition & (data["library_options"] == "backend=qibojit,platform=numba")
    heights = np.array([float(data[condition & (data["circuit"] == c)][quantity]) for c in circuits])
    plt.bar(xvalues + widths[0], heights, color=oranges[0], align="center", width=width, 
            log=logscale, alpha=1, hatch=hatches[0], edgecolor='w')
    condition = base_condition & (data["library_options"] == "backend=qibojit,platform=numba,max_qubits=2")
    heights = np.array([float(data[condition & (data["circuit"] == c)][quantity]) for c in circuits])
    plt.bar(xvalues + widths[1], heights, color=oranges[1], align="center", width=width, 
            log=logscale, alpha=1, hatch=hatches[1], edgecolor='w')

    condition = base_condition & (data["library_options"] == "backend=qibojit,platform=cupy")
    heights = np.array([float(data[condition & (data["circuit"] == c)][quantity]) for c in circuits])
    plt.bar(xvalues + widths[2], heights, color=purples[0], align="center", width=width, 
            log=logscale, alpha=1, hatch=hatches[0], edgecolor='w')
    condition = base_condition & (data["library_options"] == "backend=qibojit,platform=cupy,max_qubits=2")
    heights = np.array([float(data[condition & (data["circuit"] == c)][quantity]) for c in circuits])
    plt.bar(xvalues + widths[3], heights, color=purples[1], align="center", width=width, 
            log=logscale, alpha=1, hatch=hatches[1], edgecolor='w')

    condition = base_condition & (data["library_options"] == "backend=qibojit,platform=cuquantum")
    heights = np.array([float(data[condition & (data["circuit"] == c)][quantity]) for c in circuits])
    plt.bar(xvalues + widths[4], heights, color=greens[0], align="center", width=width, 
            log=logscale, alpha=1, hatch=hatches[0], edgecolor='w')
    condition = base_condition & (data["library_options"] == "backend=qibojit,platform=cuquantum,max_qubits=2")
    heights = np.array([float(data[condition & (data["circuit"] == c)][quantity]) for c in circuits])
    plt.bar(xvalues + widths[5], heights, color=greens[1], align="center", width=width, 
            log=logscale, alpha=1, hatch=hatches[1], edgecolor='w')

    if quantity == "total_dry_time":
        plt.ylabel("Total dry run time (sec)")
    elif quantity == "total_simulation_time":
        plt.ylabel("Total simulation time (sec)")
    
    if legend:
        legend_elements = [
            Patch(facecolor="w", edgecolor="k", hatch=hatches[0], label="No fusion"),
            Patch(facecolor="w", edgecolor="k", hatch=hatches[1], label="Two-qubit fusion"),
            Patch(color=oranges[1], label="numba"),
            Patch(color=purples[1], label="cupy"),
            Patch(color=greens[1], label="cuquantum")
        ]
        plt.legend(handles=legend_elements)
    if save:
        plt.savefig(f"qibojit_fusion_{precision}_{nqubits}qubits_{quantity}.pdf", bbox_inches="tight")
    else:
        plt.show()