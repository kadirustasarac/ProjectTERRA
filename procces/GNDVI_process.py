'''
___________________

@author: tahacolak
___________________

******************************************************************************************************************************************
param. exp.: GNDVI, bitki sağlığını NDVI'ya benzer bir şekilde değerlendirir
             ancak kırmızı bant yerine yeşil bandı kullanır. Özellikle, su durumu
             ve klorofil içeriği için hassas olabilir.
******************************************************************************************************************************************

'''

import numpy as np
import cv2
import rasterio
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

def calculate_gndvi(nir_image, green_image):
    # Görüntüleri float32 formatına dönüştür
    nir = nir_image.astype(np.float32)
    green = green_image.astype(np.float32)
    
    # GNDVI hesaplama
    valOfGNDVI = (nir - green) / (nir + green)
    
    # GNDVI'yi -1 ile 1 arasında normalize et
    valOfGNDVI = np.clip(valOfGNDVI, -1, 1)
    
    return valOfGNDVI


def plot_gndvi(valOfGNDVI):
    plt.figure(figsize=(10, 10))
    plt.imshow(valOfGNDVI, cmap='RdYlGn')
    plt.colorbar(label='GNDVI')
    plt.title('GNDVI Haritası')
    plt.show()

# GNDVI haritasını göster
def process_images_and_generate_gndvi(nir_image_path, green_image_path):
    # NIR ve Green görüntülerini rasterio ile oku
    with rasterio.open(nir_image_path) as nir_src:
        nir_band = nir_src.read(1)

    with rasterio.open(green_image_path) as green_src:
        green_band = green_src.read(1)

    # GNDVI hesapla ve haritayı göster
    gndvi_image = calculate_gndvi(nir_band, green_band)
    plot_gndvi(gndvi_image)

# Örnek kullanım
process_images_and_generate_gndvi('images/NIR.TIF', 'images/GREEN.TIF')
