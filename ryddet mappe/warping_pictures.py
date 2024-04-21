import cv2
import numpy as np
import warping_utils as utils

img = cv2.imread("ryddet mappe/images/abc_iphone3.jpg")
img_original = img.copy()

# Image modification
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Convert to grayscale

# Trackbar/original image window creation
cv2.namedWindow("trackbar_window", cv2.WINDOW_NORMAL)
cv2.namedWindow("original_image", cv2.WINDOW_NORMAL)
cv2.resizeWindow("trackbar_window", 500, 667)
cv2.resizeWindow("original_image", 550, 733)

cv2.createTrackbar("threshold1", "trackbar_window", 100, 600, lambda x: None)
cv2.createTrackbar("threshold2", "trackbar_window", 100, 600, lambda x: None)
cv2.createTrackbar("diameter", "trackbar_window", 9, 75, lambda x: None)
cv2.createTrackbar("sigmaColor", "trackbar_window", 75, 300, lambda x: None)
cv2.createTrackbar("sigmaSpace", "trackbar_window", 75, 150, lambda x: None)

while True:
    threshold1_pos = cv2.getTrackbarPos("threshold1", "trackbar_window")
    threshold2_pos = cv2.getTrackbarPos("threshold2", "trackbar_window")
    diameter_pos = cv2.getTrackbarPos("diameter", "trackbar_window")
    sigmaColor_pos = cv2.getTrackbarPos("sigmaColor", "trackbar_window")
    sigmaSpace_pos = cv2.getTrackbarPos("sigmaSpace", "trackbar_window")

    # To avoid undefined behavior
    if diameter_pos == 0:
        diameter_pos = 1

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, diameter_pos, sigmaColor_pos, sigmaSpace_pos)
    edged = cv2.Canny(gray, threshold1_pos, threshold2_pos)

    cv2.imshow("trackbar_window", edged)
    cv2.imshow("original_image", img_original)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break

print(f"\chose: \n threshold1: {threshold1_pos}, threshold2: {threshold2_pos}, diameter: {diameter_pos}, sigmaColor: {sigmaColor_pos}, sigmaSpace: {sigmaSpace_pos}")

# Find contours, hierarchy is not used
contours, hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Sort contours by area, biggest first
contours = sorted(contours, key = cv2.contourArea, reverse = True)

#Finds the contour with 4 corners with the biggest area
filtered = utils.contour_filtering(contours)

# Sometimes method doesn't find 4 corners, then return error
if filtered.size == 0:
    print("No 4 vertices found! Exiting..")
    exit(1)

# Draw the biggest 4 corner contour
cv2.drawContours(img, [filtered], -1, (0, 255, 0), 3)

top_left, top_right, bottom_right, bottom_left, corner_points = utils.get_corner_points(filtered)
print("topleft",top_left)
# Draw circles on the corners
utils.draw_circles_on_corners(img, corner_points, circle_radius=40, line_thickness=5)

# What we want to warp to
width_warped = 700
height_warped = 700

# converted points 
converted_points = np.array([[0,0], [width_warped, 0], [width_warped, height_warped], [0, height_warped]], dtype="float32")
# perspective transformation
matrix = cv2.getPerspectiveTransform(corner_points, converted_points)
img_output = cv2.warpPerspective(img_original, matrix, (width_warped, height_warped))

# ----------------- Displaying --------------
# Define the desired width and height for display

# Image shape modification (the two dont include the channel)
gray = np.stack((gray,)*3, axis=-1) 
edged = np.stack((edged,)*3, axis=-1)

# Image stacking, få alle på ett vindu
img_hor = np.hstack((img_original, gray, edged, img))
# skaler ned ellers tar det hele skjermen
cv2.namedWindow("step_by_step", cv2.WINDOW_NORMAL) #så ikke zoomed-in
cv2.resizeWindow("step_by_step", 500*3, 667*3) 
cv2.imshow("step_by_step", img_hor)

cv2.namedWindow("warped_perspective", cv2.WINDOW_NORMAL)

cv2.resizeWindow("warped_perspective", width_warped, height_warped)
cv2.imshow("warped_perspective", img_output)
cv2.imwrite("ryddet mappe/images/test.jpg", img_output)

cv2.waitKey(0)