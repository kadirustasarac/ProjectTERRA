import numpy as np
import cv2
import rasterio
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

def calculate_ndwi(nir_image, green_image):
    # Görüntüleri float32 formatına dönüştür
    nir = nir_image.astype(np.float32)
    green = green_image.astype(np.float32)
    
    # NDVI hesaplama
    ndwi = (green - nir) / (green + nir)
    
    # NDVI'yi -1 ile 1 arasında normalize et
    ndwi = np.clip(ndwi, -1, 1)
    
    return ndwi


def plot_ndwi(ndwi):
    colors = [(0.6, 0.3, 0.2), (0.8, 0.9, 0.4), (0.2, 0.4, 1.0)]
    cmap = LinearSegmentedColormap.from_list("ndwi_cmap", colors, N=256)
    plt.figure(figsize=(10, 10))
    plt.imshow(ndwi, cmap=cmap)
    plt.colorbar(label='NDWI')
    plt.title('NDWI Haritası')
    plt.show()

# NDVI haritasını göster

def process_images_and_generate_ndwi(nir_image_path, green_image_path):
    with rasterio.open(nir_image_path) as nir_src:
        nir_band = nir_src.read(1)

    with rasterio.open(green_image_path) as green_src:
        green_band = green_src.read(1)

    ndwi_image = calculate_ndwi(nir_band, green_band)
    plot_ndwi(ndwi_image)

# Örnek kullanım
process_images_and_generate_ndwi('images/NIR.TIF', 'images/GREEN.TIF')

