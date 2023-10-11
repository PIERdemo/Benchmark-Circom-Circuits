#!/usr/bin/python3.10

import json
import os
import tensorflow as tf
import numpy as np


def resize_image(image, height, width):
    """
    Resize an image to the given dimensions.
    :param image_path: Path to the image to resize.
    :param height: Height of the resized image.
    :param width: Width of the resized image.
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
    if width is None:
        width = height
    rimg =  np.random.randint(0, 256, size=(height, width, 3), dtype=np.uint8)
    return rimg

def generate_resize_input(output_path, f_height,f_width,r_height,r_width):
    img = generate_random_image(f_height,f_width)
    rsz = resize_image(img,r_height,r_width)

    json_input = {'full_image':img.astype(str), 'resize_image':rsz.astype(str) }
    os.makedirs('input',exist_ok=True)
    with open(output_path, 'w') as outfile:
        json.dump(json_input, outfile)

