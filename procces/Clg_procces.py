import numpy as np
import cv2
import rasterio
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

def calculate_clg(nir_image, red_image):
    # Görüntüleri float32 formatına dönüştür
    nir = nir_image.astype(np.float32)
    green = red_image.astype(np.float32)
    
    # NDVI hesaplama
    clg = ((nir/green) - 1)
    
    # NDVI'yi -1 ile 1 arasında normalize et
    clg = np.clip(clg, -1, 1)
    
    return clg


def plot_clg(clg):
    plt.figure(figsize=(10, 10))
    plt.imshow(clg, cmap='RdYlGn')
    plt.colorbar(label='Clg')
    plt.title('Clg Haritası')
    plt.show()

# NDVI haritasını göster

def process_images_and_generate_clg(nir_image_path, red_image_path):
    with rasterio.open(nir_image_path) as nir_src:
        nir_band = nir_src.read(1)
def progress_image_sensoring():
    with rasterio.open(red_image_path) as red_src:
        red_band = red_src.read(1)

    ndvi_image = calculate_clg(nir_band, red_band)
    plot_clg(ndvi_image)

# Örnek kullanım
process_images_and_generate_clg('images/NIR.TIF', 'images/GREEN.TIF')

