import os
import numpy as np
import cv2
import glob
import matplotlib.pyplot as plt



WIDTH = 800
HEIGHT = 600

MIN_MATCH_COUNT = 3

#* RESIM ISLEMLERI

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


#* IMAGE STITCHING ISLEMLERI
def warpImages(img1, img2, H):
    
  rows1, cols1 = img1.shape[:2]
  rows2, cols2 = img2.shape[:2]

  list_of_points_1 = np.float32([[0,0], [0, rows1],[cols1, rows1], [cols1, 0]]).reshape(-1, 1, 2) #coordinates of a reference image
  temp_points = np.float32([[0,0], [0,rows2], [cols2,rows2], [cols2,0]]).reshape(-1,1,2) #coordinates of second image

  # When we have established a homography we need to warp perspective
  # Change field of view
  list_of_points_2 = cv2.perspectiveTransform(temp_points, H)#calculate the transformation matrix

  list_of_points = np.concatenate((list_of_points_1,list_of_points_2), axis=0)

  [x_min, y_min] = np.int32(list_of_points.min(axis=0).ravel() - 0.5)
  [x_max, y_max] = np.int32(list_of_points.max(axis=0).ravel() + 0.5)
  
  translation_dist = [-x_min,-y_min]
  
  H_translation = np.array([[1, 0, translation_dist[0]], [0, 1, translation_dist[1]], [0, 0, 1]])

  output_img = cv2.warpPerspective(img2, H_translation.dot(H), (x_max-x_min, y_max-y_min))
  output_img[translation_dist[1]:rows1+translation_dist[1], translation_dist[0]:cols1+translation_dist[0]] = img1

  return output_img


def descriptorSelector(image,method = "ORB",debug=False):
  assert method is not None, "No method described"

  if method == "SIFT":
      descriptor = cv2.SIFT_create()
  elif method == "SURF":
      descriptor = cv2.SURF_create()
  elif method == "BRISK":
      descriptor = cv2.BRISK_create()
  elif method == "ORB":
      descriptor = cv2.ORB_create(nfeatures=2000)

  (keypoints, features) = descriptor.detectAndCompute(image, None)

  if(debug):
     img_keypoints = cv2.drawKeypoints(image,keypoints,None, color=(0, 255, 0))
     plt.imshow(img_keypoints)
     plt.show()
  return (keypoints,features)




imageList = getImages("images/stitching")
imageList = imageScale(imageList,600,800)


def stitchImages(method, crossCheck,img1,img2):

    keypoints1,descriptors1 = descriptorSelector(img1,method)
    keypoints2,descriptors2 = descriptorSelector(img2,method)

    if method == "SIFT" or method == "SURF":
        bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=crossCheck)
    elif method== "ORB" or method == "BIRSK":
        bf = cv2.BFMatcher(cv2.NORM_HAMMING,crossCheck=crossCheck)
    
    matches = bf.knnMatch(descriptors1, descriptors2,k=2)

    all_matches = []
    for m, n in matches:
      all_matches.append(m)
#   Finding the best matches
    good = []
    for m, n in matches:
      if m.distance < 0.75 * n.distance:#Threshold
          good.append(m)

#   Set minimum match condition

    if len(good) > MIN_MATCH_COUNT:

      # Convert keypoints to an argument for findHomography
      src_pts = np.float32([ keypoints1[m.queryIdx].pt for m in good]).reshape(-1,1,2)
      dst_pts = np.float32([ keypoints2[m.trainIdx].pt for m in good]).reshape(-1,1,2)

      # Establish a homography
      M, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)

      result = warpImages(img2, img1, M)
      return result




def finalMethod(imageList):
    for i in range(0,len(imageList) - 1):
        final_img = stitchImages("SIFT",False,imageList[0],imageList[1])
        imageList.pop(0)
        imageList.pop(0)
        imageList.insert(0,final_img)

    return imageList[0]



if __name__ == "__main__":
    imageFinal = finalMethod(imageList)
    plt.imshow(imageFinal)
    plt.show()







