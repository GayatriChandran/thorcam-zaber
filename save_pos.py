#!/usr/bin/env python

"""
Save a list of stage positions as csv.
Gayatri 01/2025

"""

import numpy as np
import csv

# Define start and end positions
start_pos = 2.5  # Input start wavelength (nm) for sweep
end_pos = 7.5    # Input end wavelength (nm)

# Create the translation array
translation = np.arange(start_pos, end_pos, 0.05)

# Save the array as a CSV file
output_filename = "translation_array_2.csv"

# Save using the CSV writer
with open(output_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    for value in translation:
        writer.writerow([value])

print(f"Translation array saved as {output_filename}.")