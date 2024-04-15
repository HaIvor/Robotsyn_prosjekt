import cv2 
import numpy as np 

# Load image 
image = cv2.imread('assets/martin.jpg', 0) 
#image = cv2.resize(image, (500,350))
image = cv2.resize(image, (700,700))
image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
gris = cv2.Canny(image,150,250)
# do morphology remove horizontal lines
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,7))
gris = cv2.morphologyEx(gris, cv2.MORPH_CLOSE, kernel, iterations = 1)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (6,1))
gris = cv2.morphologyEx(gris, cv2.MORPH_CLOSE, kernel, iterations = 1)
gris = cv2.threshold(gris,128,255,cv2.THRESH_BINARY)[1]


# Set our filtering parameters 
# Initialize parameter setting using cv2.SimpleBlobDetector 
params = cv2.SimpleBlobDetector_Params() 

# Set Area filtering parameters 
params.filterByArea = True
params.minArea = 950
params.maxArea = 1200
# Set Circularity filtering parameters 
params.filterByCircularity = True
params.minCircularity = 0.5

# Set Convexity filtering parameters 
params.filterByConvexity = True
params.minConvexity = 0.9
	
# Set inertia filtering parameters 
params.filterByInertia = True
params.minInertiaRatio = 0.01
#params.maxInertiaRatio = 0.99

# Create a detector with the parameters 
detector = cv2.SimpleBlobDetector_create(params) 
	
# Detect blobs 
keypoints = detector.detect(gris) 

# Draw blobs on our image as red circles 
circle = cv2.drawKeypoints(image, keypoints, outImage=image, color =(0, 0, 255), 
						flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS) 

number_of_blobs = len(keypoints) 
print(cv2.KeyPoint_convert(keypoints))
image = cv2.circle(image, (158,595), radius =10, color=(0,0,255), thickness=-1)
'''
text = "Number of Circular Blobs: " + str(len(keypoints)) 
cv2.putText(blobs, text, (20, 550), 
			cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 100, 255), 2) 
'''
# Show blobs 
cv2.imshow("Filtering Circular Blobs Only", image) 
cv2.waitKey(0) 
cv2.destroyAllWindows() 