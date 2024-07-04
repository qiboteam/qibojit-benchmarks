"""Benchmark scripts."""
import time
from benchmarks.logger import JsonLogger


def qibotn_benchmark_mpi(nqubits, library, circuit_name, circuit_options=None,
                      library_options=None, precision=None, nreps=1,
                      filename=None):
    """Runs benchmark for different quantum simulation libraries.

    See ``benchmarks/compare.py`` for documentation of each argument.
    """
    from mpi4py import MPI  # this line initializes MPI
    import numpy as np
    import cupy as cp
    #import socket

    try:
    # Try to create MPI.COMM_WORLD
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()
        #hostname = socket.gethostname()
        #device_id = rank % cp.cuda.runtime.getDeviceCount()
    except MPI.Exception:
    # MPI is not available or not launched deliberately, set rank to 0
        rank = 0        
        
    # logs = JsonLogger(filename)
    if rank == 0:
        logs = JsonLogger(filename)
        logs.log(nqubits=nqubits, nreps=nreps)

    if rank == 0:
        start_time = time.time()
    from benchmarks import libraries
    backend = libraries.get(library, library_options)
    if rank == 0:
        logs.log(import_time=time.time() - start_time)
        logs.log(library_options=library_options)
    if precision is not None:

        backend.set_precision(precision)

    if rank == 0:
        logs.log(library=backend.name,
             precision=backend.get_precision(),
             device=backend.get_device(),
             version=backend.__version__)


    from benchmarks import circuits
    gates = circuits.get(circuit_name, nqubits, circuit_options)
    #gates = circuits.get(circuit_name, nqubits, circuit_options, True) #use qibo gate

    if rank == 0:
        logs.log(circuit=circuit_name, circuit_options=str(gates))
        start_time = time.time()
    circuit = backend.from_qasm(gates.to_qasm())
    
    if rank == 0:
        logs.log(creation_time=time.time() - start_time)
        start_time = time.time()
    
    # mem_avail = cp.cuda.Device(device_id).mem_info[0]
    # formatted_string = f"{hostname}/{device_id}/{rank}/{mem_avail}"
    # logs.log(hostname_id_rank_mem=formatted_string)
    
    # result = backend(circuit)
    result = 0 # No dry run for qibotn
    if rank == 0:
        logs.log(dry_run_time=time.time() - start_time)
    # dtype = str(result.dtype)

    del(result)
    mem_avail_list=[]
    if rank == 0:   
        simulation_times = []
        if backend.expectation_flag is not None:
                expectation_result = [] 
    for _ in range(nreps):
        # mem_avail = cp.cuda.Device(device_id).mem_info[0]
        # formatted_string = f"{hostname}/{device_id}/{rank}/{mem_avail}"
        # mem_avail_list.append(formatted_string)

        if rank == 0:
            start_time = time.time()
        result = backend(circuit)
        dtype = str(result.dtype)

        # result, rank = expectation_pauli_tn_MPI(circuit,"complex128","XXXZ")
        if isinstance(result, cp.ndarray):
            result = cp.asnumpy(result)
        else:
            result = np.array([result])

        if rank == 0:
            simulation_times.append(time.time() - start_time)
            #if _==0:
                #modified_string = library_options.replace("=", "_")
                #modified_string = modified_string.replace(",", "")
                #filename = modified_string+str(circuit.nqubits)+".dat"
                #np.savetxt(filename,result)
            #print(result)
            if backend.expectation_flag is not None:
                # magnitude = np.abs(result[0])
                magnitude = np.abs(result)

                magnitude_list = magnitude.tolist()

                expectation_result.append(magnitude_list)
            '''
            else:
                components = library_options.split(',')

                # Iterate through the components to find the one that starts with "platform="
                for component in components:
                    if component.startswith("platform="):
                        # Extract the platform value
                        platform_value = component.split('=')[1]
                        print("Platform:", platform_value)
                        break
                output_text = backend.name + '_' + circuit_name + '_'  +platform_value +  '_' +str(nqubits) + '.npz'
                np.savez(output_text, result)
            '''
        del(result)
    # logs.log(mem_ava=mem_avail_list)

    if rank == 0:
        logs.log(dtype=dtype, simulation_times=simulation_times)
        logs.average("simulation_times")
        if backend.expectation_flag is not None:
                logs.log(dtype=dtype, expectation_result=expectation_result)
                logs.average("expectation_result")
        logs.dump()
        return logs
    
def qibotn_benchmark_single(nqubits, library, circuit_name, circuit_options=None,
                      library_options=None, precision=None, nreps=1,
                      filename=None):
    """Runs benchmark for different quantum simulation libraries.

    See ``benchmarks/compare.py`` for documentation of each argument.
    """
    from mpi4py import MPI  # this line initializes MPI
    import numpy as np
    import cupy as cp
    import socket

    try:
    # Try to create MPI.COMM_WORLD
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()
        hostname = socket.gethostname()
        device_id = rank % cp.cuda.runtime.getDeviceCount()
    except MPI.Exception:
    # MPI is not available or not launched deliberately, set rank to 0
        rank = 0        
    logs = JsonLogger(filename)

    if rank == 0:
        #logs = JsonLogger(filename)
        logs.log(nqubits=nqubits, nreps=nreps)

    if rank == 0:
        start_time = time.time()
    from benchmarks import libraries
    backend = libraries.get(library, library_options)
    if rank == 0:
        logs.log(import_time=time.time() - start_time)
        logs.log(library_options=library_options)
    if precision is not None:

        backend.set_precision(precision)
        backend.expectation_flag

    if rank == 0:
        logs.log(library=backend.name,
             precision=backend.get_precision(),
             device=backend.get_device(),
             version=backend.__version__)

    from benchmarks import circuits
    gates = circuits.get(circuit_name, nqubits, circuit_options)
    #gates = circuits.get(circuit_name, nqubits, circuit_options, True) #use qibo gate

    if rank == 0:
        logs.log(circuit=circuit_name, circuit_options=str(gates))
        start_time = time.time()
    circuit = backend.from_qasm(gates.to_qasm())
    
    if rank == 0:
        logs.log(creation_time=time.time() - start_time)
        start_time = time.time()
    
    # mem_avail = cp.cuda.Device(device_id).mem_info[0]
    # formatted_string = f"{hostname}/{device_id}/{rank}/{mem_avail}"
    # logs.log(hostname_id_rank_mem=formatted_string)
    
    result = backend(circuit)
    
    if rank == 0:
        logs.log(dry_run_time=time.time() - start_time)
    dtype = str(result.dtype)
    del(result)
    mem_avail_list=[]
    if rank == 0:   
        simulation_times = []
        if backend.expectation_flag is not None:
                expectation_result = [] 
    for _ in range(nreps):
        # mem_avail = cp.cuda.Device(device_id).mem_info[0]
        # formatted_string = f"{hostname}/{device_id}/{rank}/{mem_avail}"
        # mem_avail_list.append(formatted_string)

        if rank == 0:
            start_time = time.time()
        # result = backend(circuit)
        result=0
        if isinstance(result, cp.ndarray):
            result = cp.asnumpy(result)
        else:
            result = np.array([result])

        if rank == 0:
            simulation_times.append(time.time() - start_time)
            #if _==0:
                #modified_string = library_options.replace("=", "_")
                #modified_string = modified_string.replace(",", "")
                #filename = modified_string+str(circuit.nqubits)+".dat"
                #np.savetxt(filename,result)
            #print(result)
            if backend.expectation_flag is not None:
                magnitude = np.abs(result[0])
                magnitude_list = magnitude.tolist()

                expectation_result.append(magnitude_list)
            '''
            else:
                components = library_options.split(',')

                # Iterate through the components to find the one that starts with "platform="
                for component in components:
                    if component.startswith("platform="):
                        # Extract the platform value
                        platform_value = component.split('=')[1]
                        print("Platform:", platform_value)
                        break
                output_text = backend.name + '_' + circuit_name + '_'  +platform_value +  '_' +str(nqubits) + '.npz'
                np.savez(output_text, result)
            '''
        del(result)
    # logs.log(mem_ava=mem_avail_list)

    if rank == 0:
        logs.log(dtype=dtype, simulation_times=simulation_times)
        logs.average("simulation_times")
        if backend.expectation_flag is not None:
                logs.log(dtype=dtype, expectation_result=expectation_result)
                logs.average("expectation_result")
        logs.dump()
        return logs