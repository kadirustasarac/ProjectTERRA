import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

'''
Coded by @tahacolak

'''
image = cv2.imread('ndviExample.jpeg')

# Simulate NIR and RED channels (as before)
nir_channel = image[:, :, 2].astype(float)  # Near InfraRed Channel
red_channel = image[:, :, 0].astype(float)  # Red Channel

# Calculate NDVI via Formula
ndvi = (nir_channel - red_channel) / (nir_channel + red_channel + 1e-10)  # added 1e+10 to dividing correctly (0 cannot be denominator)


# Normalize NDVI for visualization
ndvi_normalized = cv2.normalize(ndvi, None, 0, 1, cv2.NORM_MINMAX)

# Flatten the NDVI array and create a DataFrame
ndvi_flat = ndvi.flatten()
data_frame = pd.DataFrame({'NDVI_TahaColak': ndvi_flat})

# Write the NDVI data to a CSV file
csv_file = 'ndvi_data.csv'
data_frame.to_csv(csv_file, index=False)
print(f"NDVI data written to {csv_file}")

# Read back NDVI datas from the file
df_read = pd.read_csv(csv_file)
ndvi_read = df_read['NDVI_TahaColak'].values.reshape(ndvi.shape)

# Display the NDVI read from CSV to verify
plt.imshow(ndvi_read, cmap='RdYlGn')
plt.colorbar()
plt.title('NDVI (from CSV)')
plt.show()