import cv2
import numpy as np

img = cv2.imread("assets/abc_iphone (3).jpg")
img = cv2.resize(img, (700, 700))
img2 = img.copy()
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img = cv2.bilateralFilter(img, 4, 94, 70)
img = cv2.Canny(img, 268, 148)

img_2 = cv2.imread("assets/abc_iphone (3).jpg")
img_2 = cv2.resize(img_2, (700, 700))
# Convert img_gray to a three-dimensional array to match the dimensions of img_2
img_gray_3d = np.dstack((img, img, img))



contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)#edged.copy()?
# sorterer contours etter størrelse, sort descending, tar de 10 største
contours = sorted(contours, key = cv2.contourArea, reverse = True)[:100]

for i in contours:
    cv2.drawContours(img2, [i], -1, (0, 255, 0), 3)
cv2.imshow("hough", img2)
img_hor = np.hstack((img_2, img2))
cv2.namedWindow("Two Pictures", cv2.WINDOW_NORMAL)
cv2.imshow("Two Pictures", img_hor)
cv2.imwrite('contour_example.jpg', img_hor)
cv2.waitKey(0)
cv2.destroyAllWindows()
