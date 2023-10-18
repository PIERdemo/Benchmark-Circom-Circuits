#!/usr/bin/python3.10

from scripts.util import append_to_csv, generate_circuit, generate_resize_input, measure_command, measure_pagefault_time_command, compute_input
from getpass import getpass
import os

def test_page_fault(input_size,password, circuit_name = 'resize_and_hash' ,pot_path = './powersoftau/28pot.ptau',verbose = True):
    if input_size % 2 != 0:
        HFULL, WFULL, HRESIZE, WRESIZE = input_size+2,input_size+2, int((input_size+1)/2)+1, int((input_size+1)/2)+1
    else:
        HFULL, WFULL, HRESIZE, WRESIZE = input_size+1,input_size+1, int(input_size/2)+1, int(input_size/2)+1

    generate_circuit({'HFULL': HFULL, 'WFULL':WFULL, 'HRESIZE':HRESIZE, 'WRESIZE' : WRESIZE },f'./circuits/base/{circuit_name}.circom',id=HFULL*WFULL)
    
    input_path = f'./input/input_{HFULL}_{WFULL}.json'
    generate_resize_input(input_path,HFULL, WFULL, HRESIZE, WRESIZE)
    
    if verbose:
        print(f'[{circuit_name}] (Input Size {HFULL}x{WFULL}x{3}) Start Test')
    
    measure_command(f'./scripts/compile_circuit.sh ./circuits/benchmark/{circuit_name}_{HFULL*WFULL}.circom {input_path} ',False,False)
    measure_command(f'./scripts/proving_system/setup_prover.sh {circuit_name}_{HFULL*WFULL} {pot_path}',False,False)
    
    LIMIT_MEM = 'cgexec -g memory:circom_test {}'
    time, pagefaults, cpu_percentage, swap_out = measure_pagefault_time_command(LIMIT_MEM.format(f'./scripts/proving_system/prover.sh {circuit_name}_{HFULL*WFULL}'),password = password)
    if verbose:
        print(f'[{circuit_name}] (Input Size {HFULL}x{WFULL}x{3}) Time: {time} seconds, Page Faults: {pagefaults}, CPU Percentage: {cpu_percentage}, Swap Out: {swap_out}')

    measure_command(f'./scripts/proving_system/verifier.sh {circuit_name}_{HFULL*WFULL}',False,False)
    return time, pagefaults, cpu_percentage, swap_out


if __name__ == '__main__':
    
    MAX_available_GB = int(2.56e8)
    MAX_GB = 1
    PASSWORD = getpass(f'[{os.getlogin()}] password: ')

    measure_command(f'echo "{PASSWORD}" | sudo -S cgset -r memory.limit_in_bytes={(MAX_available_GB)} circom_test',False,False)

    for used_gigabyte in [.25,.5,.75,MAX_GB]:
        input_size = compute_input(used_gigabyte)
        time,page_fault, cpu_percentage, swap_out = test_page_fault(input_size, password = PASSWORD)

        INFO = {'MAX RAM BYTE (GB)':MAX_available_GB,
                'NECESSARY BYTE (GB)':used_gigabyte,
                'INPUT SIZE':{f"{input_size}x{input_size}x3"},
                'TIME (s)':time,
                'PAGE FAULT':page_fault,
                'CPU PERCENTAGE':cpu_percentage,
                'SWAP OUT':swap_out}
        append_to_csv(INFO,'./benchmark_pagefaults.csv')