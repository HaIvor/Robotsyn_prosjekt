import cv2
import numpy as np

img = cv2.imread("assets/pult.jpg")
img = cv2.imread("assets/rotated_maad.jpg")
img = cv2.imread("assets/martin.jpg")
img = ~img
# img = cv2.imread("assets/jingle_iphone (1).jpg")
# img = cv2.imread("assets/test.jpg")
# img = cv2.imread("assets/christ_iphone (1).jpg")
# img = cv2.imread("assets/enter_iphone (4).jpg")
img_original = img.copy()

# Image modification
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Convert to grayscale
#bilateralFilter(src, diameter , sigmaColor, sigmaSpace[, dst[, borderType]]) -> dst
gray = cv2.bilateralFilter(gray, 4, 94, 70) # Smoothen the image with bilateral filter

# Search for edges
# Canny(image, threshhold1, threshhold2) -> edges
edged = cv2.Canny(gray, 268, 148)

# Trackbar for choosing parameters
cv2.namedWindow("trackbar_window", cv2.WINDOW_NORMAL)
cv2.namedWindow("original_image", cv2.WINDOW_NORMAL)
cv2.createTrackbar("threshold1", "trackbar_window", 722, 900, lambda x: None)
cv2.createTrackbar("threshold2", "trackbar_window", 538, 900, lambda x: None)
cv2.createTrackbar("diameter", "trackbar_window", 9, 75, lambda x: None)
cv2.createTrackbar("sigmaColor", "trackbar_window", 79, 150, lambda x: None)
cv2.createTrackbar("sigmaSpace", "trackbar_window", 75, 150, lambda x: None)

while True:
    cv2.imshow("trackbar_window", edged)
    cv2.imshow("original_image", img_original)
    cv2.resizeWindow("trackbar_window", 500, 667)
    cv2.resizeWindow("original_image", 550, 733)
    threshold1_pos = cv2.getTrackbarPos("threshold1", "trackbar_window")
    threshold2_pos = cv2.getTrackbarPos("threshold2", "trackbar_window")
    diameter_pos = cv2.getTrackbarPos("diameter", "trackbar_window")
    sigmaColor_pos = cv2.getTrackbarPos("sigmaColor", "trackbar_window")
    sigmaSpace_pos = cv2.getTrackbarPos("sigmaSpace", "trackbar_window")
    #so doesnt crash..
    if diameter_pos == 0:
        diameter_pos = 1
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, diameter_pos, sigmaColor_pos, sigmaSpace_pos)
    edged = cv2.Canny(gray, threshold1_pos, threshold2_pos)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
print(f"threshold1: {threshold1_pos}, threshold2: {threshold2_pos}, diameter: {diameter_pos}, sigmaColor: {sigmaColor_pos}, sigmaSpace: {sigmaSpace_pos}")

contours, hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)#edged.copy()?

contours = sorted(contours, key = cv2.contourArea, reverse = True)[:80]

for contour in contours:
    peri  = cv2.arcLength(contour, True)
    epsilon = 0.1 * peri
    approx = cv2.approxPolyDP(contour, epsilon, True)
    # cv2.drawContours(img, [contour], -1, (0, 255, 0), 3)
    if len(approx) == 4:
        print("Hei")
        cv2.drawContours(img, [contour], -1, (0, 255, 0), 3)

# draws all contours! comment away maybe
# for i in contours:
#     cv2.drawContours(img, [i], -1, (0, 255, 0), 3)

width = 500
height = 500

# Define the desired width and height for display
desired_width = 500
desired_height = 667

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
cv2.resizeWindow("warped_perspective", 1000, 1000)
cv2.imshow("warped_perspective", img)
print("wtf")
cv2.imwrite("assets/circle_contours.jpg", img)
cv2.waitKey(0)