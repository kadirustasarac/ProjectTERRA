import numpy as np
import cv2
import rasterio
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

def calculate_bai(nir_image, red_image):
    # Görüntüleri float32 formatına dönüştür
    nir = nir_image.astype(np.float32)
    red = red_image.astype(np.float32)
    
    # NDVI hesaplama
    bai = 1/(((red - 0.06) ** 2) + ((nir - 0.1) ** 2))
    
    # NDVI'yi -1 ile 1 arasında normalize et
    bai = np.clip(bai, -1, 1)
    
    return bai


def plot_bai(bai):
    plt.figure(figsize=(10, 10))
    plt.imshow(bai, cmap='RdYlGn_r')
    plt.colorbar(label='BAI')
    plt.title('BAI Haritası')
    plt.show()

# NDVI haritasını göster

def process_images_and_generate_bai(nir_image_path, red_image_path):
    with rasterio.open(nir_image_path) as nir_src:
        nir_band = nir_src.read(1)

    with rasterio.open(red_image_path) as red_src:
        red_band = red_src.read(1)

    ndvi_image = calculate_bai(nir_band, red_band)
    plot_bai(ndvi_image)

# Örnek kullanım
process_images_and_generate_bai('images/NIR.TIF', 'images/RED.TIF')
