import cv2
import numpy as np

# Görüntüleri yükleme
img1 = cv2.imread('images/first.JPG', 0)  # İlk görüntü
img2 = cv2.imread('images/second.JPG', 0)  # İkinci görüntü

# Görüntülerin doğru yüklenip yüklenmediğini kontrol etme
if img1 is None or img2 is None:
    print("Görüntüler yüklenemedi. Dosya yolunu kontrol edin.")
    exit()

# SIFT detektörü oluşturma
sift = cv2.SIFT_create()

# Anahtar noktaları ve tanımlayıcıları bulma
keypoints1, descriptors1 = sift.detectAndCompute(img1, None)
keypoints2, descriptors2 = sift.detectAndCompute(img2, None)

# Tanımlayıcıların boş olup olmadığını kontrol etme
if descriptors1 is None or descriptors2 is None:
    print("Özellik bulunamadı, lütfen görüntülerin yeterince detay içerdiğinden emin olun.")
    exit()

# BFMatcher oluşturma ve özellik eşleştirme
bf = cv2.BFMatcher()
matches = bf.knnMatch(descriptors1, descriptors2, k=2)

# İyi eşleşmeleri seçme
good_matches = []
for m, n in matches:
    if m.distance < 0.75 * n.distance:
        good_matches.append(m)

# Eşleşen noktaların sayısını kontrol etme
if len(good_matches) < 10:
    print("Yeterli iyi eşleşme bulunamadı.")
    exit()

# Eşleşen noktaları bulma
src_pts = np.float32([keypoints1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
dst_pts = np.float32([keypoints2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

# Homografi matrisini bulma
H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

# Görüntü 2'yi hizalama (warp)
height, width = img1.shape
img2_aligned = cv2.warpPerspective(img2, H, (width + img2.shape[1], height))

# Görüntü 1'i yerleştirme
img2_aligned[0:height, 0:width] = img1

# Sonucu gösterme
cv2.imshow("Birleşmiş Görüntü", img2_aligned)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Sonucu kaydetme
cv2.imwrite('stitched_image.jpg', img2_aligned)
