'''
___________________

@author: tahacolak
___________________

******************************************************************************************************************************************
param. exp.: NDRE, kırmızı kenar spektral bandını kullanarak bitki sağlığını ve klorofil seviyelerini ölçer. 
             Kırmızı kenar bandı, özellikle olgun bitkilerde kullanışlıdır.

******************************************************************************************************************************************

'''

import numpy as np
import cv2
import rasterio
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

def calculate_ndre(nir_image, red_edge_image):
    # Görüntüleri float32 formatına dönüştür
    nir = nir_image.astype(np.float32)
    red_edge = red_edge_image.astype(np.float32)
    
    # NDRE hesaplama
    valOfNDRE = (nir - red_edge) / (nir + red_edge)
    
    # NDRE'yi -1 ile 1 arasında normalize et
    valOfNDRE = np.clip(valOfNDRE, -1, 1)
    
    return valOfNDRE

def plot_ndre(valOfNDRE):
    plt.figure(figsize=(10, 10))
    plt.imshow(valOfNDRE, cmap='RdYlGn')
    plt.colorbar(label='NDRE')
    plt.title('NDRE Haritası')
    plt.show()

# NDRE haritasını göster
def process_images_and_generate_ndre(nir_image_path, red_edge_image_path):
    # NIR ve Red Edge görüntülerini rasterio ile oku
    with rasterio.open(nir_image_path) as nir_src:
        nir_band = nir_src.read(1)

    with rasterio.open(red_edge_image_path) as red_edge_src:
        red_edge_band = red_edge_src.read(1)

    # NDRE hesapla ve haritayı göster
    ndre_image = calculate_ndre(nir_band, red_edge_band)
    plot_ndre(ndre_image)

# Örnek kullanım
process_images_and_generate_ndre('images/NIR.TIF', 'images/REG.TIF')
