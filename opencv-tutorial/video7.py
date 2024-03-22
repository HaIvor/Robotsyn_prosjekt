#template matching

#ball.png should be the same size as the ball in the image, close at least

import numpy as np 
import cv2 

img = cv2.resize(cv2.imread("assets/soccer_practice.jpg", 0), (0,0), fx=0.5, fy=0.5)
template = cv2.resize(cv2.imread("assets/shoe.png", 0), (0,0), fx=0.5, fy=0.5)
h, w = template.shape


methods = [cv2.TM_CCOEFF, cv2.TM_CCOEFF_NORMED, cv2.TM_CCORR, 
           cv2.TM_CCORR_NORMED, cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]

for method in methods:
    img2 = img.copy()

    result = cv2.matchTemplate(img2, template, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    print(min_loc, max_loc)
    #max/min is different for different methods so therefore the logic
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        location = min_loc
    else:
        location = max_loc

    bottom_right = (location[0] + w, location[1] + h)
    cv2.rectangle(img2, location, bottom_right, 255, 5)
    cv2.imshow("match",img2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    #(W - w + 1, H - h + 1)
    # W: Width of base image, w: width of template image

""" 
(3, 3)
W = 4
w = 2
H = 4
h = 2
4x4
2x2

#slide to right, slide down
#"matching matrix"
[[0, 0, 0],
 [0, 1, 0],
 [0 ,0, 0]]

[[255, 255, 255, 255],
 [255, 255, 255, 255],
 [255, 255, 255, 255],
 [255, 255, 255, 255]]

[[255, 255],
 [255, 255]] """