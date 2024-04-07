import cv2
import numpy as np

img = cv2.imread("assets/rotated_maad.jpg")
img_original = img.copy()

# Image modification
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Convert to grayscale
#bilateralFilter(src, diameter , sigmaColor, sigmaSpace[, dst[, borderType]]) -> dst
gray = cv2.bilateralFilter(gray, 20, 30, 30) # Smoothen the image with bilateral filter

# Search for edges
# Canny(image, threshhold1, threshhold2) -> edges
edged = cv2.Canny(gray, 95, 230)

cv2.namedWindow("frame")
cv2.createTrackbar("threshold1", "frame", 100, 300, lambda x: print(x))
cv2.createTrackbar("threshold2", "frame", 100, 300, lambda x: print(x))

# Define the desired width and height for display
desired_width = 500
desired_height = 667

# ----------------- Displaying --------------
# Define the desired width and height for display

cv2.namedWindow("original_resized", cv2.WINDOW_NORMAL) 
cv2.resizeWindow("original_resized", 500, 667) 

cv2.namedWindow("gray_resized", cv2.WINDOW_NORMAL)
cv2.resizeWindow("gray_resized", 500, 667)

cv2.namedWindow("edged_resized", cv2.WINDOW_NORMAL)
cv2.resizeWindow("edged_resized", 500, 667)


cv2.imshow("original_resized", img_original)
cv2.imshow("gray_resized", gray)
cv2.imshow("edged_resized", edged)

cv2.waitKey(0)