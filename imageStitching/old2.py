import cv2
import numpy as np
import matplotlib.pyplot as plt
import warnings


ALGORITHM = 'SIFT'

feature_to_match = 'bf'

width_to_scale = 800
height_to_scale = 600

train_photo = cv2.imread("images/stitching/image1.JPG")
query_photo = cv2.imread("images/stitching/image2.JPG")

train_photo = cv2.resize(train_photo,(width_to_scale,height_to_scale))
query_photo = cv2.resize(query_photo,(width_to_scale,height_to_scale))

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

# for keypoint in keypoint_query_img:
#     x,y = keypoint.pt
#     size = keypoint.size
#     orientation = keypoint.angle
#     response = keypoint.response
#     octave = keypoint.octaved 
#     class_id = keypoint.class_id


#     fig , (ax1,ax2) = plt.subplots(nrows=1,ncols=2,figsize=(20,8),constrained_layout=False)
    
#     ax1.imshow(cv2.drawKeypoints(train_photo_gray,keypoint_train_img,None,color=(0,255,0)))
#     ax1.set_xlabel('(a)')

#     ax2.imshow(cv2.drawKeypoints(query_photo_gray,keypoint_query_img,None,color=(0,255,0)))
#     ax2.set_xlabel('(b)')

    #plt.savefig(ALGORITHM + '_feature_img' + ".jpeg",bbox_inches = 'tight',dpi=300,format='jpeg')
    #plt.show()


def create_matching_object(method, crossCheck):
    if method == "SIFT" or method == "SURF":
        bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=crossCheck)
    elif method== "ORB" or method == "BIRSK":
        bf = cv2.BFMatcher(cv2.NORM_HAMMING,crossCheck=crossCheck)
    
    return bf

def keypoints_matching(feature_train_img,feature_query_img,method):
    bf = create_matching_object(method,crossCheck=True)

    best_matches = bf.match(feature_train_img,feature_query_img)

    raw_matches = sorted(best_matches, key = lambda x: x.distance)
    print('Raw matches with BF' , len(raw_matches))

    return raw_matches

def keypoints_matching_KNN(feature_train_img,feature_query_img,ratio,method):
    bf = create_matching_object(method,crossCheck=False)

    raw_matches = bf.knnMatch(feature_train_img,feature_query_img,k=2)
    
    print('Raw matches with KNNS' , len(raw_matches))

    knn_matches = []

    for m,n in raw_matches:
        if m.distance > n.distance * ratio:
            knn_matches.append(m)

    return knn_matches


print('Drawing matched features for', feature_to_match)

fig = plt.figure(figsize=(20,8))
if feature_to_match == "bf":
    matches = keypoints_matching(feature_train_img,feature_query_img,ALGORITHM)
    mapped_feature_image = cv2.drawMatches(train_photo_rgb,keypoint_train_img,query_photo_rgb,keypoint_query_img,matches[:100],None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

elif feature_to_match == "knn":
    matches = keypoints_matching_KNN(feature_train_img,feature_query_img,0.75,ALGORITHM)
    mapped_feature_image_KNN = cv2.drawMatches(train_photo_rgb,keypoint_train_img,query_photo_rgb,keypoint_query_img,np.random.choice(matches,100),None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

plt.imshow(mapped_feature_image)
plt.show()

def homography_stitching(keypoints_train_img, keypoints_query_img, matches, reprojThresh):   

    keypoints_train_img = np.float32([keypoint.pt for keypoint in keypoints_train_img])
    keypoints_query_img = np.float32([keypoint.pt for keypoint in keypoints_query_img])
    
    if len(matches) > 4:
        # construct the two sets of points
        points_train = np.float32([keypoints_train_img[m.queryIdx] for m in matches])
        points_query = np.float32([keypoints_query_img[m.trainIdx] for m in matches])
        
        # Calculate the homography between the sets of points
        (H, status) = cv2.findHomography(points_train, points_query, cv2.RANSAC, reprojThresh)

        return (matches, H, status)
    else:
        return None
    
M = homography_stitching(keypoint_train_img,keypoint_query_img,matches,reprojThresh=4)

if M is None:
    print("NEGGGGAAAA")

(matches,Homography_Matrix,status) = M

width = query_photo.shape[1] + train_photo.shape[1]

height = max(query_photo.shape[0], train_photo.shape[0])

result = cv2.warpPerspective(train_photo,Homography_Matrix,(width,height))

plt.figure(figsize=(20,10))
plt.axis('off')
plt.imshow(result)
plt.show()

