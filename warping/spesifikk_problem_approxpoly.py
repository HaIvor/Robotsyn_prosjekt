import cv2
import numpy as np

def contour_filtering(contours):
    biggest = np.array([])
    max_area = 0
    for i in contours:
        area = cv2.contourArea(i) # area in pixels
        if area > 2000:
            peri  = cv2.arcLength(i, True)
            print("peri: ", peri)
            #epsilon: approximation accuracy, True: closed contour
            epsilon = 0.01 * peri
            print("epsilon: ", epsilon)
            approx = cv2.approxPolyDP(i, epsilon, True)
            if area > max_area and len(approx) == 4:
                biggest = approx
                max_area = area
    return biggest

img = cv2.imread("assets/pult.jpg")
img = cv2.imread("assets/rotated_maad.jpg")
img = cv2.imread("assets/abc_iphone (4).jpg")
# img = cv2.imread("assets/jingle_iphone (5).jpg")
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
cv2.createTrackbar("threshold1", "trackbar_window", 143, 600, lambda x: None)
cv2.createTrackbar("threshold2", "trackbar_window", 26, 600, lambda x: None)
cv2.createTrackbar("diameter", "trackbar_window", 8, 30, lambda x: None)
cv2.createTrackbar("sigmaColor", "trackbar_window", 90, 150, lambda x: None)
cv2.createTrackbar("sigmaSpace", "trackbar_window", 75, 150, lambda x: None)

while True:
    cv2.imshow("trackbar_window", edged)
    cv2.imshow("original_image", img_original)
    cv2.resizeWindow("trackbar_window", 500, 667)
    cv2.resizeWindow("original_image", 450, 633)
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
#opencv documentation
contours, hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)#edged.copy()?

# sorterer contours etter størrelse, sort descending, tar de 10 største
contours = sorted(contours, key = cv2.contourArea, reverse = True)[:8]
k=1
for i in contours:
    #detta e rett contour, koffår e den 7.?
    
    if k==7:
        cv2.drawContours(img, [i], -1, (0, 255, 0), 3)
        peri  = cv2.arcLength(i, True)
        stop=0
        approx = [0, 0]
        value = 0.001
        while len(approx) != 4 and stop<40000:
            epsilon = value * peri
            approx = cv2.approxPolyDP(i, epsilon, True)
            value = value + 0.001
            stop=stop+1
        print("hei",value)
        print(len(approx))
        print("stop", stop)
        epsilon = 0.0555 * peri
        area = cv2.contourArea(i)
        approx = cv2.approxPolyDP(i, epsilon, True)
        print("peri7: ", peri)
        print("area7: ", area)
        print("approx7: ", approx)
        print("approx7 length: ", len(approx))
    if k==1:
        #cv2.drawContours(img, [i], -1, (0, 255, 0), 3)
        peri  = cv2.arcLength(i, True)
        epsilon = 0.02 * peri
        area = cv2.contourArea(i)
        approx = cv2.approxPolyDP(i, epsilon, True)
        print("peri1: ", peri)
        print("area1: ", area)
        print("approx1: ", approx)
    k=k+1
    # Draw points on the image
    points = np.array([[[1785, 1452]], [[385, 2015]], [[1051, 2187]], [[1784, 1454]], [[1050, 2187]], [[385, 2011]]])
    for point in points:
        cv2.circle(img, tuple(point[0]), 10, (0, 0, 255), 4)

cv2.namedWindow("step_by_step", cv2.WINDOW_NORMAL) #så ikke zoomed-in
cv2.resizeWindow("step_by_step",400, 547) 
cv2.imshow("step_by_step", img)
#check if as 4 corners and biggest area
#biggest = contour_filtering(contours)
cv2.waitKey(0)