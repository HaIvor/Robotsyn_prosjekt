import cv2

img = cv2.imread("assets/notes.png",-1)

#resize the image to 800x800px
#img = cv2.resize(img, (800,800))

#when using fx fy, just put 0,0. The fx and fy are the scaling factors in the x and y directions respectively.
img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)

img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)

#make new file
cv2.imwrite("assets/rotated_img.jpg",img)

#bgr instead of rbg ...?

#-1, cv2.IMREAD_COLOR : Loads a color image. Any transparency of image will be neglected. It is the default flag.
#0, cv2.IMREAD_GRAYSCALE : Loads image in grayscale mode
#1, cv2.IMREAD_UNCHANGED : Loads image as such including alpha channel

cv2.imshow("Image",img)
#wait an infinite amount of time for a key to be pressed (5 is 5 milliseconds)
cv2.waitKey(0)
#then destroy them all so they dont run in the background for no reason
cv2.destroyAllWindows()