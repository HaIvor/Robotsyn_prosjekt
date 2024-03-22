import cv2

img = cv2.imread("assets/abnormal.jpg",-1)
img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)

cv2.imshow("Image",img)
print("(rows, columns, colors):", img.shape)

cv2.waitKey(0)
cv2.destroyAllWindows()