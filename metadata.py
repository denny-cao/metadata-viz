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
    - Dictionary of dictionaries to store metadata
'''

import os 
from numpy import linspace
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from collections import defaultdict
import exifread


class Metadata:
    def __init__(self):
        self.img_path = None
        self.x, self.y = [], []
        self.meta_dict = defaultdict(lambda: defaultdict(int))


    def update_img_path(self, img_path):
        self.img_path = img_path


    def interpolate(self) -> interp1d:
    
        '''
        Interpolate discrete data points
        '''
        
        interpolated_y = interp1d(self.x, self.y, kind='quadratic')

        x_new = linspace(min(self.x), max(self.x), num=100)
        
        return x_new, interpolated_y(x_new)


    def focal_length(self) -> int:
        
        '''
        Get focal length of current image to add new key to metadata dictionary
        or increment value of present key 
        '''

        with open(self.img_path, 'rb') as raw:
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
        
        pass

    def apertures(self) -> float:
        
        '''
        Get aperature of current image to add new key to metadata dictionary
        or increment value of present key
        '''

        with open(self.img_path, 'rb') as raw:
            tags = exifread.process_file(raw, stop_tag='ApertureValue')
            
            return tags['EXIF ApertureValue'].values[0]

    
    def plot(self) -> None:
        
        '''
        Parse dictionary and split key (metadata) and value (count)
        and plot key as x and value as y
        '''

        x_discrete, y_discrete = zip(*self.meta_dict['Focal Lengths'].items())
        x_discrete = list(int(x) for x in x_discrete)
        y_discrete = list(y_discrete)

        self.x, self.y = x_discrete, y_discrete
        x_new, y_smooth = self.interpolate()

        plt.plot(x_discrete, y_discrete, 'o', label='discrete')
        plt.plot(x_new, y_smooth, label='quadratic interpolation')

        plt.legend()
        plt.show()


def main() -> None:
    metadata = Metadata()
    path = '/mnt/f/My Drive/Photography/2022'

    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            if name.endswith('.NEF'):
                metadata.update_img_path(os.path.join(root, name))
                foc_len = metadata.focal_length()
                metadata.meta_dict['Focal Lengths'][foc_len] += 1

    metadata.plot()


if __name__ == '__main__':
    main()   



