import cv2
import numpy as np

def contour_filtering(contours):
    filtered = np.array([])
    max_area = 0
    for contour in contours:
        # area in pixels
        area = cv2.contourArea(contour) 
        if area > 2000:
            peri  = cv2.arcLength(contour, True)
            #epsilon: approximation accuracy (smaller -> more accurate)
            epsilon = 0.02 * peri
            approx = cv2.approxPolyDP(contour, epsilon, True)
            # if somewhat big area and 4 corners
            if area > max_area and len(approx) == 4:
                filtered = approx
                max_area = area
    return filtered

def get_corner_points(filtered):
    # pixel values of the corners of the biggest contour
    points = filtered.reshape(4,2)
    print(points)
    corner_points = np.zeros((4,2), dtype="float32")

    # points_sum = x + y
    points_sum = points.sum(axis=1)
    corner_points[0] = points[np.argmin(points_sum)]
    corner_points[2] = points[np.argmax(points_sum)]

    # points_diff = x - y
    points_diff = np.diff(points, axis=1)
    corner_points[1] = points[np.argmin(points_diff)]
    corner_points[3] = points[np.argmax(points_diff)]

    top_left, top_right, bottom_right, bottom_left = corner_points

    return top_left, top_right, bottom_right, bottom_left, corner_points

def draw_circles_on_corners(img, corner_points, circle_radius, line_thickness):

    # convert corner points from floats to integers
    corner_points = corner_points.astype(int)
    top_left, top_right, bottom_right, bottom_left = corner_points

    cv2.circle(img, (top_left[0], top_left[1]), circle_radius, (0, 0, 255), line_thickness)
    cv2.circle(img, (top_right[0], top_right[1]), circle_radius, (0, 0, 255), line_thickness)
    cv2.circle(img, (bottom_right[0], bottom_right[1]), circle_radius, (0, 0, 255), line_thickness)
    cv2.circle(img, (bottom_left[0], bottom_left[1]), circle_radius, (0, 0, 255), line_thickness)