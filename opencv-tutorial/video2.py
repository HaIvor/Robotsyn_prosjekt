import cv2
import random
#open cv and numpy is working together
img = cv2.imread("assets/damn.jpeg",-1)
img = cv2.resize(img, (0,0), fx=0.3, fy=0.3)

tag = img[100:150,200:300]
img[250:300,100:200] = tag
#print(img)

#height, width, channels. channels are the colorspaces. BRG here...
print(img.shape)

#three values for each pixel. 0,0,0 is black. 255,255,255 is white.
""" [
    [[0,0,0], [255, 255, 255]],
    [[0,0,0], [255, 255, 255]]
] """
#first row
#print(img[0])

print(img[257][250:254])

for i in range(130):
    for j in range(img.shape[1]):
        img[i][j] = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]

cv2.imshow("Image",img)
#wait an infinite amount of time for a key to be pressed (5 is 5 seconds)
cv2.waitKey(0)
#then destroy them all so they dont run in the background for no reason
cv2.destroyAllWindows()