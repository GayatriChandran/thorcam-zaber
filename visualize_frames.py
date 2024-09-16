#!/usr/bin/env python

"""
To control Zaber + Thorcam and get stage position-vs-BFP image data. From this we can estimate the incident angle corresponding to each position of the stage. 

Gayatri 09/2024

"""

import numpy as np
import matplotlib.pyplot as plt
import skimage as ski

def visualize(img, mask):
    fig, ax = plt.subplots(ncols=2, figsize=(10, 5))
    ax[0].imshow(img)
    ax[0].set_title('Original')
    ax[0].set_axis_off()
    ax[1].imshow(mask)
    ax[1].set_title('Floating type')
    ax[1].set_axis_off()
    plt.show()

if __name__ == "__main__":
    
    # Load data
    positions = np.loadtxt('data/pos.csv')
    imgdata = np.load('data/water.npy')                                      
    n_frames = np.shape(imgdata)[2]
    intensities = np.zeros(n_frames, dtype=float)

    for frame in range(1,5):
        image = ski.util.img_as_float(imgdata[:,:,frame]/1023.00)
        visualize(imgdata[:,:,frame]/1023.00, image)