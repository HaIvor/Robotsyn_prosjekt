import cv2
import numpy as np

cap = cv2.VideoCapture(0)

cv2.namedWindow("frame")

# lambda x: print(x), prints the value of the trackbar each time it is moved
cv2.createTrackbar("test", "frame", 50, 500, lambda x: print(x))

while True:
    _, frame = cap.read()
    cv2.imshow("frame", frame)

    trackbar_pos = cv2.getTrackbarPos("test", "frame")
    if trackbar_pos == 0:
        print("Hello")
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()