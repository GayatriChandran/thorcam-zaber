#!/usr/bin/env python

"""
To control Zaber + Thorcam and get stage position-vs-BFP image data. From this we can estimate the incident angle corresponding to each position of the stage. 

Gayatri 09/2024

"""

import numpy as np
import matplotlib.pyplot as plt
import skimage as ski
from skimage import draw, io
from skimage.util import img_as_float
from skimage.draw import rectangle

from skimage.transform import AffineTransform, warp




def visualize(img, f, cropped):

    data_1d = cropped.ravel() # or data_2d.flatten() or np.reshape(data_2d, -1)
    plt.hist(data_1d, bins=200, alpha=0.7) # Plot the histogram
    plt.show()

    fig, ax = plt.subplots(ncols=2,figsize=(8, 8))
    ax[0].imshow(img)
    ax[0].set_title('Frame # '+str(f))
    ax[1].imshow(cropped)
    ax[1].set_title('Cropped')
    plt.show()
    

if __name__ == "__main__":
    
    # Load data
    positions = np.loadtxt('translation_array.csv')
    imgdata = np.load('air-07-21-2025-hwp-48.npy')                                      
    n_frames = np.shape(imgdata)[2]
    intensities = np.zeros(n_frames, dtype=float)
    # print('No. of frames : ', n_frames)
    selected_frames = [48,50,53]
    # selected_frames = [5]
    #####
    # Define center and angle
    sample = img_as_float(np.maximum(imgdata[:,:,2], imgdata[:,:,80]))

    # Step 1: Draw a line to define angle and center
    fig, ax = plt.subplots()
    ax.imshow(sample, cmap='gray')
    plt.title("Click two points to define a rotated crop")
    pts = plt.ginput(1)
    plt.close()

    # Step 2: Compute angle and center
    print('Center : ', pts)
    (x,y) = pts[0]

    # x = 818.85
    # y = 403.91
    print(x,y)
    # print(center[0])
    angle = 10  # degrees

    # Create transform: rotation around center
    # Rotate around center (cx, cy)
    t1 = AffineTransform(translation=(-x,-y))               # move center to origin
    t2 = AffineTransform(rotation=np.deg2rad(angle))       # rotate
    t3 = AffineTransform(translation=(x,y))                 # move center back
        
    total_tform = t1 + t2 + t3

    #####
    for frame in selected_frames:
        # Crop axis-aligned rectangle around the center in rotated image
        
        cropped_image = warp(imgdata[:, :, frame], total_tform.inverse)
        visualize(imgdata[:,:,frame], frame, cropped_image[0:900,750:900])