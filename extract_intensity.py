#!/usr/bin/env python

"""
To control Zaber + Thorcam and get stage position-vs-BFP image data. From this we can estimate the incident angle corresponding to each position of the stage. 

Gayatri 09/2024

"""

import numpy as np
import pandas as pd
from skimage.filters import threshold_otsu
import matplotlib.pyplot as plt
from scipy import ndimage as ndi
from skimage import img_as_float
from skimage.feature import peak_local_max
from skimage import util, filters, color
from skimage.segmentation import watershed
import skimage as ski
from skimage.morphology import erosion, dilation, opening, closing
from skimage import data, restoration, util
from scipy.ndimage import maximum_filter
from skimage.draw import disk

def visualize(img, mask):
    fig, ax = plt.subplots(ncols=2, figsize=(10, 5))
    ax[0].imshow(img)
    ax[0].set_title('Original')
    ax[0].set_axis_off()
    ax[1].imshow(mask)
    ax[1].set_title('Dilated mask')
    ax[1].set_axis_off()
    plt.show()

def doSomething(img, coordinates):
    # print('Found it !')
    # threshold1 = threshold_otsu(img)
    # print('Otsu threshold : ', threshold1)
    # thresh = 0.004
    # Define the ROI radius
    roi_radius = 20
    mask = np.zeros_like(image, dtype=bool)
    rr, cc = disk(coordinates[0], roi_radius)
    mask[rr, cc] = True

    # Extract the ROI from the image
    binary = img[mask]

    # binary = img > thresh
    # dil_mask = multi_dil(binary,2)
    # ero_mask = multi_ero(dil_mask,1)
    # opened = opening(ero_mask)
    # img_masked = np.ma.masked_array(img, ~binary)
    # visualize(img, mask)
    return binary

def doSomethingElse(img):
    print('Lost it !')
    roi_radius = 20
    mask = np.zeros_like(image, dtype=bool)
    rr, cc = disk([500, 500], roi_radius)
    mask[rr, cc] = True
    binary = img[mask]
    # visualize(img, mask)
    return binary

def doWatershed(img, seeds):
    
    distance = ndi.distance_transform_edt(img)

    local_max_coords = ski.feature.peak_local_max(distance, min_distance=500, exclude_border=False)
    local_max_mask = np.zeros(distance.shape, dtype=bool)
    local_max_mask[tuple(local_max_coords.T)] = True
    markers = ski.measure.label(local_max_mask)

    segmented_img = ski.segmentation.watershed(-distance, markers, mask=img)

    fig, ax = plt.subplots(ncols=2, figsize=(10, 5))
    ax[0].imshow(img, cmap='gray')
    ax[0].set_title('Overlapping nuclei')
    ax[0].set_axis_off()
    ax[1].imshow(ski.color.label2rgb(segmented_img, bg_label=0))
    ax[1].set_title('Segmented nuclei')
    ax[1].set_axis_off()
    plt.show()

def multi_dil(im,num):
    for i in range(num):
        im = dilation(im)
    return im

def multi_ero(im,num):
    for i in range(num):
        im = erosion(im)
    return im

def visualize_peaks(img,peaks):
    fig, ax = plt.subplots(ncols=1, figsize=(5, 5))
    ax.imshow(img)
    ax.scatter(peaks[:,1], peaks[:,0],c='r')
    ax.set_title('Image with detected peaks')
    # ax.set_axis_off()
    plt.show()

def find_peaks_2d(data, min_distance=50):
    """Finds 2D peaks in a given array."""
    coordinates = peak_local_max(data, min_distance=min_distance, num_peaks=1, threshold_rel=0.5, exclude_border=(5,300))
    return coordinates


if __name__ == "__main__":
    
    # Load data
    positions = np.loadtxt('data/09-14-2024/pos-01.csv')
    imgdata = np.load('data/09-14-2024/water-09-14-2024-10.npy')                                      
    n_frames = np.shape(imgdata)[2]
    intensities = np.zeros(n_frames, dtype=float)

    for frame in range(n_frames):
        
        image = ski.util.img_as_float(imgdata[:,:,frame]/1022.00)
        peaks = find_peaks_2d(image)

        background = np.median(image) + 3*np.std(image)
        # threshold = 10*np.median(image)
        if len(peaks)>0:
            img_masked = doSomething(image, peaks)
        else:
            img_masked = doSomethingElse(image)


        print('Pos = ', np.round(positions[frame], 2), ' , Sum = ', np.sum(img_masked[img_masked>background]), ', Background = ', background)
        intensities[frame] = np.sum(img_masked[img_masked>background])
        # print(img_masked[img_masked>background].compressed())

    data = np.column_stack((np.round(positions, 2), intensities))
    df = pd.DataFrame({'Stage': data[:, 0], 'Intensity': data[:, 1]})
    file_name = 'data/09-14-2024/refl-water-09-14-2024-10.csv'
    df.to_csv(file_name, index=False)





