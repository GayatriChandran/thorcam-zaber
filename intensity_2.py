import numpy as np
import matplotlib.pyplot as plt
from skimage.filters import threshold_otsu
from skimage import io as io

if __name__ == "__main__":
    
    # Load data
    imgdata = np.load('data/air.npy')                                      # Input end wavelength (nm)
    
    #Find Otsu threshold 
    thresh = threshold_otsu(imgdata[:,:,50])
    binary_image = imgdata[:,:,50] < thresh
    #Create a mask for the binary image where holes are 
    # white (1) and the rest is black (0)
    binary = np.zeros(shape=binary_image.shape)
    binary[binary_image] = 1
    io.imshow(binary)
    plt.axis('off')
    plt.title('Binary Image')
    plt.show()