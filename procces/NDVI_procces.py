import numpy as np
import cv2
import rasterio
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

def calculate_ndvi(nir_image, red_image):
    # Görüntüleri float32 formatına dönüştür
    nir = nir_image.astype(np.float32)
    red = red_image.astype(np.float32)
    
    # NDVI hesaplama
    ndvi = (nir - red) / (nir + red)
    
    # NDVI'yi -1 ile 1 arasında normalize et
    ndvi = np.clip(ndvi, -1, 1)
    
    return ndvi


def plot_ndvi(ndvi):
    plt.figure(figsize=(10, 10))
    plt.imshow(ndvi, cmap='RdYlGn')
    plt.colorbar(label='NDVI')
    plt.title('NDVI Haritası')
    plt.show()

# NDVI haritasını göster

def process_images_and_generate_ndvi(nir_image_path, red_image_path):
    with rasterio.open(nir_image_path) as nir_src:
        nir_band = nir_src.read(1)

    with rasterio.open(red_image_path) as red_src:
        red_band = red_src.read(1)

    ndvi_image = calculate_ndvi(nir_band, red_band)

# Örnek kullanım
process_images_and_generate_ndvi('images/final/nir.TIF', 'images/final/red.TIF')

