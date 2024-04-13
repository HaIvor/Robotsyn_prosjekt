import cv2
import numpy as np 

img = cv2.imread('assets/martin.jpg',0)
img = cv2.medianBlur(img,5)
cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,20,
                            param1=50,param2=30,minRadius=0,maxRadius=40)
# print(circles)
circles = np.uint16(np.around(circles))
for i in circles[0,:]:
    print(i)
    # draw the outer circle
    cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
    # print(cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2))
    # draw the center of the circle
    cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

cv2.namedWindow("circle detect", cv2.WINDOW_NORMAL) #så ikke zoomed-in
cv2.resizeWindow("circle detect", cimg.shape[0]-100, cimg.shape[1]-120) 
cv2.imshow('circle detect',cimg)
cv2.waitKey(0)