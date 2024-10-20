import os
import numpy as np
import cv2
import glob
import matplotlib.pyplot as plt

# Global constants
WIDTH = 800
HEIGHT = 600
MIN_MATCH_COUNT = 5

#* RESIM ISLEMLERI
def getImages(path, extension="JPG"):
    img_path = glob.glob(os.path.join(path, f"*.{extension}"))
    images = [cv2.imread(img) for img in img_path]
    return images

def imageShow(imageList):
    fig, axes = plt.subplots(1, len(imageList), figsize=(15, 6))
    for i, img in enumerate(imageList):
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Corrected to RGB
        axes[i].imshow(rgb)
        axes[i].axis('off')
    plt.tight_layout()
    plt.show()

def imageScale(imageList, height, width):
    return [cv2.resize(img, (width, height)) for img in imageList]

#* IMAGE STITCHING ISLEMLERI
def warpImages(img1, img2, H):
    rows1, cols1 = img1.shape[:2]
    rows2, cols2 = img2.shape[:2]

    # Coordinates of reference and second image corners
    points1 = np.float32([[0, 0], [0, rows1], [cols1, rows1], [cols1, 0]]).reshape(-1, 1, 2)
    points2 = np.float32([[0, 0], [0, rows2], [cols2, rows2], [cols2, 0]]).reshape(-1, 1, 2)

    # Warp perspective
    points2_transformed = cv2.perspectiveTransform(points2, H)
    all_points = np.concatenate((points1, points2_transformed), axis=0)

    [x_min, y_min] = np.int32(all_points.min(axis=0).ravel() - 0.5)
    [x_max, y_max] = np.int32(all_points.max(axis=0).ravel() + 0.5)

    # Translation matrix to fit everything in the output image
    translation_dist = [-x_min, -y_min]
    H_translation = np.array([[1, 0, translation_dist[0]], [0, 1, translation_dist[1]], [0, 0, 1]])

    # Warp the second image
    output_img = cv2.warpPerspective(img2, H_translation.dot(H), (x_max - x_min, y_max - y_min))
    output_img[translation_dist[1]:rows1 + translation_dist[1], translation_dist[0]:cols1 + translation_dist[0]] = img1
    return output_img

def descriptorSelector(image, method="ORB", debug=False):
    assert method, "No method described"

    descriptor = {
        "ORB": lambda: cv2.ORB_create(nfeatures=2000)
    }.get(method, lambda: cv2.ORB_create(nfeatures=2000))()

    keypoints, features = descriptor.detectAndCompute(image, None)

    if debug:
        img_keypoints = cv2.drawKeypoints(image, keypoints, None, color=(0, 255, 0))
        plt.imshow(cv2.cvtColor(img_keypoints, cv2.COLOR_BGR2RGB))
        plt.axis('off')
        plt.show()

    return keypoints, features

def stitchImages(img1, img2, method="ORB", crossCheck=False, debug=False):
    keypoints1, descriptors1 = descriptorSelector(img1, method, debug)
    keypoints2, descriptors2 = descriptorSelector(img2, method, debug)

    if method in ["SIFT", "SURF"]:
        bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=crossCheck)
    else:
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=crossCheck)

    matches = bf.knnMatch(descriptors1, descriptors2, k=2)

    good = [m for m, n in matches if m.distance < 0.6 * n.distance]  # Adjust threshold if necessary

    if len(good) > MIN_MATCH_COUNT:
        src_pts = np.float32([keypoints1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([keypoints2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

        H, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        return warpImages(img1, img2, H)
    else:
        if debug:
            print(f"Not enough matches are found: {len(good)}/{MIN_MATCH_COUNT}")
        return None

def finalStitching(imageList, method="ORB", crossCheck=False, debug=False):
    stitched_image = imageList[0]
    for i in range(1, len(imageList)):
        stitched_image = stitchImages(stitched_image, imageList[i], method, crossCheck, debug)
        if stitched_image is None:
            print(f"Stitching failed at image {i}.")
            break
    return stitched_image

# Load and scale images
imageList = getImages("images/stitching")
imageList = imageScale(imageList, HEIGHT, WIDTH)

# Perform stitching
final_image = finalStitching(imageList, method="ORB", crossCheck=False, debug=False)

# Show final stitched image
if final_image is not None:
    plt.imshow(cv2.cvtColor(final_image, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()
else:
    print("Stitching process failed.")
