import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""
Coded by @tahacolak
"""

original_image = cv2.imread('ndviExample.jpeg')

#variable called blankArea is trivial.

image_height, image_width, blankArea= original_image.shape

# Read the NDVI data from the CSV file
csv_file = 'ndvi_data.csv'
df_read = pd.read_csv(csv_file)
ndvi_read = df_read['NDVI'].values

# Reshape the NDVI array to match the original image dimensions
ndvi_matrix = ndvi_read.reshape((image_height, image_width))


k = 255.0 #k cons. for reverse formulating

#Formula Reversing
nir_channel = (1 + ndvi_matrix) * k / 2
red_channel = (1 - ndvi_matrix) * k / 2


blue_channel = np.zeros_like(nir_channel)

#Combining three-channels image
image_reconstructed = np.stack((red_channel, blue_channel, nir_channel), axis=-1).astype(np.uint8)

#Save:
output_image = 'reconstructed_image.jpeg'
cv2.imwrite(output_image, image_reconstructed)
print(f"Reconstructed image saved as {output_image}")

#Show:
plt.imshow(cv2.cvtColor(image_reconstructed, cv2.COLOR_BGR2RGB))
plt.title('Reconstructed Image from NDVI-TUSMEC_TahaColak')
plt.show()
