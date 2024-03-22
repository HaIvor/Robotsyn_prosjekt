import numpy as np 
import cv2

img = cv2.imread("assets/chess.png")
img = cv2.resize(img, (0,0), fx=0.9, fy=0.9)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#shi tomasi corner detection, 100 best corners, quality level 0-1, min distance between corners, euclidean distance
corners = cv2.goodFeaturesToTrack(gray, 100, 0.01, 10)
#corners are floating point values
corners = np.int0(corners)


for corner in corners:
    x, y = corner.ravel() #[[1, 2], [2,1]] -> [1,2,2,1]. [[x,y]] -> [x,y]
    cv2.circle(img, (x,y), 3, (255,0,0), -1)

for i in range(len(corners)):
    for j in range(i+1, len(corners)):
        corner1 = tuple(corners[i][0]) # [0]: [[x, y]] -> [x, y]
        corner2 = tuple(corners[j][0])
        color = tuple(map(lambda x: int(x), np.random.randint(0, 255, size=3)))
        cv2.line(img, corner1, corner2, color, 1)
""" 
euclidean distance formula
(x1,y1) (x2,y2)
sqrt((x2-x1)^2 + (y2-y1)^2)
 """



cv2.imshow("Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()