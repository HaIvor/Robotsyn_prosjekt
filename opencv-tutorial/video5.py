import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    width = int(cap.get(3))
    height = int(cap.get(4))

    #hsv: hue, saturation, value=lightness?
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_orange = np.array([5, 50, 50])
    upper_orange = np.array([15, 255, 255])

    #mask is the part of the image that is blue
    mask = cv2.inRange(hsv, lower_orange, upper_orange)

    result = cv2.bitwise_and(frame, frame, mask=mask)

    """ 
    bitwise_and
    1 1 = 1
    0 1 = 0
    1 0 = 0
    0 0 = 0 """

    cv2.imshow("frame", result)
    cv2.imshow("mask", mask)

    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()



""" BGR_color = np.array([[[255,0,0]]])
x = cv2.cvtColor(BGR_color, cv2.COLOR_BGR2HSV)
x[0][0] is the one pixel in hsv format"""