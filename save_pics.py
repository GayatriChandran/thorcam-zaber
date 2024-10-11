#!/usr/bin/env python

"""
To control Zaber + Thorcam and get stage position-vs-BFP image data. From this we can estimate the incident angle corresponding to each position of the stage. 

Gayatri 09/2024

"""

import numpy as np
import skimage as ski
from tifffile import imwrite

if __name__ == "__main__":
    
    # Load data
    positions = np.loadtxt('data/09-14-2024/pos-01.csv')
    file_name = 'data/09-14-2024/water-09-14-2024-06.npy'
    imgdata = np.load(file_name)                                      
    n_frames = np.shape(imgdata)[2]


    for frame in range(n_frames):
        
        # image = ski.util.img_as_float(imgdata[:,:,frame]/1022.00)
        fn = file_name.rsplit('.npy')[0]+str(frame)+'.tif'
        imwrite(fn, imgdata[:,:,frame], imagej=True)







