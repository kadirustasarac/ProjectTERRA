import os
import numpy
import cv2
import glob
import matplotlib.pyplot as plt


def getImages(path):
    images = []
    img_path = glob.glob(os.path.join(path,"*.JPG"))
    images = list(map(lambda img: cv2.imread(img),img_path))
    return images


def imageShow(imageList):
    for img in imageList:
        plt.imshow(img)
        plt.axis('off')
        plt.show()





imageList = getImages("imageStitching/Pictures/")
print(type(imageList[0]))
imageShow(imageList)