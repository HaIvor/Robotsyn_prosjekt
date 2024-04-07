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
edged = cv2.Canny(gray, 10, 20)

cv2.namedWindow("frame")
cv2.createTrackbar("threshold1", "frame", 100, 300, lambda x: print(x))
cv2.createTrackbar("threshold2", "frame", 100, 300, lambda x: print(x))

# Define the desired width and height for display
desired_width = 500
desired_height = 667

original_resized = cv2.resize(img, (desired_width, desired_height))
gray_resized = cv2.resize(gray, (desired_width, desired_height))
edged_resized = cv2.resize(edged, (desired_width, desired_height))

while True:
    cv2.imshow("frame", edged)
    threshold1_pos = cv2.getTrackbarPos("threshold1", "frame")
    threshold2_pos = cv2.getTrackbarPos("threshold2", "frame")
    edged = cv2.Canny(gray_resized, threshold1_pos, threshold2_pos)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ----------------- Displaying --------------
# Define the desired width and height for display
# desired_width = 500
# desired_height = 667

# Resize the image
# resized_image_orginal = cv2.resize(img, (desired_width, desired_height))
# resized_image_gray = cv2.resize(gray, (desired_width, desired_height))
# resized_image_edged = cv2.resize(edged, (desired_width, desired_height))

# cv2.imshow("Original", resized_image_orginal)
# cv2.imshow("Gray", resized_image_gray)
# cv2.imshow("Edged", resized_image_edged)
#cv2.imshow("warped perspective", img_output)

cv2.waitKey(0)