from plots.utils import load_data

import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Patch
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['font.family'] = 'STIXGeneral'
import pandas as pd

save = True # if ``True`` plots will be saved in the current directory as pdfs


def plot_scaling_expectation(input1, input2, input3, circuit, quantity, precision="double", fontsize=30, legend=True, save=False):
    
 
    combine_data  = input1
    combine_data2  = input2
    combine_data3  = input3

    matplotlib.rcParams["font.size"] = fontsize
    # Prepare GPU data
    condition  = (combine_data["circuit"]  == circuit) & (combine_data["precision"]  == precision)
    condition2  = (combine_data2["circuit"]  == circuit) & (combine_data2["precision"]  == precision)
    condition3  = (combine_data3["circuit"]  == circuit) & (combine_data3["precision"]  == precision)

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
 
    # Plot data
    cpu_cp = sns.color_palette("Oranges", 7)
    gpu_cp = sns.color_palette("Purples", 7)
    gpu_cp2 = sns.color_palette("Greens", 7)
    gpu_cp3 = sns.color_palette("Reds", 7)
  
    plt.figure(figsize=(16, 9))
    

    plt.semilogy(data["qibotn"]["nqubits"], data["qibotn"][quantity],
                 color=cpu_cp[3], linewidth=1.5, label="1x1 gpu", marker=".", markersize=10)     
    plt.semilogy(data["qibotn MPI"]["nqubits"], data["qibotn MPI"][quantity],
                 color=gpu_cp[3], linewidth=1.5, label="1x8 gpu MPI", marker=".", markersize=10)  
    # plt.semilogy(data["qibotn NCCL"]["nqubits"], data["qibotn NCCL"][quantity],
    #              color=gpu_cp[5], linewidth=1.5, label="1x8 gpu NCCL", marker=".", markersize=10)   
    
    plt.semilogy(data2["qibotn MPI"]["nqubits"], data2["qibotn MPI"][quantity],
                 color=gpu_cp2[3], linewidth=1.5, label="2x8 gpu MPI", marker=".", markersize=10)  
    plt.semilogy(data3["qibotn MPI"]["nqubits"], data3["qibotn MPI"][quantity],
                 color=gpu_cp3[3], linewidth=1.5, label="4x8 gpu MPI", marker=".", markersize=10)  
    
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
        
def plot_pathfinding_data(input1, input2, input3, circuit, quantity, precision="double", fontsize=30, legend=True, save=False):
    num_reps=3
    num_pathfinding_per_rep=4 #equivalent to total number of GPUs
    combine_data  = input1
    combine_data2  = input2
    combine_data3  = input3

    matplotlib.rcParams["font.size"] = fontsize
    # Prepare GPU data
    condition  = (combine_data["circuit"]  == circuit) & (combine_data["precision"]  == precision)
    condition2  = (combine_data2["circuit"]  == circuit) & (combine_data2["precision"]  == precision)
    condition3  = (combine_data3["circuit"]  == circuit) & (combine_data3["precision"]  == precision)

    data = {}
    data["qibotn MPI"] = combine_data[(combine_data["library_options"] == "backend=qibotn,platform=cutensornet,computation_settings=cu_tensornet_mpi_expectation.json") & condition]
    data2 = {}
    data2["qibotn MPI"] = combine_data2[(combine_data2["library_options"] == "backend=qibotn,platform=cutensornet,computation_settings=cu_tensornet_mpi_expectation.json") & condition2]
    data3 = {}
    data3["qibotn MPI"] = combine_data3[(combine_data3["library_options"] == "backend=qibotn,platform=cutensornet,computation_settings=cu_tensornet_mpi_expectation.json") & condition3]
         
       # Plot data
       
    color_1x1 = sns.color_palette("Oranges", 7)
    color_1x4 = sns.color_palette("Purples", 7)
    color_2x4 = sns.color_palette("Greens", 7)
    color_4x4 = sns.color_palette("Reds", 7)
                
    def extract_metric(data,rep_index,metric_of_interest):
        #metric of interest 0: num slices, 1: opt cost, 2: largest intermediate, 3: time
        metric_list_total=[]
        metric_max=[]
        metric_min=[]
        metric_max_index=[]
        metric_min_index=[]
        for each_record in range(len(data["qibotn MPI"]['nqubits'])):
            each_rep = data["qibotn MPI"][quantity][each_record][rep_index][0]
            split_data = [each_rep[i:i + 4] for i in range(0, len(each_rep), 4)]
            metric_list=[]
            for each_gpu in range(len(split_data)):
                metric_list.append(split_data[each_gpu][metric_of_interest])
            metric_list_total.append(metric_list)
            max_value = max(metric_list)
            max_value_index = metric_list.index(max_value)
            min_value = min(metric_list)
            min_value_index = metric_list.index(min_value)
            metric_max.append(max_value)
            metric_min.append(min_value)
            metric_max_index.append(max_value_index)
            metric_min_index.append(min_value_index)
            
        return metric_list_total, metric_max, metric_min, metric_max_index, metric_min_index
    
    def extract_metric_with_index_of_interest(data,rep_index,metric_of_interest,index_of_interest):
        #metric of interest 0: num slices, 1: opt cost, 2: largest intermediate, 3: time
        metric_list_total=[]
        metric_max=[]
        metric_min=[]
        metric_selected=[]
        
        for each_record in range(len(data["qibotn MPI"]['nqubits'])):
            each_rep = data["qibotn MPI"][quantity][each_record][rep_index][0]
            split_data = [each_rep[i:i + 4] for i in range(0, len(each_rep), 4)]
            metric_list=[]
            for each_gpu in range(len(split_data)):
                metric_list.append(split_data[each_gpu][metric_of_interest])
            metric_list_total.append(metric_list)
            max_value = max(metric_list)
            interest_value = metric_list[(index_of_interest[each_record])]
            min_value = min(metric_list)
            
            metric_max.append(max_value)
            metric_min.append(min_value)
            metric_selected.append(interest_value)

        return metric_list_total, metric_max, metric_min, metric_selected
    
    rep_data = 0
    rep_data2 = 1
    rep_data3 = 0
    
    data_opt_cost_original, max_cost, min_cost,max_cost_index, min_cost_index = extract_metric(data,rep_data,1)
    data_opt_cost = [list(i) for i in zip(*data_opt_cost_original)]
    
    data_opt_cost_original2, max_cost2, min_cost2, max_cost_index2, min_cost_index2 = extract_metric(data2,rep_data2,1)
    data_opt_cost2 = [list(i) for i in zip(*data_opt_cost_original2)]
  
    data_opt_cost_original3, max_cost3, min_cost3, max_cost_index3, min_cost_index3 = extract_metric(data3,rep_data3,1)
    data_opt_cost3 = [list(i) for i in zip(*data_opt_cost_original3)]
    
    ##### 
    data_num_slices_original, _, _,selected1 = extract_metric_with_index_of_interest(data,rep_data,0,min_cost_index)
    data_num_slices = [list(i) for i in zip(*data_num_slices_original)]
    
    data_num_slices_original2, _, _, selected2= extract_metric_with_index_of_interest(data2,rep_data2,0,min_cost_index2)
    data_num_slices2 = [list(i) for i in zip(*data_num_slices_original2)]
  
    data_num_slices_original3, _, _, selected3 = extract_metric_with_index_of_interest(data3,rep_data3,0,min_cost_index3)
    data_num_slices3 = [list(i) for i in zip(*data_num_slices_original3)]
    
    ####_time
    data_time_original, max_cost_time, min_cost_time,max_cost_index_time, min_cost_index_time = extract_metric(data,rep_data,3)
    data_time = [list(i) for i in zip(*data_time_original)]
    
    data_time_original2, max_cost2_time, min_cost2_time, max_cost_index2_time, min_cost_index2_time = extract_metric(data2,rep_data2,3)
    data_time2 = [list(i) for i in zip(*data_time_original2)]
  
    data_time_original3, max_cost3_time, min_cost3_time, max_cost_index3_time, min_cost_index3_time = extract_metric(data3,rep_data3,3)
    data_time3 = [list(i) for i in zip(*data_time_original3)]
    
    # for i in range(len(data_opt_cost)):
    #     print("max", max_cost[i],"min",min_cost[i],data_opt_cost[i])
    # print("1x4",data["qibotn MPI"]["nqubits"])
    # print("2x4",data2["qibotn MPI"]["nqubits"])
    # print("4x4",data3["qibotn MPI"]["nqubits"])      
    
    
    #### PLOT COST OF PATH ####
    plt.figure(figsize=(16, 9))

    color4x4=3
    # 4x4
    plt.scatter(data3["qibotn MPI"]["nqubits"], data_opt_cost3[0],
                color=color_4x4[color4x4], marker=".", s=100)
    plt.scatter(data3["qibotn MPI"]["nqubits"], data_opt_cost3[1],
                color=color_4x4[color4x4], marker=".", s=100)
    plt.scatter(data3["qibotn MPI"]["nqubits"], data_opt_cost3[2],
                color=color_4x4[color4x4], marker=".", s=100)
    plt.scatter(data3["qibotn MPI"]["nqubits"], data_opt_cost3[3],
                color=color_4x4[color4x4], marker=".", s=100)
    plt.scatter(data3["qibotn MPI"]["nqubits"], data_opt_cost3[4],
                color=color_4x4[color4x4], marker=".", s=100)
    plt.scatter(data3["qibotn MPI"]["nqubits"], data_opt_cost3[5],
                color=color_4x4[color4x4], marker=".", s=100)
    plt.scatter(data3["qibotn MPI"]["nqubits"], data_opt_cost3[6],
                color=color_4x4[color4x4], marker=".", s=100)
    plt.scatter(data3["qibotn MPI"]["nqubits"], data_opt_cost3[7],
                color=color_4x4[color4x4], marker=".", s=100)
    plt.scatter(data3["qibotn MPI"]["nqubits"], data_opt_cost3[8],
                color=color_4x4[color4x4], marker=".", s=100)
    plt.scatter(data3["qibotn MPI"]["nqubits"], data_opt_cost3[9],
                color=color_4x4[color4x4], marker=".", s=100)
    plt.scatter(data3["qibotn MPI"]["nqubits"], data_opt_cost3[10],
                color=color_4x4[color4x4], marker=".", s=100)
    plt.scatter(data3["qibotn MPI"]["nqubits"], data_opt_cost3[11],
                color=color_4x4[color4x4], marker=".", s=100)
    plt.scatter(data3["qibotn MPI"]["nqubits"], data_opt_cost3[12],
                color=color_4x4[color4x4], marker=".", s=100)
    plt.scatter(data3["qibotn MPI"]["nqubits"], data_opt_cost3[13],
                color=color_4x4[color4x4], marker=".", s=100)
    plt.scatter(data3["qibotn MPI"]["nqubits"], data_opt_cost3[14],
                color=color_4x4[color4x4], marker=".", s=100)
    plt.scatter(data3["qibotn MPI"]["nqubits"], data_opt_cost3[15],
                color=color_4x4[color4x4], marker=".", s=100)

    # 2x4
    plt.scatter(data2["qibotn MPI"]["nqubits"], data_opt_cost2[0],
                color=color_2x4[2], marker=".", s=100)
    plt.scatter(data2["qibotn MPI"]["nqubits"], data_opt_cost2[1],
                color=color_2x4[2], marker=".", s=100)
    plt.scatter(data2["qibotn MPI"]["nqubits"], data_opt_cost2[2],
                color=color_2x4[2], marker=".", s=100)
    plt.scatter(data2["qibotn MPI"]["nqubits"], data_opt_cost2[3],
                color=color_2x4[2], marker=".", s=100)
    plt.scatter(data2["qibotn MPI"]["nqubits"], data_opt_cost2[4],
                color=color_2x4[2], marker=".", s=100)
    plt.scatter(data2["qibotn MPI"]["nqubits"], data_opt_cost2[5],
                color=color_2x4[2], marker=".", s=100)
    plt.scatter(data2["qibotn MPI"]["nqubits"], data_opt_cost2[6],
                color=color_2x4[2], marker=".", s=100)
    plt.scatter(data2["qibotn MPI"]["nqubits"], data_opt_cost2[7],
                color=color_2x4[2], marker=".", s=100)



   # 1x4
    plt.scatter(data["qibotn MPI"]["nqubits"], data_opt_cost[0],
                color=color_1x4[2], marker=".", s=100)
    plt.scatter(data["qibotn MPI"]["nqubits"], data_opt_cost[1],
                color=color_1x4[2], marker=".", s=100)
    plt.scatter(data["qibotn MPI"]["nqubits"], data_opt_cost[2],
                color=color_1x4[2], marker=".", s=100)
    plt.scatter(data["qibotn MPI"]["nqubits"], data_opt_cost[3],
                color=color_1x4[2],marker=".", s=100)
    
    # Best path
    plt.semilogy(data["qibotn MPI"]["nqubits"], min_cost,
                color=color_1x4[3], label="1x4 selected", linewidth=1.5, marker="x", markersize=10)
    # Best path
    plt.semilogy(data2["qibotn MPI"]["nqubits"], min_cost2,
                color=color_2x4[3], label="2x4 selected",linewidth=1.5, marker="x", markersize=10)
    # Best path
    plt.semilogy(data3["qibotn MPI"]["nqubits"], min_cost3,
                color=color_4x4[3], label="4x4 selected",linewidth=1.5, marker="x", markersize=10)

    plt.xlim(left=0, right=305)

    plt.title(f"Cost of Paths Found: {circuit}, depth {5}, {precision} precision")
    plt.xlabel("Number of qubits")
    plt.ylabel("FLOP")
    if legend:
        plt.legend(fontsize="small")
    if save:
        plt.savefig(f"qibo_scaling_{circuit}_{quantity}_{precision}_pathfinding.pdf", bbox_inches="tight")
    else:
        plt.show()
        
#### PLOT NUM OF SLICES ####
    plt.figure(figsize=(16, 9))

    color4x4=3
    # 4x4
    plt.scatter(data3["qibotn MPI"]["nqubits"], data_num_slices3[0],
                color=color_4x4[color4x4], marker=".", s=100)
    plt.scatter(data3["qibotn MPI"]["nqubits"], data_num_slices3[1],
                color=color_4x4[color4x4], marker=".", s=100)
    plt.scatter(data3["qibotn MPI"]["nqubits"], data_num_slices3[2],
                color=color_4x4[color4x4], marker=".", s=100)
    plt.scatter(data3["qibotn MPI"]["nqubits"], data_num_slices3[3],
                color=color_4x4[color4x4], marker=".", s=100)
    plt.scatter(data3["qibotn MPI"]["nqubits"], data_num_slices3[4],
                color=color_4x4[color4x4], marker=".", s=100)
    plt.scatter(data3["qibotn MPI"]["nqubits"], data_num_slices3[5],
                color=color_4x4[color4x4], marker=".", s=100)
    plt.scatter(data3["qibotn MPI"]["nqubits"], data_num_slices3[6],
                color=color_4x4[color4x4], marker=".", s=100)
    plt.scatter(data3["qibotn MPI"]["nqubits"], data_num_slices3[7],
                color=color_4x4[color4x4], marker=".", s=100)
    plt.scatter(data3["qibotn MPI"]["nqubits"], data_num_slices3[8],
                color=color_4x4[color4x4], marker=".", s=100)
    plt.scatter(data3["qibotn MPI"]["nqubits"], data_num_slices3[9],
                color=color_4x4[color4x4], marker=".", s=100)
    plt.scatter(data3["qibotn MPI"]["nqubits"], data_num_slices3[10],
                color=color_4x4[color4x4], marker=".", s=100)
    plt.scatter(data3["qibotn MPI"]["nqubits"], data_num_slices3[11],
                color=color_4x4[color4x4], marker=".", s=100)
    plt.scatter(data3["qibotn MPI"]["nqubits"], data_num_slices3[12],
                color=color_4x4[color4x4], marker=".", s=100)
    plt.scatter(data3["qibotn MPI"]["nqubits"], data_num_slices3[13],
                color=color_4x4[color4x4], marker=".", s=100)
    plt.scatter(data3["qibotn MPI"]["nqubits"], data_num_slices3[14],
                color=color_4x4[color4x4], marker=".", s=100)
    plt.scatter(data3["qibotn MPI"]["nqubits"], data_num_slices3[15],
                color=color_4x4[color4x4], marker=".", s=100)


    # 2x4
    plt.scatter(data2["qibotn MPI"]["nqubits"], data_num_slices2[0],
                color=color_2x4[2], marker=".", s=100)
    plt.scatter(data2["qibotn MPI"]["nqubits"], data_num_slices2[1],
                color=color_2x4[2], marker=".", s=100)
    plt.scatter(data2["qibotn MPI"]["nqubits"], data_num_slices2[2],
                color=color_2x4[2], marker=".", s=100)
    plt.scatter(data2["qibotn MPI"]["nqubits"], data_num_slices2[3],
                color=color_2x4[2], marker=".", s=100)
    plt.scatter(data2["qibotn MPI"]["nqubits"], data_num_slices2[4],
                color=color_2x4[2], marker=".", s=100)
    plt.scatter(data2["qibotn MPI"]["nqubits"], data_num_slices2[5],
                color=color_2x4[2], marker=".", s=100)
    plt.scatter(data2["qibotn MPI"]["nqubits"], data_num_slices2[6],
                color=color_2x4[2], marker=".", s=100)
    plt.scatter(data2["qibotn MPI"]["nqubits"], data_num_slices2[7],
                color=color_2x4[2], marker=".", s=100)


   # 1x4
    plt.scatter(data["qibotn MPI"]["nqubits"], data_num_slices[0],
                color=color_1x4[2], marker=".", s=100)
    plt.scatter(data["qibotn MPI"]["nqubits"], data_num_slices[1],
                color=color_1x4[2], marker=".", s=100)
    plt.scatter(data["qibotn MPI"]["nqubits"], data_num_slices[2],
                color=color_1x4[2], marker=".", s=100)
    plt.scatter(data["qibotn MPI"]["nqubits"], data_num_slices[3],
                color=color_1x4[2],marker=".", s=100)
    
    # Best path
    plt.semilogy(data["qibotn MPI"]["nqubits"], selected1,
                color=color_1x4[3], label="1x4 selected", linewidth=1.5, marker="x", markersize=10)
    # Best path
    plt.semilogy(data2["qibotn MPI"]["nqubits"], selected2,
                color=color_2x4[3], label="2x4 selected",linewidth=1.5, marker="x", markersize=10)
    # Best path
    plt.semilogy(data3["qibotn MPI"]["nqubits"], selected3,
                color=color_4x4[3], label="4x4 selected",linewidth=1.5, marker="x", markersize=10)

    plt.xlim(left=0, right=305)

    plt.title(f"Slicing: {circuit}, depth {5}, {precision} precision")
    plt.xlabel("Number of qubits")
    plt.ylabel("Number of slices")
    if legend:
        plt.legend(fontsize="small")
    if save:
        plt.savefig(f"qibo_scaling_{circuit}_{quantity}_{precision}_slicing.pdf", bbox_inches="tight")
    else:
        plt.show()
        
#### PLOT Time PF ####
    plt.figure(figsize=(16, 9))

    color4x4=3
    # 4x4
    plt.scatter(data3["qibotn MPI"]["nqubits"], data_time3[0],
                color=color_4x4[color4x4], marker=".", s=100)
    plt.scatter(data3["qibotn MPI"]["nqubits"], data_time3[1],
                color=color_4x4[color4x4], marker=".", s=100)
    plt.scatter(data3["qibotn MPI"]["nqubits"], data_time3[2],
                color=color_4x4[color4x4], marker=".", s=100)
    plt.scatter(data3["qibotn MPI"]["nqubits"], data_time3[3],
                color=color_4x4[color4x4], marker=".", s=100)
    plt.scatter(data3["qibotn MPI"]["nqubits"], data_time3[4],
                color=color_4x4[color4x4], marker=".", s=100)
    plt.scatter(data3["qibotn MPI"]["nqubits"], data_time3[5],
                color=color_4x4[color4x4], marker=".", s=100)
    plt.scatter(data3["qibotn MPI"]["nqubits"], data_time3[6],
                color=color_4x4[color4x4], marker=".", s=100)
    plt.scatter(data3["qibotn MPI"]["nqubits"], data_time3[7],
                color=color_4x4[color4x4], marker=".", s=100)
    plt.scatter(data3["qibotn MPI"]["nqubits"], data_time3[8],
                color=color_4x4[color4x4], marker=".", s=100)
    plt.scatter(data3["qibotn MPI"]["nqubits"], data_time3[9],
                color=color_4x4[color4x4], marker=".", s=100)
    plt.scatter(data3["qibotn MPI"]["nqubits"], data_time3[10],
                color=color_4x4[color4x4], marker=".", s=100)
    plt.scatter(data3["qibotn MPI"]["nqubits"], data_time3[11],
                color=color_4x4[color4x4], marker=".", s=100)
    plt.scatter(data3["qibotn MPI"]["nqubits"], data_time3[12],
                color=color_4x4[color4x4], marker=".", s=100)
    plt.scatter(data3["qibotn MPI"]["nqubits"], data_time3[13],
                color=color_4x4[color4x4], marker=".", s=100)
    plt.scatter(data3["qibotn MPI"]["nqubits"], data_time3[14],
                color=color_4x4[color4x4], marker=".", s=100)
    plt.scatter(data3["qibotn MPI"]["nqubits"], data_time3[15],
                color=color_4x4[color4x4], marker=".", s=100)


    # 2x4
    plt.scatter(data2["qibotn MPI"]["nqubits"], data_time2[0],
                color=color_2x4[2], marker=".", s=100)
    plt.scatter(data2["qibotn MPI"]["nqubits"], data_time2[1],
                color=color_2x4[2], marker=".", s=100)
    plt.scatter(data2["qibotn MPI"]["nqubits"], data_time2[2],
                color=color_2x4[2], marker=".", s=100)
    plt.scatter(data2["qibotn MPI"]["nqubits"], data_time2[3],
                color=color_2x4[2], marker=".", s=100)
    plt.scatter(data2["qibotn MPI"]["nqubits"], data_time2[4],
                color=color_2x4[2], marker=".", s=100)
    plt.scatter(data2["qibotn MPI"]["nqubits"], data_time2[5],
                color=color_2x4[2], marker=".", s=100)
    plt.scatter(data2["qibotn MPI"]["nqubits"], data_time2[6],
                color=color_2x4[2], marker=".", s=100)
    plt.scatter(data2["qibotn MPI"]["nqubits"], data_time2[7],
                color=color_2x4[2], marker=".", s=100)


   # 1x4
    plt.scatter(data["qibotn MPI"]["nqubits"], data_time[0],
                color=color_1x4[2], marker=".", s=100)
    plt.scatter(data["qibotn MPI"]["nqubits"], data_time[1],
                color=color_1x4[2], marker=".", s=100)
    plt.scatter(data["qibotn MPI"]["nqubits"], data_time[2],
                color=color_1x4[2], marker=".", s=100)
    plt.scatter(data["qibotn MPI"]["nqubits"], data_time[3],
                color=color_1x4[2],marker=".", s=100)
    
    # Best path
    plt.semilogy(data["qibotn MPI"]["nqubits"], max_cost_time,
                color=color_1x4[3], label="1x4 selected", linewidth=1.5, marker="x", markersize=10)
    # Best path
    plt.semilogy(data2["qibotn MPI"]["nqubits"], max_cost2_time,
                color=color_2x4[3], label="2x4 selected",linewidth=1.5, marker="x", markersize=10)
    # Best path
    plt.semilogy(data3["qibotn MPI"]["nqubits"], max_cost3_time,
                color=color_4x4[3], label="4x4 selected",linewidth=1.5, marker="x", markersize=10)

    plt.xlim(left=0, right=305)

    plt.title(f"Pathfinding Time: {circuit}, depth {5}, {precision} precision")
    plt.xlabel("Number of qubits")
    plt.ylabel("Pathfinding Time (sec)")
    if legend:
        plt.legend(fontsize="small")
    if save:
        plt.savefig(f"qibo_scaling_{circuit}_{quantity}_{precision}_pftime.pdf", bbox_inches="tight")
    else:
        plt.show()

data1 = load_data("/home/project/11003124/tankya/costa1/qibojit-benchmarks/qibotn_pathfind_double_1x4_variational_d5.dat")
data2 = load_data("/home/project/11003124/tankya/costa1/qibojit-benchmarks/qibotn_pathfind_double_2x4_variational_d5.dat")
data3 = load_data("/home/project/11003124/tankya/costa1/qibojit-benchmarks/qibotn_pathfind_double_4x4_variational_d5_old.dat")

plot_pathfinding_data(data1,data2,data3,"variational", "expectation_result","double", legend=True, save=save)
