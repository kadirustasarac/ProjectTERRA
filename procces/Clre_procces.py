import numpy as np
import cv2
import rasterio
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

def calculate_clre(nir_image, red_image):
    # Görüntüleri float32 formatına dönüştür
    nir = nir_image.astype(np.float32)
    red = red_image.astype(np.float32)
    
    # NDVI hesaplama
    clre = ((nir/red) - 1)
    
    # NDVI'yi -1 ile 1 arasında normalize et
    clre = np.clip(clre, -1, 1)
    
    return clre


def plot_clre(clre):
    plt.figure(figsize=(10, 10))
    plt.imshow(clre, cmap='RdYlGn')
    plt.colorbar(label='Clre')
    plt.title('Clre Haritası')
    plt.show()

# NDVI haritasını göster

def process_images_and_generate_clre(nir_image_path, red_image_path):
    with rasterio.open(nir_image_path) as nir_src:
        nir_band = nir_src.read(1)

    with rasterio.open(red_image_path) as red_src:
        red_band = red_src.read(1)

    ndvi_image = calculate_clre(nir_band, red_band)
    plot_clre(ndvi_image)

# Örnek kullanım
process_images_and_generate_clre('images/NIR.TIF', 'images/REG.TIF')

