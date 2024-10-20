import cv2
import matplotlib.pyplot as plt
import glob
import os
def getImages(path):
    images = []
    img_path = glob.glob(os.path.join(path,"*.JPG"))
    images = list(map(lambda img: cv2.imread(img),img_path))
    return images
def imageShow(imageList):
    fig, axes = plt.subplots(1,len(imageList),figsize=(15,6))
    for i,img in enumerate(imageList):
        rgb = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
        axes[i].imshow(rgb)
        axes[i].axis('off')
    
    plt.tight_layout()
    plt.show()       
def imageScale(imagelist,height,width):
    scaledList = list(map(lambda img: cv2.resize(img,(width,height)),imagelist))
    return scaledList
# Birleştirilecek görüntü dosyalarının yolunu içeren bir liste

# Görüntüleri yükleyip bir listeye ekliyoruz
imageList = getImages("images/stitching")
images = imageScale(imageList,600,800)

# Stitcher nesnesini oluşturuyoruz
stitcher = cv2.Stitcher_create()


# Görüntüleri birleştiriyoruz (stitching)
status, stitched = stitcher.stitch(images)

# Durumu kontrol ediyoruz
if status == cv2.Stitcher_OK:
    print("Görüntüler başarıyla birleştirildi")
    # Birleştirilen görüntüyü kaydetmek için:
    cv2.imwrite("stitched_output.jpg", stitched)
    # Birleştirilen görüntüyü göstermek için:
    plt.imshow(stitched)
    plt.show()
else:
    print("Görüntüler birleştirilemedi. Hata kodu:", status)


