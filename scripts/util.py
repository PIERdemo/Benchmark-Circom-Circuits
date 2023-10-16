#!/usr/bin/env python3

from csv import DictWriter
import json
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf
import numpy as np
import random
import subprocess
import psutil
import re


def measure_command(command, time = True, memory = True):
    """
    Measure the time and memory usage of a specified command.

    :param command: The command to execute and measure.
    :param time: True if you want to measure time, False otherwise.
    :param memory: True if you want to measure memory usage, False otherwise.

    :return: A tuple containing the elapsed time (if time=True) and memory usage (if memory=True).
    """
    command = f'/usr/bin/time -p -f "%e %M" {command} > /dev/null'
    if memory:
        init_swap_used = psutil.swap_memory().used
        max_swap_used = init_swap_used
    
    process = subprocess.Popen(command, 
                               shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    
    if memory:
        while process.poll() is None:
            max_swap_used = max(max_swap_used, psutil.swap_memory().used)

    command_output = process.communicate()[1].decode('utf-8')
    t,mem = command_output.split('\n')[0].split(' ')
    t = float(t)

    if memory:
        swap = (max_swap_used-init_swap_used)/1024
        m = float(mem)+(swap if swap > 0 else 0)
    
    return t if time else None, m if memory else None


def generate_circuit(info, circuit_template, id = None):
    """
    Generate a circuit from a template
    :param info: dictionary with the information to replace in the template
    :param circuit_template: path to the template
    :param id: id of the circuit

    """
    out_circuit = circuit_template.split('/')[-1].split('.')[0]
    os.makedirs('circuits/benchmark',exist_ok=True)

    with open(circuit_template, 'r') as infile:
        circuit = infile.read()
        for k,v in info.items():
            circuit = circuit.replace(k, str(v))
        circuit = circuit.replace('//MAIN', '')
        
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
    os.makedirs('input',exist_ok=True)
    with open(output_path, 'w') as outfile:
        json.dump(json_input, outfile)
    

def extract_contraints(r1cs_file):
    infos = subprocess.check_output(f'snarkjs r1cs info {r1cs_file}',shell=True).decode('utf-8')
    return int(re.search(r'# of Constraints: (\d+)',infos).group(1))



def resize_image(image, height, width):
    """
    Resize an image to the given dimensions.
    :param image_path: Path to the image to resize.
    :param height: Height of the resized image.
    :param width: Width of the resized image.
    :return: the resized image.
    """
    original_height, original_width, _ = image.shape

    if (original_height-1) % (height-1) != 0 or (original_width-1) % (width-1) != 0:
        divisors_h = [v+1 for v in range(1, (original_height - 1)//2) if (original_height - 1) % v == 0]
        divisors_w = [v+1 for v in range(1, (original_width - 1)//2) if (original_width - 1) % v == 0]
        raise ValueError(f"The image cannot be resized to the given dimensions.\n The height must be one of this numbers: {divisors_h}\
                          \n The width must be one of this numbers: {divisors_w}")

    return (
        (
            tf.compat.v1.image.resize(
                image,
                [height, width],
                align_corners=True,
                method=tf.image.ResizeMethod.BILINEAR,
            )
        )
        .numpy()
        .round()
        .astype(np.uint8)
    )
    


def generate_random_image(height, width = None):
    """
    Generate a random image.
    :param height: Height of the image.
    :param width: Width of the image.
    :return: the random image.
    """
    if width is None:
        width = height
    rimg =  np.random.randint(0, 256, size=(height, width, 3), dtype=np.uint8)
    return rimg

def generate_resize_input(output_path, f_height,f_width,r_height,r_width):
    """
    Generate a random input that fits the cirtuit for the resize operation check.
    :param output_path: Path to the output file.
    :param f_height: Height of the full image.
    :param f_width: Width of the full image.
    :param r_height: Height of the resized image.
    :param r_width: Width of the resized image.
    """
    img = generate_random_image(f_height,f_width)
    rsz = resize_image(img,r_height,r_width)

    json_input = {'full_image':img.astype(str).tolist(), 'resize_image':rsz.astype(str).tolist() }
    os.makedirs('input',exist_ok=True)
    with open(output_path, 'w') as outfile:
        json.dump(json_input, outfile)


if __name__ == '__main__':
    raise ValueError('This script is not meant to be executed directly')