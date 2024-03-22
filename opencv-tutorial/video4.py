import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    width = int(cap.get(3))
    height = int(cap.get(4))

    #draw a line, top left corner is 0,0
    # from 0,0 to end, blue line, 10 thickness
    img = cv2.line(frame, (0,0), (width, height), (255,0,0), 10)
    img = cv2.line(img, (0,height), (width, 0), (0,255,0), 10)
    #top left rectangle to bottom right, color, thickness
    img = cv2.rectangle(img, (100,100), (200,200), (128,128,128), 5)
    # center circle, radius 60, red, -1 is fill
    img = cv2.circle(img, (300,300), 60, (0,0,255), -1)

    font = cv2.FONT_HERSHEY_SIMPLEX
    #bottom left corner, font, size, color, thickness, line type (cv2.line_aa makes it better...)
    img = cv2.putText(img, "Hello world", (100, height-100), font, 3, (255,255,255), 10, cv2.LINE_AA)

    cv2.imshow("frame", frame)

    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()