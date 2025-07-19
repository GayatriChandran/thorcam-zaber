#!/usr/bin/env python

"""
To control Zaber + Thorcam and get stage position-vs-BFP image data. From this we can estimate the incident angle corresponding to each position of the stage. 

Gayatri 09/2024

"""

import numpy as np
import matplotlib.pyplot as plt
import skimage as ski

def visualize(img, f, cropped):
    fig, ax = plt.subplots(ncols=2,figsize=(8, 5))
    ax[0].imshow(img)
    ax[0].set_title('Frame # '+str(f))
    ax[1].imshow(cropped)
    ax[1].set_title('Cropped')
    plt.show()

if __name__ == "__main__":
    
    # Load data
    positions = np.loadtxt('translation_array.csv')
    imgdata = np.load('air-07-18-2025-hwp-2-qwp-4.npy')                                      
    n_frames = np.shape(imgdata)[2]
    intensities = np.zeros(n_frames, dtype=float)
    print('No. of frames : ', n_frames)
    selected_frames = [10,25,50,75,80,98]
    for frame in selected_frames:
        cropped_image = ski.util.img_as_float(imgdata[:,770:985,frame]/1022.00)
        visualize(imgdata[:,:,frame]/1022.00, frame, cropped_image)