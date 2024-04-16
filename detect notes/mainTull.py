import cv2 
import numpy as np 
import math
from matplotlib import pyplot as plt

import lineDetection as lines
import blobblob as blob

num_of_lines = 0
new_staff = []

# Load image 
image = cv2.imread('halvor.jpg', 0) 
#image = cv2.resize(image, (500,350))
image = cv2.resize(image, (700,700))

image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
imageCAN = cv2.Canny(image,150,250)

staff = cv2.HoughLines(imageCAN, 1,np.pi/180,170,np.array([]))#95 is the length of line i think...
staff_copy = staff


new_staff = lines.removeDuplicates(staff, new_staff)
final_staff = np.array([line for line in new_staff], dtype=np.float32) #converts to np array

sorted_lines = np.argsort(final_staff[:,0,0])
sorted_lines = final_staff[sorted_lines]

for line in sorted_lines:
    ang,x1,x2,y1,y2 = lines.getLineCalc(line)
    if ang > -85: #check angle of line
        cv2.line(image, (x1,y1),(x2,y2), (0,0,255),1)#draws line
        num_of_lines+=1   
print("number of lines:")
print(num_of_lines)
#print(final_staff)
#print(sorted_lines)




gris = blob.removeLines(imageCAN)
params = blob.getNoteDetectParams(400,1500)

# Create a notedetector with the parameters 
noteDetector = cv2.SimpleBlobDetector_create(params) 	
# Detect ellipse like shape in the binary image (gris) from the parameters given to the notedetector
keypoints = noteDetector.detect(gris) 
# marks detected notes with red dots
for note in cv2.KeyPoint_convert(keypoints):
	image = cv2.circle(image, (round(note[0]),round(note[1])), radius =8, color=(0,0,255), thickness=-1)

# Show blobs 
cv2.imshow("Notes found", image)  
#cv2.imwrite("test",image)
cv2.waitKey(0) 
cv2.destroyAllWindows() 