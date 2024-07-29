from plots.utils import load_data

import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Patch
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['font.family'] = 'STIXGeneral'
import pandas as pd

save = True # if ``True`` plots will be saved in the current directory as pdfs


def plot_scaling_expectation(input1, input2, input3,input4, circuit, quantity, precision="double", fontsize=30, legend=True, save=False):
    
 
    combine_data  = input1
    combine_data2  = input2
    combine_data3  = input3
    combine_data4  = input4

    matplotlib.rcParams["font.size"] = fontsize
    # Prepare GPU data
    condition  = (combine_data["circuit"]  == circuit) & (combine_data["precision"]  == precision)
    condition2  = (combine_data2["circuit"]  == circuit) & (combine_data2["precision"]  == precision)
    condition3  = (combine_data3["circuit"]  == circuit) & (combine_data3["precision"]  == precision)
    condition4  = (combine_data4["circuit"]  == circuit) & (combine_data4["precision"]  == precision)

    data = {}
    data["qibotn MPI"] = combine_data[(combine_data["library_options"] == "backend=qibotn,platform=cutensornet,computation_settings=cu_tensornet_mpi_expectation.json") & condition]
    data["qibotn NCCL"] = combine_data[(combine_data["library_options"] == "backend=qibotn,platform=cutensornet,computation_settings=cu_tensornet_nccl_expectation.json") & condition]
    data["qibotn"] = combine_data[(combine_data["library_options"] == "backend=qibotn,platform=cutensornet,computation_settings=cu_tensornet_expectation.json") & condition]
    data["qibojit numba"] = combine_data[(combine_data["library_options"] == "backend=qibojit,platform=numba,expectation=XXXZ") & condition]
 
    data2 = {}
    data2["qibotn MPI"] = combine_data2[(combine_data2["library_options"] == "backend=qibotn,platform=cutensornet,computation_settings=cu_tensornet_mpi_expectation.json") & condition2]
    data2["qibotn NCCL"] = combine_data2[(combine_data2["library_options"] == "backend=qibotn,platform=cutensornet,computation_settings=cu_tensornet_nccl_expectation.json") & condition2]
    data2["qibotn"] = combine_data2[(combine_data2["library_options"] == "backend=qibotn,platform=cutensornet,computation_settings=cu_tensornet_expectation.json") & condition2]
    data2["qibojit numba"] = combine_data2[(combine_data2["library_options"] == "backend=qibojit,platform=numba,expectation=XXXZ") & condition2]
 
    data3 = {}
    data3["qibotn MPI"] = combine_data3[(combine_data3["library_options"] == "backend=qibotn,platform=cutensornet,computation_settings=cu_tensornet_mpi_expectation.json") & condition3]
    data3["qibotn NCCL"] = combine_data3[(combine_data3["library_options"] == "backend=qibotn,platform=cutensornet,computation_settings=cu_tensornet_nccl_expectation.json") & condition3]
    data3["qibotn"] = combine_data3[(combine_data3["library_options"] == "backend=qibotn,platform=cutensornet,computation_settings=cu_tensornet_expectation.json") & condition3]
    data3["qibojit numba"] = combine_data3[(combine_data3["library_options"] == "backend=qibojit,platform=numba,expectation=XXXZ") & condition3]
 
    data4 = {}
    data4["qibotn MPI"] = combine_data4[(combine_data4["library_options"] == "backend=qibotn,platform=cutensornet,computation_settings=cu_tensornet_mpi_expectation.json") & condition4]
    data4["qibotn NCCL"] = combine_data4[(combine_data4["library_options"] == "backend=qibotn,platform=cutensornet,computation_settings=cu_tensornet_nccl_expectation.json") & condition4]
    data4["qibotn"] = combine_data4[(combine_data4["library_options"] == "backend=qibotn,platform=cutensornet,computation_settings=cu_tensornet_expectation.json") & condition4]
    data4["qibojit numba"] = combine_data4[(combine_data4["library_options"] == "backend=qibojit,platform=numba,expectation=XXXZ") & condition4]
 
    # Plot data
    cpu_cp = sns.color_palette("Oranges", 7)
    gpu_cp = sns.color_palette("Purples", 7)
    gpu_cp2 = sns.color_palette("Greens", 7)
    gpu_cp3 = sns.color_palette("Reds", 7)
    gpu_cp4 = sns.color_palette("Blues", 7)
    plt.figure(figsize=(16, 9))
    
    # 24 hours in seconds
    seconds_in_24_hours = 24 * 60 * 60

    # Plotting the horizontal dashed line
    plt.axhline(y=seconds_in_24_hours, color='r', linestyle='--', linewidth=1.5, label='24 hours')

    plt.semilogy(data["qibotn"]["nqubits"], data["qibotn"][quantity],
                 color=cpu_cp[3], linewidth=1.5, label="1x1 gpu", marker=".", markersize=10)     
    plt.semilogy(data2["qibotn MPI"]["nqubits"], data2["qibotn MPI"][quantity],
                 color=gpu_cp[3], linewidth=1.5, label="1x4 gpu MPI", marker=".", markersize=10)  
    # plt.semilogy(data["qibotn NCCL"]["nqubits"], data["qibotn NCCL"][quantity],
    #              color=gpu_cp[5], linewidth=1.5, label="1x8 gpu NCCL", marker=".", markersize=10)   
    
    plt.semilogy(data3["qibotn MPI"]["nqubits"], data3["qibotn MPI"][quantity],
                 color=gpu_cp2[3], linewidth=1.5, label="2x4 gpu MPI", marker=".", markersize=10)  
    plt.semilogy(data4["qibotn MPI"]["nqubits"], data4["qibotn MPI"][quantity],
                 color=gpu_cp3[3], linewidth=1.5, label="4x4 gpu MPI", marker=".", markersize=10)  
    # plt.semilogy(data4["qibotn MPI"]["nqubits"], data4["qibotn MPI"][quantity],
    #              color=gpu_cp5[3], linewidth=1.5, label="4x8 gpu MPI", marker=".", markersize=10)  
    
    # plt.semilogy(data["qibojit numba"]["nqubits"], data["qibojit numba"][quantity],
    #              color=cpu_cp[2], linewidth=1.5, label="CPU", marker=".", markersize=10)  
    
    # plt.ylim(bottom=1e-4, top=1e3)
    # plt.xlim(left=0, right=1750)
    # plt.xlim(left=0, right=60)

    #plt.xlim(right=31)

    plt.title(f"Expectation: {circuit}, depth {5}, {precision} precision")
    plt.xlabel("Number of qubits")
    if quantity == "total_dry_time":
        plt.ylabel("Total dry run time (sec)")
    elif quantity == "total_simulation_time":
        plt.ylabel("Total simulation time (sec)")
    elif quantity == "simulation_times_mean":
        plt.ylabel("Simulation times mean (sec)")
    if legend:
        plt.legend(fontsize="small")
    if save:
        plt.savefig(f"qibo_scaling_{circuit}_{quantity}_{precision}_ex.pdf", bbox_inches="tight")
    else:
        plt.show()
        

# data1 = load_data("/home/user3/qibotn_benchmarks/qibojit-benchmarks/qibotn_expectation_double_1x8_var.dat")
# plot_scaling_expectation(data1,"variational", "simulation_times_mean","double", legend=True, save=save)

# data1 = load_data("/home/user3/qibotn_benchmarks/qibojit-benchmarks/qibotn_expectation_double_1x8_sup.dat")
# plot_scaling_expectation(data1,"supremacy", "simulation_times_mean","double", legend=True, save=save)

# data1 = load_data("/home/user3/qibotn_benchmarks/qibojit-benchmarks/qibotn_expectation_double_1x8_qft.dat")
# data1 = load_data("/home/user3/qibotn_benchmarks/qibojit-benchmarks/qibotn_expectation_double_1x8_sup.dat")
# data1 = load_data("/home/user3/qibotn_benchmarks/qibojit-benchmarks/qibotn_expectation_double_1x8_var.dat")
data1 = load_data("/home/project/11003124/tankya/costa1/qibojit-benchmarks/qibotn_expectation_double_1x1_variational_d5.dat")
data2 = load_data("/home/project/11003124/tankya/costa1/qibojit-benchmarks/qibotn_expectation_double_1x4_variational_d5.dat")
data3 = load_data("/home/project/11003124/tankya/costa1/qibojit-benchmarks/qibotn_expectation_double_2x4_variational_d5.dat")
data4 = load_data("/home/project/11003124/tankya/costa1/qibojit-benchmarks/qibotn_expectation_double_4x4_variational_d5.dat")

plot_scaling_expectation(data1,data2,data3,data4,"variational", "simulation_times_mean","double", legend=True, save=save)

#1x4 Missing value

{"datetime": "2024-07-13 01:38:18", "nqubits": 10, "nreps": 1, "import_time": 2.0695817470550537, "library_options": "backend=qibotn,platform=cutensornet,computation_settings=cu_tensornet_mpi_expectation.json", "library": "qibo", "precision": "double", "device": "/CPU:0", "version": "0.2.5", "circuit": "variational", "circuit_options": "nqubits=10, nlayers=5, seed=123", "creation_time": 0.12717008590698242, "dry_run_time": 4.76837158203125e-07, "dtype": "complex128", "simulation_times": [2.722426176071167], "simulation_times_mean": 2.722426176071167, "simulation_times_std": 0.0, "expectation_result": [[[0.044218473681389266]]], "expectation_result_mean": 0.044218473681389266, "expectation_result_std": 0.0}

{"datetime": "2024-07-13 01:38:18", "nqubits": 40, "nreps": 1, "import_time": 2.0695817470550537, "library_options": "backend=qibotn,platform=cutensornet,computation_settings=cu_tensornet_mpi_expectation.json", "library": "qibo", "precision": "double", "device": "/CPU:0", "version": "0.2.5", "circuit": "variational", "circuit_options": "nqubits=40, nlayers=5, seed=123", "creation_time": 0.12717008590698242, "dry_run_time": 4.76837158203125e-07, "dtype": "complex128", "simulation_times": [92.54630327224731], "simulation_times_mean": 92.54630327224731, "simulation_times_std": 0.0, "expectation_result": [[[1.0185800644540888e-06]]], "expectation_result_mean": 1.0185800644540888e-06, "expectation_result_std": 0.0}

{"datetime": "2024-07-13 01:38:18", "nqubits": 60, "nreps": 1, "import_time": 2.0695817470550537, "library_options": "backend=qibotn,platform=cutensornet,computation_settings=cu_tensornet_mpi_expectation.json", "library": "qibo", "precision": "double", "device": "/CPU:0", "version": "0.2.5", "circuit": "variational", "circuit_options": "nqubits=60, nlayers=5, seed=123", "creation_time": 0.12717008590698242, "dry_run_time": 4.76837158203125e-07, "dtype": "complex128", "simulation_times": [271.3857560157776], "simulation_times_mean": 271.3857560157776, "simulation_times_std": 0.0, "expectation_result": [[[5.877344374846953e-11]]], "expectation_result_mean": 5.877344374846953e-11, "expectation_result_std": 0.0}

{"datetime": "2024-07-13 01:38:18", "nqubits": 80, "nreps": 1, "import_time": 2.0695817470550537, "library_options": "backend=qibotn,platform=cutensornet,computation_settings=cu_tensornet_mpi_expectation.json", "library": "qibo", "precision": "double", "device": "/CPU:0", "version": "0.2.5", "circuit": "variational", "circuit_options": "nqubits=80, nlayers=5, seed=123", "creation_time": 0.12717008590698242, "dry_run_time": 4.76837158203125e-07, "dtype": "complex128", "simulation_times": [1084.1304409503937], "simulation_times_mean": 1084.1304409503937, "simulation_times_std": 0.0, "expectation_result": [[[5.36328554751669e-16]]], "expectation_result_mean": 5.36328554751669e-16, "expectation_result_std": 0.0}

{"datetime": "2024-07-13 01:38:18", "nqubits": 110, "nreps": 1, "import_time": 2.0695817470550537, "library_options": "backend=qibotn,platform=cutensornet,computation_settings=cu_tensornet_mpi_expectation.json", "library": "qibo", "precision": "double", "device": "/CPU:0", "version": "0.2.5", "circuit": "variational", "circuit_options": "nqubits=110, nlayers=5, seed=123", "creation_time": 0.12717008590698242, "dry_run_time": 4.76837158203125e-07, "dtype": "complex128", "simulation_times": [9504.664041519165], "simulation_times_mean": 9504.664041519165, "simulation_times_std": 0.0, "expectation_result": [[[3.446458226795824e-19]]], "expectation_result_mean": 3.446458226795824e-19, "expectation_result_std": 0.0}

{"datetime": "2024-07-13 01:38:18", "nqubits": 130, "nreps": 1, "import_time": 2.0695817470550537, "library_options": "backend=qibotn,platform=cutensornet,computation_settings=cu_tensornet_mpi_expectation.json", "library": "qibo", "precision": "double", "device": "/CPU:0", "version": "0.2.5", "circuit": "variational", "circuit_options": "nqubits=130, nlayers=5, seed=123", "creation_time": 0.12717008590698242, "dry_run_time": 4.76837158203125e-07, "dtype": "complex128", "simulation_times": [14543.339746236801], "simulation_times_mean": 14543.339746236801, "simulation_times_std": 0.0, "expectation_result": [[[1.789240796703424e-20]]], "expectation_result_mean": 1.789240796703424e-20, "expectation_result_std": 0.0}

