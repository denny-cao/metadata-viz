#!/usr/bin/python3

'''
Extract metadata from raw files and visualize them to determine what lens to buy.
'''

'''
TODO: 
    - Add ability to save data to csv file
    - Improve interpolation
    - Add more metadata visualization
    - Somehow factor in date of image... See what I favored in the past vs now
    - Group similar focal legnths together to typical prime lens focal lengths
'''

import os 
from numpy import linspace
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from collections import defaultdict
import exifread


def focal_length(img_path: str) -> int:
    
    '''
    Get focal length of current image to add new key to focal length dictionary
    or increment value of present key 
    '''

    with open(img_path, 'rb') as raw:
        tags = exifread.process_file(raw, stop_tag='FocalLength')
        
        return tags['EXIF FocalLength'].values[0]


def round_focal(focal_len: int) -> int:
    
    '''
    Round focal length to nearest typical prime lens focal lengths
    using binary tree for O(log(log n))
    '''

    typical = {
        18: 0,
        24: 0,
        35: 0,
        55: 0,
        85: 0,
        105: 0,
        135: 0,
        200: 0,
        300: 0
    }

def interpolate(focal_len: list, focal_count: list) -> interp1d:
   
    '''
    Interpolate discrete data points
    '''
    
    interpolated_y = interp1d(focal_len, focal_count, kind='quadratic')

    x_new = linspace(min(focal_len), max(focal_len), num=100)
    return x_new, interpolated_y(x_new)

def plot(focal_dict: defaultdict) -> None:
    
    '''
    Parse dictionary and split key (focal length) and value (count)
    and plot key as x and value as y
    '''

    x_discrete, y_discrete = zip(*focal_dict.items())
    x_discrete = list(int(x) for x in x_discrete)
    y_discrete = list(y_discrete)

    x_new, y_smooth = interpolate(x_discrete, y_discrete)

    plt.plot(x_discrete, y_discrete, "o", label="discrete")
    plt.plot(x_new, y_smooth, label="quadratic interpolation")

    plt.legend()
    plt.show()


def main() -> None:
    path = "/mnt/f/My Drive/Photography/2022"

    focal_lengths = defaultdict(int)

    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            if name.endswith('.NEF'):
                foc_len = focal_length(os.path.join(root, name))
                focal_lengths[foc_len] += 1

    plot(focal_lengths)


if __name__ == "__main__":
    main()
    



