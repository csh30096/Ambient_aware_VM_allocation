# Ambient_aware_VM_allocation

Ambient-aware VM allocation technique for virtualized heterogeneous data center

## Description
1. It needs local server at least two. one for global manager, one for local.
2. It needs to know maximum frequency of CPUs.
3. It needs to know LLC MPKI of the VMs.
4. Virtual machine configurations are in VM_list file
5. Physical machine configurations are in PM_list file.

- Global manager sorts VM_list and start the VMs. Global manager also sorts PM_list and allocate VMs to PMs
- Local manager calculate ambient-aware dynamic computing capability of PMs. Ambient-aware dynamic computing capability is related to the performance of a PM.


## How to use
1. Set the one physical machine to global manager
2. Setting the information of the VMs and PMs.
2. (In global manager machine) python global_allocator.py

## Dependencies
- Python 3.7
- gcc 5.4.0
- virt-manager 1.3.2
- QEMU emulater 2.6.2

## Needs
- real-time ambient thermometer
