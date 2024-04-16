import cv2
import numpy as np

def contour_filtering(contours):
    biggest = np.array([])
    max_area = 0
    for i in contours:
        area = cv2.contourArea(i) # area in pixels
        if area > 1000:
            peri  = cv2.arcLength(i, True)
            print("peri: ", peri)
            #epsilon: approximation accuracy, True: closed contour
            epsilon = 0.02 * peri
            print("epsilon: ", epsilon)
            approx = cv2.approxPolyDP(i, epsilon, True)
            if area > max_area and len(approx) == 4:
                biggest = approx
                max_area = area
    return biggest

img = cv2.imread("assets/pult.jpg")
img = cv2.imread("assets/rotated_maad.jpg")
img = cv2.imread("assets/abc_iphone (3).jpg")
img = cv2.imread("assets/jingle_iphone (1).jpg")
# img = cv2.imread("assets/test.jpg")
img = cv2.imread("assets/christ_iphone (1).jpg")
# img = cv2.imread("assets/enter_iphone (4).jpg")
img_original = img.copy()

# Image modification
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Convert to grayscale
#bilateralFilter(src, diameter , sigmaColor, sigmaSpace[, dst[, borderType]]) -> dst
gray = cv2.bilateralFilter(gray, 4, 94, 70) # Smoothen the image with bilateral filter

# Search for edges
# Canny(image, threshhold1, threshhold2) -> edges
edged = cv2.Canny(gray, 268, 148)

#opencv documentation
contours, hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)#edged.copy()?

# sorterer contours etter størrelse, sort descending, tar de 10 største
contours = sorted(contours, key = cv2.contourArea, reverse = True)[:10]

# draws all contours! comment away maybe
# for i in contours:
#     cv2.drawContours(img, [i], -1, (0, 255, 0), 3)

#check if as 4 corners and biggest area
biggest = contour_filtering(contours)

cv2.drawContours(img, [biggest], -1, (0, 255, 0), 3)

# pixel values in the original image (corners)
points = biggest.reshape(4,2)
input_points = np.zeros((4,2), dtype="float32")

points_sum = points.sum(axis=1)
input_points[0] = points[np.argmin(points_sum)]
input_points[2] = points[np.argmax(points_sum)]

points_diff = np.diff(points, axis=1)
input_points[1] = points[np.argmin(points_diff)]
input_points[3] = points[np.argmax(points_diff)]

(top_left, top_right, bottom_right, bottom_left) = input_points
# Draw red circles over each point
cv2.circle(img, tuple(map(int, top_left)), 40, (0, 0, 255), 5)
cv2.circle(img, tuple(map(int, top_right)), 40, (0, 0, 255), 5)
cv2.circle(img, tuple(map(int, bottom_right)), 40, (0, 0, 255), 5)
cv2.circle(img, tuple(map(int, bottom_left)), 40, (0, 0, 255), 5)

print(top_left)
print(top_right)
print(bottom_right)
print(bottom_left)

bottom_width = np.sqrt(((bottom_right[0] - bottom_left[0]) ** 2) + ((bottom_right[1] - bottom_left[1]) ** 2))
top_width = np.sqrt(((top_right[0] - top_left[0]) ** 2) + ((top_right[1] - top_left[1]) ** 2))
right_height = np.sqrt(((top_right[0] - bottom_right[0]) ** 2) + ((top_right[1] - bottom_right[1]) ** 2))
left_height = np.sqrt(((top_left[0] - bottom_left[0]) ** 2) + ((top_left[1] - bottom_left[1]) ** 2))

#output image size 
max_width = max(int(bottom_width), int(top_width))
max_height = max(int(right_height), int(left_height))
print(f"max_width: {max_width}, max_height: {max_height}")

# converted points 
converted_points = np.array([[0,0], [max_width-1, 0], [max_width-1, max_height-1], [0, max_height-1]], dtype="float32")
width = 500
height = 500

# converted_points = np.array([[0,0], [width-1, 0], [width-1, height-1], [0, height-1]], dtype="float32")

# perspective transformation
matrix = cv2.getPerspectiveTransform(input_points, converted_points)
img_output = cv2.warpPerspective(img_original, matrix, (max_width, max_height))

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
cv2.namedWindow("original_resized", cv2.WINDOW_NORMAL) #så ikke zoomed-in
cv2.resizeWindow("original_resized", 500*3, 667*3) 
cv2.imshow("original_resized", img_hor)
cv2.imwrite("output2.jpg", img_output)
cv2.namedWindow("warped_perspective", cv2.WINDOW_NORMAL)
if max_width > 500:
    max_width = 500 
if max_height > 500:
    max_height = 500
cv2.resizeWindow("warped_perspective", max_width, max_height)
cv2.imshow("warped_perspective", img_output)

# cv2.namedWindow("original_resized", cv2.WINDOW_NORMAL) 
# cv2.resizeWindow("original_resized", 500, 667) 

# cv2.namedWindow("gray_resized", cv2.WINDOW_NORMAL)
# cv2.resizeWindow("gray_resized", 500, 667)

# cv2.namedWindow("edged_resized", cv2.WINDOW_NORMAL)
# cv2.resizeWindow("edged_resized", 500, 667)


# cv2.imshow("original_resized", img_original)
# cv2.imshow("gray_resized", gray)
# cv2.imshow("edged_resized", edged)

cv2.waitKey(0)