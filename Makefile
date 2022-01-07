GPUNAME=placeholder
SHELL:=/bin/bash

all: qibo qibojit_gpu libraries

qibo: qibo_single qibo_double

libraries: libraries_single libraries_double

qibo_single:
	for nqubits in {3..24} ; do \
		for backend in numpy tensorflow qibotf qibojit ; do \
			filename=qibo_cpu.dat backend=$$backend precision=single nqubits=$$nqubits bash scripts/qibo_cpu.sh ; \
		done \
	done
	for nqubits in {3..26} ; do \
		for backend in tensorflow qibotf qibojit ; do \
			filename=qibo_gpu.dat backend=$$backend precision=single nqubits=$$nqubits bash scripts/qibo_gpu.sh ; \
		done \
	done

qibo_double:
	for nqubits in {3..23} ; do \
		for backend in numpy tensorflow qibotf qibojit ; do \
			filename=qibo_cpu.dat backend=$$backend precision=double nqubits=$$nqubits bash scripts/qibo_cpu.sh ; \
		done \
	done
	for nqubits in {3..25} ; do \
		for backend in tensorflow qibotf qibojit ; do \
			filename=qibo_gpu.dat backend=$$backend precision=double nqubits=$$nqubits bash scripts/qibo_gpu.sh ; \
		done \
	done

qibojit_gpu:
	for nqubits in {3..26} ; do \
		filename=qibojit_$(GPUNAME).dat backend=qibojit precision=single nqubits=$$nqubits bash scripts/qibo_gpu.sh ; \
	done
	for nqubits in {3..25} ; do \
		filename=qibojit_$(GPUNAME).dat backend=qibojit precision=double nqubits=$$nqubits bash scripts/qibo_gpu.sh ; \
	done

libraries_single:
	for nqubits in {3..24} ; do \
		for backend in qibo qiskit qsim qulacs projectq hybridq ; do \
			filename=library_cpu.dat library=$$backend precision=single nqubits=$$nqubits bash scripts/library_cpu.sh ; \
		done \
	done
	for nqubits in {3..26} ; do \
		for backend in qibo qiskit-gpu qsim-gpu qsim-cuquantum qulacs-gpu qcgpu hybridq-gpu ; do \
			filename=library_gpu.dat library=$$backend precision=single nqubits=$$nqubits bash scripts/library_gpu.sh ; \
		done \
	done

libraries_double:
	for nqubits in {3..23} ; do \
		for backend in qibo qiskit qulacs projectq hybridq ; do \
			filename=library_cpu.dat library=$$backend precision=double nqubits=$$nqubits bash scripts/library_cpu.sh ; \
		done \
	done
	for nqubits in {3..25} ; do \
		for backend in qibo qiskit-gpu qulacs-gpu ; do \
			filename=library_gpu.dat library=$$backend precision=double nqubits=$$nqubits bash scripts/library_gpu.sh ; \
		done \
	done

clean:
	rm *.dat plots/*.pdf
