import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the image (as before)
image = cv2.imread('C:\Users\W10\Desktop\hps.png')

# Simulate NIR and RED channels (as before)
nir_channel = image[:, :, 2].astype(float)  # Simulated NIR channel
red_channel = image[:, :, 0].astype(float)  # Simulated RED channel

# Calculate NDVI (as before)
ndvi = (nir_channel - red_channel) / (nir_channel + red_channel + 1e-10)

# Normalize NDVI for visualization
ndvi_normalized = cv2.normalize(ndvi, None, 0, 1, cv2.NORM_MINMAX)

# Flatten the NDVI array and create a DataFrame
ndvi_flat = ndvi.flatten()
df = pd.DataFrame({'NDVI': ndvi_flat})

# Write the NDVI data to a CSV file
csv_file = 'ndvi_data.csv'
df.to_csv(csv_file, index=False)
print(f"NDVI data written to {csv_file}")

# Read the NDVI data back from the CSV file
df_read = pd.read_csv(csv_file)
ndvi_read = df_read['NDVI'].values.reshape(ndvi.shape)

# Display the NDVI read from CSV to verify
plt.imshow(ndvi_read, cmap='RdYlGn')
plt.colorbar()
plt.title('NDVI (from CSV)')
plt.show()