import cv2 
import numpy as np 
def removeLines(imageCanny):
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (6,6))#kernel for rectangle
	imageNoLines = cv2.morphologyEx(imageCanny, cv2.MORPH_CLOSE, kernel)#fills inn lines

	imageNoLines = cv2.threshold(imageNoLines,128,255,cv2.THRESH_BINARY)[1]

	return imageNoLines

def getNoteDetectParams(minAreal,maxAreal):
	#filter for a note like shape (ellipse)
	params = cv2.SimpleBlobDetector_Params() 

	# Set Area 
	params.filterByArea = True
	params.minArea = minAreal
	params.maxArea = maxAreal

	# Set Circularity 
	params.filterByCircularity = True
	params.minCircularity = 0.75
	params.maxCircularity = 0.85

	# Set Convexity (the larger -> more like a cricle)
	params.filterByConvexity = True
	params.minConvexity = 0.9
		
	# Set inertia (this gives ellipse like shape between zero and one i think... cicle is 1)
	params.filterByInertia = True
	params.minInertiaRatio = 0.4
	params.maxInertiaRatio = 0.56
	return params
'''
# Load image 
image = cv2.imread('halvor.jpg', 0) 
#image = cv2.resize(image, (500,350))
image = cv2.resize(image, (700,700))

image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
imageCAN = cv2.Canny(image,150,250)
gris = removeLines(imageCAN)
params = getNoteDetectParams(400,1500)

# Create a notedetector with the parameters 
noteDetector = cv2.SimpleBlobDetector_create(params) 	
# Detect ellipse like shape in the binary image (gris) from the parameters given to the notedetector
keypoints = noteDetector.detect(gris) 
# marks detected notes with red dots
for note in cv2.KeyPoint_convert(keypoints):
	image = cv2.circle(image, (round(note[0]),round(note[1])), radius =5, color=(0,0,255), thickness=-1)

# Show blobs 
cv2.imshow("Notes found", image)  
cv2.waitKey(0) 
cv2.destroyAllWindows() 
'''