'''
___________________

@author: tahacolak
___________________

******************************************************************************************************************************************
param. exp.: EVI (Enhanced Vegetation Index), NDVI'ye benzer ancak atmosferik etkileri ve toprağın yansıma etkilerini daha iyi dengeleyen
             bir indekstir. Bu sayede bitki sağlığını daha doğru bir şekilde ölçer. EVI formülü, NIR, Red ve Blue bantlarını kullanır. 
             L toprak düzeltme katsayısıdır, genellikle 1 kullanılır. C1 ve C2 ise atmosferik direnç katsayılarıdır, tipik olarak C1=6.0, 
             C2=7.5 olarak kullanılır.

******************************************************************************************************************************************

'''

import numpy as np
import cv2
import rasterio
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

def calculate_evi(nir_image, red_image, blue_image, L=1, C1=6, C2=7.5):
    # Görüntüleri float32 formatına dönüştür
    nir = nir_image.astype(np.float32)
    red = red_image.astype(np.float32)
    blue = blue_image.astype(np.float32)
    
    # EVI hesaplama
    valOfEVI = 2.5 * ((nir - red) / (nir + C1 * red - C2 * blue + L))
    
    # EVI'yi -1 ile 1 arasında normalize et
    valOfEVI = np.clip(valOfEVI, -1, 1)
    
    return valOfEVI


def plot_evi(valOfEVI):
    plt.figure(figsize=(10, 10))
    plt.imshow(valOfEVI, cmap='RdYlGn')
    plt.colorbar(label='EVI')
    plt.title('EVI Haritası')
    plt.show()

# EVI haritasını göster
def process_images_and_generate_evi(nir_image_path, red_image_path, blue_image_path):
    # NIR, Red ve Blue görüntülerini rasterio ile oku
    with rasterio.open(nir_image_path) as nir_src:
        nir_band = nir_src.read(1)

    with rasterio.open(red_image_path) as red_src:
        red_band = red_src.read(1)
        
    with rasterio.open(blue_image_path) as blue_src:
        blue_band=blue_src.read(1)

     # NDRE hesapla ve haritayı göster
    evi_image = calculate_evi(nir_band, red_band,blue_band)
    plot_evi(evi_image)
    
process_images_and_generate_evi('images/NIR.TIF', 'images/REG.TIF')