#!/usr/bin/env python3

from csv import DictWriter
import json
import os
import random
import subprocess
import psutil
import re

def measure_command(command):
    """
    Execute a command and measure the time and memory used
    :param command: command to execute
    :return: tuple with the time and memory used
    """
    command = f'/usr/bin/time -p -f "%e %M" {command} > /dev/null'
    init_swap_used = psutil.swap_memory().used
    max_swap_used = init_swap_used

    process = subprocess.Popen(command, 
                               shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    while process.poll() is None:
        max_swap_used = max(max_swap_used, psutil.swap_memory().used)

    command_output = process.communicate()[1].decode('utf-8')
    
    time,mem = command_output.split('\n')[0].split(' ')
    swap = (max_swap_used-init_swap_used)/1024
    
    
    return float(time),float(mem)+(swap if swap > 0 else 0)


def generate_circuit(info, circuit_template, id = None):
    """
    Generate a circuit from a template
    :param info: dictionary with the information to replace in the template
    :param circuit_template: path to the template
    :param id: id of the circuit

    """
    out_circuit = circuit_template.split('/')[-1].split('_')[0]
    os.makedirs('circuits/benchmark',exist_ok=True)

    with open(circuit_template, 'r') as infile:
        circuit = infile.read()
        for k,v in info.items():
            circuit = circuit.replace(k, str(v))
        
        id = f'_{id}' if id is not None else ''
        out_path = f'circuits/benchmark/{out_circuit}{id}.circom'
        with open(out_path, 'w') as outfile:
            outfile.write(circuit)
    return out_path


def append_to_csv(row,csv_path):
    """
    Append a row to a csv file if it exists, otherwise create it
    :param row: dictionary with the row to append
    :param csv_path: path to the csv file
    """
    with open(csv_path, 'a+', newline='') as csv_file:
        dict_writer = DictWriter(csv_file, fieldnames=list(row.keys()))
        if 0 == os.stat(csv_path).st_size:
            dict_writer.writeheader()
        dict_writer.writerow(row)


def generate_input(output_path, size):
    """
    Generate a random input for a circuit of a given size
    :param output_path: path to the output file
    :param size: size of the input
    """
    json_input = {'in':[str(random.randint(0, 255)) for _ in range(size)] }
    with open(output_path, 'w') as outfile:
        json.dump(json_input, outfile)
    

def extract_contraints(r1cs_file):
    infos = subprocess.check_output(f'snarkjs r1cs info {r1cs_file}',shell=True).decode('utf-8')
    return int(re.search(r'# of Constraints: (\d+)',infos).group(1))


if __name__ == '__main__':
    raise ValueError('This script is not meant to be executed directly')