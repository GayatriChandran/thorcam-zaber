#!/usr/bin/env python

"""
To control Zaber + Thorcam and get stage position-vs-BFP image data. From this we can estimate the incident angle corresponding to each position of the stage. 

Gayatri 09/2024

"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from skimage.transform import AffineTransform, warp
from skimage.util import img_as_float


if __name__ == "__main__":
    
    # Load data
    positions = np.loadtxt('translation_array.csv')
    imgdata = np.load('air-07-21-2025-hwp-2.npy')                                      
    n_frames = np.shape(imgdata)[2]
    
    intensities = np.zeros(n_frames, dtype=float)

    ###

    # Define center and angle
    sample = img_as_float(np.maximum(imgdata[:,:,2], imgdata[:,:,80]))

    # Step 1: Draw a line to define angle and center
    fig, ax = plt.subplots()
    ax.imshow(sample, cmap='gray')
    plt.title("Click two points to define a rotated crop")
    pts = plt.ginput(1)
    plt.close()

    # Step 2: Compute angle and center
    print(pts)
    (x,y) = pts[0]
    print(x,y)
    # print(center[0])
    angle = 10  # degrees

    # Create transform: rotation around center
    # Rotate around center (cx, cy)
    t1 = AffineTransform(translation=(-x,-y))               # move center to origin
    t2 = AffineTransform(rotation=np.deg2rad(angle))       # rotate
    t3 = AffineTransform(translation=(x,y))                 # move center back
        
    total_tform = t1 + t2 + t3

    ###    

    for frame in range(n_frames):
        cropped_image = warp(imgdata[:, :, frame], total_tform.inverse)
        region = cropped_image[20:900, 750:900]
        # mean_val = np.mean(region)
        # std_val = np.std(region)
        # print(mean_val, std_val)
        intensities[frame] = np.sum(region[region > 0.05])
        
    data = np.column_stack((np.round(positions, 2), intensities))
    df = pd.DataFrame({'Stage': data[:, 0], 'Intensity': data[:, 1]})
    file_name = 'air-07-21-2025-hwp-2-intensities.csv'
    df.to_csv(file_name, index=False)





