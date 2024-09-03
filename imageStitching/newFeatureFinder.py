import cv2
import numpy as np
import matplotlib.pyplot as plt
import warnings


ALGORITHM = 'BRISK'

feature_to_match = 'bf'

train_photo = cv2.imread("image1.JPG")
query_photo = cv2.imread("image2.JPG")

train_photo_rgb = cv2.cvtColor(train_photo,cv2.COLOR_BGR2RGB)
train_photo_gray = cv2.cvtColor(train_photo_rgb,cv2.COLOR_RGB2GRAY)

query_photo_rgb = cv2.cvtColor(query_photo,cv2.COLOR_BGR2RGB)
query_photo_gray = cv2.cvtColor(query_photo_rgb,cv2.COLOR_RGB2GRAY)

def select_descriptor_method(image, method=None):
    assert method is not None, "No method described"
    
    if method == "SIFT":
        descriptor = cv2.SIFT_create()
    elif method == "SURF":
        descriptor = cv2.SURF_create()
    elif method == "BRISK":
        descriptor = cv2.BRISK_create()
    elif method == "ORB":
        descriptor = cv2.ORB_create()
    
    (keypoints, features) = descriptor.detectAndCompute(image, None)
    return (keypoints,features)

keypoint_train_img, feature_train_img = select_descriptor_method(train_photo_gray, ALGORITHM)
keypoint_query_img, feature_query_img = select_descriptor_method(query_photo_gray, ALGORITHM)

for keypoint in keypoint_query_img:
    x,y = keypoint.pt
    size = keypoint.size
    orientation = keypoint.angle
    response = keypoint.response
    octave = keypoint.octave
    class_id = keypoint.class_id


    fig , (ax1,ax2) = plt.subplots(nrows=1,ncols=2,figsize=(20,8),constrained_layout=False)
    
    ax1.imshow(cv2.drawKeypoints(train_photo_gray,keypoint_train_img,None,color=(0,255,0)))
    ax1.set_xlabel('(a)')

    ax2.imshow(cv2.drawKeypoints(query_photo_gray,keypoint_query_img,None,color=(0,255,0)))
    ax2.set_xlabel('(b)')

    plt.savefig(ALGORITHM + '_feature_img' + ".jpeg",bbox_inches = 'tight',dpi=300,format='jpeg')
    plt.show()