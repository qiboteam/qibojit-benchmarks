import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Patch
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['font.family'] = 'STIXGeneral'


def plot_libraries_double(cpu_data, gpu_data, quantity, nqubits, width=0.07, fontsize=45, legend=False, save=False):
    matplotlib.rcParams["font.size"] = fontsize
    # Process data
    gpu_data = gpu_data.copy()
    gpu_data["library"] += " GPU"
    data = pd.concat([cpu_data, gpu_data])

    # Set plot params
    circuits = ["qft", "variational", "supremacy", "qv", "bv"]
    palette     = sns.color_palette("bright", 7)
    ws = [-4*width, -3*width, -2*width, -width, 0, width, 2 * width, 3*width, 4*width, 5*width]

    # Set up plot
    libraries = [
            "qibo", 
            "qibo GPU", 
            "qiskit", 
            "qiskit-gpu GPU", 
            "qulacs", 
            "qulacs-gpu GPU",
            "hybridq",
            "hybridq-gpu GPU",
            "projectq"
        ]
    colors = {
        "qibo": palette[0],
        "qibo GPU": palette[0],
        "qiskit": palette[1],
        "qiskit-gpu GPU": palette[1],
        "qulacs": palette[2],
        "qulacs-gpu GPU": palette[2],
        "hybridq": palette[4],
        "hybridq-gpu GPU": palette[4],
        "projectq": palette[3]
    }
    labels = {
        "qibo": "Qibo",
        "qibo GPU": "Qibo GPU",
        "qiskit": "Qiskit",
        "qiskit-gpu GPU": "Qiskit GPU",
        "qulacs": "Qulacs",
        "qulacs-gpu GPU": "Qulacs GPU",
        "hybridq": "HybridQ",
        "hybridq-gpu GPU": "HybridQ GPU",
        "projectq": "ProjectQ"
    }
    hatches = {
        "qibo": "/",
        "qibo GPU": "/",
        "qiskit": "-",
        "qiskit-gpu GPU": "-",
        "qulacs": "\\",
        "qulacs-gpu GPU": "\\",
        "hybridq": "x",
        "hybridq-gpu GPU": "x",
        "projectq": "o",
    }

    # Plot the results
    xvalues = np.array(range(len(circuits)))
    plt.figure(figsize=(25, 9))
    base_condition = (data["nqubits"] == nqubits) & (data["precision"] == "double")
    for i, library in enumerate(libraries):
        # Set the color and hatch, library by library
        alpha = 1.0 if "GPU" in library else 0.5
        condition = base_condition & (data["library"] == library)
        height = np.array([float(data[condition & (data["circuit"] == c)][quantity]) for c in circuits])
        plt.bar(xvalues + ws[i], height, color=colors.get(library),
                align="center", width=width, alpha=alpha, label=labels.get(library), 
                log=True, edgecolor='w', hatch=hatches.get(library))

    plt.title(f"{nqubits} qubits - double precision")
    if quantity == "total_dry_time":
        plt.ylabel("Total dry time (sec)")
    elif quantity == "total_simulation_time":
        plt.ylabel("Total simulation time (sec)")

    plt.xticks(xvalues, circuits)
    if legend:
        plt.legend(fontsize="small", bbox_to_anchor=(1,1))
    if save:
        plt.savefig(f"libraries_double_{nqubits}qubits_{quantity}.pdf", bbox_inches="tight")
    else:
        plt.show()


def plot_libraries_single(cpu_data, gpu_data, quantity, nqubits, width=0.1, fontsize=45, legend=False, save=False):
    matplotlib.rcParams["font.size"] = fontsize
    # Process data
    gpu_data = gpu_data.copy()
    gpu_data["library"] += " GPU"
    data = pd.concat([cpu_data, gpu_data])

    # Set plot params
    circuits = ["qft", "variational", "supremacy", "qv", "bv"]
    hatches = ['/', '\\', 'o', '-', 'x', '.', '*', '+']
    palette = sns.color_palette("bright")
    ws = [-3*width, -2*width, -width, 0, width, 2 * width, 3*width, 4*width]

    # Set up plot
    libraries = [
            "qibo", 
            "qibo GPU", 
            "qiskit", 
            "qiskit-gpu GPU", 
            "qsim",
            "qcgpu GPU"
        ]
    colors = {
        "qibo": palette[0],
        "qibo GPU": palette[0],
        "qiskit": palette[1],
        "qiskit-gpu GPU": palette[1],
        "qsim": palette[2],
        "qcgpu GPU": palette[3]
    }
    labels = {
        "qibo": "Qibo",
        "qibo GPU": "Qibo GPU",
        "qiskit": "Qiskit",
        "qiskit-gpu GPU": "Qiskit GPU",
        "qsim": "qsim",
        "qcgpu GPU": "QCGPU"
    }
    hatches = {
        "qibo": "/",
        "qibo GPU": "/",
        "qiskit": "-",
        "qiskit-gpu GPU": "-",
        "qsim": "\\",
        "qcgpu GPU": "x"
    }
        
    # Plot the results
    xvalues = np.array(range(len(circuits)))
    plt.figure(figsize=(25, 9))
    base_condition = (data["nqubits"] == nqubits) & (data["precision"] == "single")
    for i, library in enumerate(libraries):
        alpha = 1.0 if "GPU" in library else 0.5
        condition = base_condition & (data["library"] == library)
        height = np.array([float(data[condition & (data["circuit"] == c)][quantity]) for c in circuits])
        plt.bar(xvalues + ws[i], height, color=colors.get(library),
                align="center", width=width, alpha=alpha, label=labels.get(library), log=True,
                edgecolor='w', hatch=hatches.get(library))

    plt.title(f"{nqubits} qubits - single precision")
    if quantity == "total_dry_time":
        plt.ylabel("Total dry time (sec)")
    elif quantity == "total_simulation_time":
        plt.ylabel("Total simulation time (sec)")

    plt.xticks(xvalues, circuits)
    if legend:
        plt.legend(fontsize="small", bbox_to_anchor=(1,1))
    if save:
        plt.savefig(f"libraries_single_{nqubits}qubits_{quantity}.pdf", bbox_inches="tight")
    else:
        plt.show()