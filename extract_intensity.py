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

def visualize(img, mask):
    fig, ax = plt.subplots(ncols=2, figsize=(10, 5))
    ax[0].imshow(img)
    ax[0].set_title('Original')
    ax[0].set_axis_off()
    ax[1].imshow(mask)
    ax[1].set_title('Dilated mask')
    ax[1].set_axis_off()
    plt.show()

def doSomething(img):
    threshold1 = threshold_otsu(img)
    print('Otsu threshold : ', threshold1)
    thresh = 0.004
    binary = img > thresh
    dil_mask = multi_dil(binary,2)
    ero_mask = multi_ero(dil_mask,1)
    opened = opening(ero_mask)
    img_masked = np.ma.masked_array(img, ~opened)
    # visualize(img, binary)
    return img_masked, thresh

def doSomethingElse(img):
    im = img
    image_max = ndi.maximum_filter(im, size=10, mode='constant')
    coordinates = peak_local_max(image_max, min_distance=50, threshold_abs = 30, num_peaks = 1)

    # fig, axes = plt.subplots(1, 3, figsize=(8, 3), sharex=True, sharey=True)
    # ax = axes.ravel()
    # ax[0].imshow(im, cmap=plt.cm.gray)
    # ax[0].axis('off')
    # ax[0].set_title('Original')

    # ax[1].imshow(image_max, cmap=plt.cm.gray)
    # ax[1].axis('off')
    # ax[1].set_title('Maximum filter')

    # ax[2].imshow(im, cmap=plt.cm.gray)
    # ax[2].autoscale(False)
    # ax[2].plot(coordinates[:, 1], coordinates[:, 0], 'r.')
    # ax[2].axis('off')
    # ax[2].set_title('Peak local max')

    # fig.tight_layout()

    # plt.show()

    doWatershed(img, coordinates)

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

if __name__ == "__main__":
    
    # Load data
    positions = np.loadtxt('data/09-14-2024/pos-01.csv')
    imgdata = np.load('09-14-2024/')                                      
    n_frames = np.shape(imgdata)[2]
    intensities = np.zeros(n_frames, dtype=float)

    for frame in range(n_frames):
        # background = np.mean(restoration.rolling_ball(imgdata[:,:,frame]))
        background = 0.001

        image = ski.util.img_as_float(imgdata[:,:,frame]/1023.00)
        # print('Original max : ', np.max(imgdata[:,:,frame]))
        # print('Original min : ', np.min(imgdata[:,:,frame]))
        # print('Converted max : ', np.max(image))
        # print('Converted min : ', np.min(image))
        img_masked, thresh = doSomething(image)


        print('Pos = ', np.round(positions[frame], 2), ' , Sum = ', np.sum(img_masked[img_masked>background].compressed()))
        intensities[frame] = np.sum(img_masked[img_masked>background])
        # print(img_masked[img_masked>background].compressed())

    data = np.column_stack((np.round(positions, 2), intensities))
    df = pd.DataFrame({'Stage': data[:, 0], 'Intensity': data[:, 1]})
    file_name = 'data/09-14-2024-air-intensities_10.csv'
    df.to_csv(file_name, index=False)





