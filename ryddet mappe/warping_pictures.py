import cv2
import numpy as np
import warping_utils as utils

img = cv2.imread("ryddet mappe/images/abc_iphone3.JPG")
img_original = img.copy()

# Image modification
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Convert to grayscale

# Trackbar/original image window creation
cv2.namedWindow("trackbar_window", cv2.WINDOW_NORMAL)
cv2.namedWindow("original_image", cv2.WINDOW_NORMAL)
cv2.resizeWindow("trackbar_window", 500, 667)
cv2.resizeWindow("original_image", 550, 733)

# Creating trackbars for the Canny edge detection and bilateral filter
cv2.createTrackbar("threshold1", "trackbar_window", 100, 600, lambda x: None)
cv2.createTrackbar("threshold2", "trackbar_window", 100, 600, lambda x: None)
cv2.createTrackbar("diameter", "trackbar_window", 9, 75, lambda x: None)
cv2.createTrackbar("sigmaColor", "trackbar_window", 75, 300, lambda x: None)
cv2.createTrackbar("sigmaSpace", "trackbar_window", 75, 150, lambda x: None)

while True:

    # Getting the trackbar positions
    threshold1_pos = cv2.getTrackbarPos("threshold1", "trackbar_window")
    threshold2_pos = cv2.getTrackbarPos("threshold2", "trackbar_window")
    diameter_pos = cv2.getTrackbarPos("diameter", "trackbar_window")
    sigmaColor_pos = cv2.getTrackbarPos("sigmaColor", "trackbar_window")
    sigmaSpace_pos = cv2.getTrackbarPos("sigmaSpace", "trackbar_window")

    # To avoid undefined behavior
    if diameter_pos == 0:
        diameter_pos = 1

    # Applying the bilateral filter and Canny edge detection from the trackbar positions
    gray_filtered = cv2.bilateralFilter(gray, diameter_pos, sigmaColor_pos, sigmaSpace_pos)
    edged = cv2.Canny(gray_filtered, threshold1_pos, threshold2_pos)
    cv2.imshow("trackbar_window", edged)
    cv2.imshow("original_image", img_original)

    # Draw text on the image
    cv2.putText(img_original, "Press q to exit", (10, 300), cv2.FONT_HERSHEY_SIMPLEX, 10, (0, 0, 255), 4)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
# Printing the chosen trackbar positions
print(f"chose trackbar values: \n threshold1: {threshold1_pos}, threshold2: {threshold2_pos}, diameter: {diameter_pos}, sigmaColor: {sigmaColor_pos}, sigmaSpace: {sigmaSpace_pos}")

# Find contours, hierarchy is not used
contours, hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Sort contours by area, biggest first
contours = sorted(contours, key = cv2.contourArea, reverse = True)

#Finds the contour with the biggest area which has 4 corners
filtered = utils.contour_filtering(contours, epsilon_scale=0.02, min_area_threshold=1000)

# Sometimes the method doesn't find 4 corners -> then return error
if filtered.size == 0:
    print("No 4 vertices found! Exiting..")
    exit(1)

# Draw the filtered out contour
cv2.drawContours(img, [filtered], -1, (0, 255, 0), 3)

# get corner points of the contour in pixel values
corner_points = utils.get_corner_points(filtered)

# Draw circles over the corners
utils.draw_circles_on_corners(img, corner_points, circle_radius=40, line_thickness=5)

# What we want the warped image to be
width_warped = 700
height_warped = 700

# Putting it in the right format 
converted_points = np.array([[0,0], [width_warped, 0], [width_warped, height_warped], [0, height_warped]], dtype="float32")

# Getting the transformation matrix
matrix = cv2.getPerspectiveTransform(corner_points, converted_points)
# Warping the image with the transformation matrix (perspective transformation)
img_output = cv2.warpPerspective(img_original, matrix, (width_warped, height_warped))


# ---Displaying the images---

# Image shape modification (Gray and edged are single channel, img is 3 channel)
gray = np.stack((gray,)*3, axis=-1) 
edged = np.stack((edged,)*3, axis=-1)

# Image stacking (getting all images in one window)
img_hor = np.hstack((img_original, gray, edged, img))

# Scaling the image to fit the screen, 4/3 is the aspect ratio of the images from the phone
cv2.namedWindow("step_by_step", cv2.WINDOW_NORMAL)
cv2.resizeWindow("step_by_step", 500*3, 667*3) 
cv2.imshow("step_by_step", img_hor)

cv2.namedWindow("warped_perspective", cv2.WINDOW_NORMAL)
cv2.resizeWindow("warped_perspective", width_warped, height_warped)
cv2.imshow("warped_perspective", img_output)

# Saving the warped image so it can be used in the next step
cv2.imwrite("ryddet mappe/images/test.jpg", img_output)

cv2.waitKey(0)