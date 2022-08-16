#!/usr/bin/python3

from email.policy import default
from typing import Tuple
import os 
from numpy import linspace
from scipy.interpolate import barycentric_interpolate
import matplotlib.pyplot as plt
from collections import defaultdict
import exiftool

def focal_length(img_path: str) -> float:
    '''
    Get focal length of current image to add new key to focal length dictionary
    or increment value of present key 
    '''
    with exiftool.ExifToolHelper() as ET:
        metadata = ET.get_tag(filename=img_path, tag="FocalLength")

    if metadata is None:
        raise Exception("Make sure the file has metadata!")
    else:
        return metadata[10]


def interpolate(focal_len: list, focal_count: list, axis: linspace) -> list:
    '''
    Interpolate discrete data points
    '''

    return barycentric_interpolate(focal_len, focal_count, axis)
    

def plot(focal_dict: defaultdict) -> None:
    '''
    Parse dictionary and split key (focal length) and value (count)
    and plot key as x and value as y
    '''
    x_discrete = focal_dict.keys
    y_discrete = focal_dict.values

    x = linspace(min(x_discrete), max(x_discrete), num=100)
    interpolated_y = interpolate(x_discrete, y_discrete, x)

    plt.plot(x_discrete, y_discrete, "o", label="discrete")
    plt.plot(x, interpolated_y, label="barycentric interpolation")

    plt.legend()
    plt.show()


if __name__ == "__main__":
    path = "/mnt/f/My Drive/Photography/2022"

    focal_lengths = defaultdict(float)

    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            if name.endswith('.NEF'):
                foc_len = focal_length(os.path.join(root, name))
                focal_lengths[foc_len] += 1
    
    plot(focal_lengths)
    


