#!/usr/bin/env python

"""
To control Zaber + Thorcam and get stage position-vs-BFP image data. From this we can estimate the incident angle corresponding to each position of the stage. 

Gayatri 09/2024

"""

import numpy as np
import matplotlib.pyplot as plt
import tifffile as tf

if __name__ == "__main__":
    
    # Load data
    imgdata = np.load('air.npy')                                      # Input end wavelength (nm)
    n_frames = np.shape(imgdata)[2]
    print(n_frames)
    # Visualize

    fig, (ax1) = plt.subplots(1, 1, figsize=(8, 8))
    ax = plt.gca()
    im = ax1.imshow(imgdata[:,:,90], cmap='viridis',aspect='equal')
    plt.title('Image')
    plt.show()


