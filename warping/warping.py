import cv2
import numpy as np

img = cv2.imread("assets/rotated_maad.jpg")
print(img.shape)

cv2.imwrite("assets/maad_scaled.jpg", img)

#Pixel values in the original image
input_points = np.float32([[1063,1609], [2087,1235], [1029, 2592], [2329,2271]])

#Output image size
width = 400
height = 400

#Desired points values in the output image
converted_points = np.float32([[0,0], [width, 0], [0, height], [width, height]])

# perspective transformation
matrix = cv2.getPerspectiveTransform(input_points, converted_points)
img_output = cv2.warpPerspective(img, matrix, (width, height))

# ----------------- Displaying --------------
# Define the desired width and height for display
desired_width = 500
desired_height = 667

# Resize the image
resized_image = cv2.resize(img, (desired_width, desired_height))

cv2.imshow("Original", resized_image)
cv2.imshow("warped perspective", img_output)

cv2.waitKey(0)