import cv2
import numpy as np

# Görüntüleri yükle
image1 = cv2.imread('image1.jpg')
image2 = cv2.imread('image2.jpg')

width_to_scale = 800
height_to_scale = 600

image1 = cv2.resize(image1,(width_to_scale,height_to_scale))
image2 = cv2.resize(image2,(width_to_scale,height_to_scale))
# SIFT ile özellik noktaları bul
sift = cv2.SIFT_create()
keypoints1, descriptors1 = sift.detectAndCompute(image1, None)
keypoints2, descriptors2 = sift.detectAndCompute(image2, None)

# BFMatcher ile noktaları eşleştir
bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
matchings = bf.match(descriptors1, descriptors2)

# Eşleşmeleri sırala
matchings = sorted(matchings, key = lambda x:x.distance)

# En iyi eşleşmeleri kullanarak homografi hesapla
src_pts = np.float32([ keypoints1[m.queryIdx].pt for m in matchings ]).reshape(-1,1,2)
dst_pts = np.float32([ keypoints2[m.trainIdx].pt for m in matchings ]).reshape(-1,1,2)
H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

# Görüntüyü döndür ve yeniden yerleştir
height, width, channels = image2.shape
image1_warped = cv2.warpPerspective(image1, H, (width, height))

# Görüntüleri birleştir
result = np.maximum(image1_warped, image2)

# Sonucu görselleştir
cv2.imshow('Mosaic', result)

cv2.waitKey(0)
cv2.destroyAllWindows()