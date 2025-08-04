import numpy as np
import tifffile

# Load your data
imgdata = np.load('air-08-01-2025-hwp-32.npy')  # shape: [H, W, N]

# Transpose to [N, H, W] — required for tifffile (Z-stack)
img_stack = np.transpose(imgdata, (2, 0, 1))

# Save as multi-page TIFF
tifffile.imwrite('air-08-01-2025-hwp-32.tiff', img_stack.astype(np.uint16))  # or np.uint8 depending on dtype
