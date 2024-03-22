import numpy as np
import cv2

#camera number 0
cap = cv2.VideoCapture(0)

while True:
    #17 different properties of this capture object...?
    ret, frame = cap.read()
    width = int(cap.get(3))
    height = int(cap.get(4))

    image = np.zeros(frame.shape, np.uint8)
    smaller_frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
    #top left
    image[:height//2, :width//2] = cv2.rotate(smaller_frame, cv2.ROTATE_180)
    #bottom left
    image[height//2:, :width//2] = smaller_frame
    #top right
    image[:height//2, width//2:] = smaller_frame
    #bottom right
    image[height//2:, width//2:] = smaller_frame

    cv2.imshow("navn på vindu", image)
    
    #ord returns the unicode of the key pressed
    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()