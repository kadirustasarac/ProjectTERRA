import cv2
import numpy as np

def stitch_images(img1, img2):
    
    sift = cv2.SIFT_create()
    keypoints1, descriptors1 = sift.detectAndCompute(img1, None)
    keypoints2, descriptors2 = sift.detectAndCompute(img2, None)
    
    bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
    matches = bf.match(descriptors1, descriptors2)
    matches = sorted(matches, key=lambda x: x.distance)
    
    best_matches = matches[:50]
    
    src_pts = np.float32([keypoints1[m.queryIdx].pt for m in best_matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([keypoints2[m.trainIdx].pt for m in best_matches]).reshape(-1, 1, 2)
    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
    
    height, width, channels = img2.shape
    img1_warp = cv2.warpPerspective(img1, M, (width + img1.shape[1], height))
    img1_warp[0:height, 0:width] = img2
    
    return img1_warp


img1 = cv2.imread('gorsel1.jpg')
img2 = cv2.imread('gorsel2.jpg')


stitched_image = stitch_images(img1, img2)


cv2.imwrite('birlesmis_gorsel.jpg', stitched_image)
cv2.imshow('Birleşmiş Görüntü', stitched_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
