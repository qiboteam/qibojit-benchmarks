"""Benchmark scripts."""
import time
from benchmarks.logger import JsonLogger

def circuit_benchmark(nqubits, backend, circuit_name, circuit_options=None,
                      nreps=1, nshots=None, transfer=False,
                      precision="double", memory=None, threading=None,
                      filename=None, platform=None):
    """Runs benchmark for different circuit types.

    See ``benchmarks/main.py`` for documentation of each argument.
    """
    if backend == "qibojit" and threading is not None:
        from benchmarks.utils import select_numba_threading
        threading = select_numba_threading(threading)

    if backend in {"qibotf", "tensorflow"} and memory is not None:
        from benchmarks.utils import limit_gpu_memory
        memory = limit_gpu_memory(memory)

    logs = JsonLogger(filename)
    logs.log(nqubits=nqubits, nreps=nreps, nshots=nshots, transfer=transfer,
             numba_threading=threading, gpu_memory=memory)

    start_time = time.time()
    import qibo
    logs.log(import_time=time.time() - start_time)

    qibo.set_backend(backend=backend, platform=platform)
    qibo.set_precision(precision)
    logs.log(backend=qibo.get_backend(),
             platform=qibo.K.get_platform(),
             precision=qibo.get_precision(),
             device=qibo.get_device(),
             version=qibo.__version__)

    from benchmarks import circuits
    gates = circuits.get(circuit_name, nqubits, circuit_options, qibo=True)
    logs.log(circuit=circuit_name, circuit_options=str(gates))
    start_time = time.time()
    circuit = qibo.models.Circuit(nqubits)
    circuit.add(gates)
    if nshots is not None:
        # add measurement gates
        circuit.add(qibo.gates.M(*range(nqubits)))
    logs.log(creation_time=time.time() - start_time)

    start_time = time.time()
    result = circuit(nshots=nshots)
    logs.log(dry_run_time=time.time() - start_time)
    start_time = time.time()
    if transfer:
        result = result.numpy()
    logs.log(dry_run_transfer_time=time.time() - start_time)
    dtype = str(result.dtype)
    del(result)

    simulation_times, transfer_times = [], []
    for _ in range(nreps):
        start_time = time.time()
        result = circuit(nshots=nshots)
        simulation_times.append(time.time() - start_time)
        start_time = time.time()
        if transfer:
            result = result.numpy()
        transfer_times.append(time.time() - start_time)
        del(result)

    logs.log(dtype=dtype, simulation_times=simulation_times,
             transfer_times=transfer_times)
    logs.average("simulation_times")
    logs.average("transfer_times")

    if nshots is not None:
        result = circuit(nshots=nshots)
        start_time = time.time()
        freqs = result.frequencies()
        logs.log(measurement_time=time.time() - start_time)
        del result
    else:
        logs.log(measurement_time=0)
        logs.dump()

    return logs


def library_benchmark(nqubits, library, circuit_name, circuit_options=None,
                      library_options=None, precision=None, nreps=1,
                      filename=None):
    """Runs benchmark for different quantum simulation libraries.

    See ``benchmarks/compare.py`` for documentation of each argument.
    """
    logs = JsonLogger(filename)
    logs.log(nqubits=nqubits, nreps=nreps)

    start_time = time.time()
    from benchmarks import libraries
    backend = libraries.get(library, library_options)
    logs.log(import_time=time.time() - start_time)
    logs.log(library_options=library_options)
    if precision is not None:
        backend.set_precision(precision)

    logs.log(library=backend.name,
             precision=backend.get_precision(),
             device=backend.get_device(),
             version=backend.__version__)

    from benchmarks import circuits
    gates = circuits.get(circuit_name, nqubits, circuit_options)
    logs.log(circuit=circuit_name, circuit_options=str(gates))
    start_time = time.time()
    circuit = backend.from_qasm(gates.to_qasm())
    logs.log(creation_time=time.time() - start_time)

    start_time = time.time()
    result = backend(circuit)
    logs.log(dry_run_time=time.time() - start_time)
    dtype = str(result.dtype)
    del(result)

    simulation_times = []
    for _ in range(nreps):
        start_time = time.time()
        result = backend(circuit)
        simulation_times.append(time.time() - start_time)
        del(result)

    logs.log(dtype=dtype, simulation_times=simulation_times)
    logs.average("simulation_times")
    logs.dump()
    return logs

def qibotn_benchmark(nqubits, library, circuit_name, circuit_options=None,
                      library_options=None, precision=None, nreps=1,
                      filename=None):
    """Runs benchmark for different quantum simulation libraries.

    See ``benchmarks/compare.py`` for documentation of each argument.
    """
    from mpi4py import MPI  # this line initializes MPI
    import numpy as np
    import cupy as cp

    try:
    # Try to create MPI.COMM_WORLD
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()
    except MPI.Exception:
    # MPI is not available or not launched deliberately, set rank to 0
        rank = 0        

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
    result = backend(circuit)
    if rank == 0:
        logs.log(dry_run_time=time.time() - start_time)
    dtype = str(result.dtype)
    del(result)

    if rank == 0:   
        simulation_times = []
        if backend.expectation_flag is not None:
                expectation_result = [] 
    for _ in range(nreps):
        if rank == 0:
            start_time = time.time()
        result = backend(circuit)
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
        
    if rank == 0:
        logs.log(dtype=dtype, simulation_times=simulation_times)
        logs.average("simulation_times")
        if backend.expectation_flag is not None:
                logs.log(dtype=dtype, expectation_result=expectation_result)
                logs.average("expectation_result")
        logs.dump()
        return logs


def evolution_benchmark(nqubits, dt, solver, backend, platform=None,
                        nreps=1, precision="double", dense=False,
                        filename=None):
    """Performs adiabatic evolution with critical TFIM as the hard Hamiltonian."""
    logs = JsonLogger(filename)
    logs.log(nqubits=nqubits, nreps=nreps, dt=dt, solver=solver, dense=dense)

    start_time = time.time()
    import qibo
    logs.log(import_time=time.time() - start_time)

    qibo.set_backend(backend=backend, platform=platform)
    qibo.set_precision(precision)
    logs.log(backend=qibo.get_backend(),
             platform=qibo.K.get_platform(),
             precision=qibo.get_precision(),
             device=qibo.get_device(),
             threads=qibo.get_threads(),
             version=qibo.__version__)

    from qibo import hamiltonians, models
    start_time = time.time()
    h0 = hamiltonians.X(nqubits, dense=dense)
    h1 = hamiltonians.TFIM(nqubits, h=1.0, dense=dense)
    logs.log(hamiltonian_creation_time=time.time() - start_time)

    start_time = time.time()
    evolution = models.AdiabaticEvolution(h0, h1, lambda t: t, dt=dt, solver=solver)
    logs.log(evolution_creation_time=time.time() - start_time)

    start_time = time.time()
    result = evolution(final_time=1.0)
    logs.log(dry_run_time=time.time() - start_time)
    dtype = str(result.dtype)
    del(result)

    simulation_times = []
    for _ in range(nreps):
        start_time = time.time()
        result = evolution(final_time=1.0)
        simulation_times.append(time.time() - start_time)
    logs.log(dtype=dtype, simulation_times=simulation_times)
    logs.average("simulation_times")
    logs.dump()
    return logs
