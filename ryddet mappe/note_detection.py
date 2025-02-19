import cv2
import numpy as np 
from matplotlib import pyplot as plt

# import functions from note_utils.py
import note_utils as utils
    
# Read the image and modify it
img = cv2.imread('ryddet mappe/images/warped_image.jpg')
# img = cv2.resize(img, (700,700))
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
gray = cv2.bitwise_not(gray)
edges = cv2.Canny(gray,150,250)

gris = utils.removeLines(gray)
gris = cv2.bitwise_not(gris)
params = utils.getNoteDetectParams(400,1500)

# Create a notedetector with the parameters 
noteDetector = cv2.SimpleBlobDetector_create(params) 	
# Detect ellipse like shape in the binary image (gris) from the parameters given to the notedetector
keypoints = noteDetector.detect(gris) 
# marks detected notes with red dots
circles = []
radius = 8
for note in cv2.KeyPoint_convert(keypoints):
    img = cv2.circle(img, (round(note[0]),round(note[1])), radius, color=(0,0,255), thickness=-1)
    circles.append((int(note[0]),int(note[1]),radius))
cv2.imshow("Notes found", img)
cv2.imshow("gris", gris)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Find the lines in the image using the hough transform (output is in polar coordinates)
lines_ro_theta = cv2.HoughLines(edges,1,np.pi/180,200) # 200 is the threshold

lines_x_y = []
for line in lines_ro_theta:
    for rho,theta in line:
        # +-30 degrees buffer from linewidth if lines are not perfectly horizontal.
        epsilon = np.pi/6 
        wanted_angle = np.pi/2
        # Filter out lines that are not horizontal
        if theta < (wanted_angle - epsilon) or theta > (wanted_angle + epsilon): 
            continue 

        # calculate the x and y starting/ending coordinates of the lines from the rho and theta
        x1, y1, x2, y2 = utils.getLinePosition(rho, theta)
        lines_x_y.append((x1,y1,x2,y2, rho, theta))

close_threshold = 30
filtered_lines = utils.remove_close_lines(lines_x_y, close_threshold, img)

for line in filtered_lines:
    x1, y1, x2, y2, rho, theta = line
    # Filter out lines that occur at the edge of the image
    filtered_lines = [line for line in filtered_lines if line[3] < img.shape[1] - 10]
    # Filter out lines that occur at the top of the image
    filtered_lines = [line for line in filtered_lines if line[1] > 0]

# Sort lines by rho value (distance from origin)
sorted_lines = sorted(filtered_lines, key=lambda x: x[4], reverse=True)
line_spacing = sorted_lines[0][3]-sorted_lines[1][3]
# Draw the lines on the image
for line in sorted_lines:
    x1, y1, x2, y2, rho, theta = line
    cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

# Split the lines into groups of 5 (5 lines per staff)
split_lines = [sorted_lines[i:i+5] for i in range(0, len(sorted_lines), 5)]

# Add note position to every line
note_index = 1
for sublist in split_lines:
    for index, tup in enumerate(sublist):
        sublist[index] = tup + (note_index,)
        note_index += 1
        if note_index > 5:
            note_index = 1

# Add clef boolean value to every line
for i in range(len(split_lines)):
    if i % 2 == 0:
        g_staff = False
    else:
        g_staff = True
    for j in range(len(split_lines[i])):
        split_lines[i][j] = split_lines[i][j] + (g_staff,)

# Draw manual circles on the image to show note detection logic
circle_positions = [(200, 30, 14), (200, 70, 14), (200, 680, 14), (200, 640, 14)]
for circle in circle_positions:
    cv2.circle(img, (circle[0], circle[1]), circle[2], (0, 0, 255), -1)
    circles.append((circle[0], circle[1], circle[2]))

# Draw the notes on the image
for circle in circles:

    no_intersection_found = True
    g_clef = True
    (x_c,y_c,r) = circle

    # Find line spacing (could add average)
    line_spacing = split_lines[0][0][3]-split_lines[0][1][3]

    smallest_distance = float("inf")
    distance_info = ()
    distances_info = []
    closest_line_gclef = None

    for line in split_lines:
        for x1, y1, x2, y2, rho, theta, line_pos, g_clef in line:
            distance = abs(int(y2) - int(y_c))
            distance_info = (distance, line_pos, y2, g_clef)
            distances_info.append(distance_info)

    # Sort the distances_info list by distance from the note to the line
    distances_info_sorted = sorted(distances_info, key=lambda x: x[0])

    # Extract the closest and second closest line parameters
    closest_line_pos = distances_info_sorted[0][1]
    second_closest_line_pos = distances_info_sorted[1][1]
    closest_line_gclef = distances_info_sorted[0][3]
    closest_line_yvalue = distances_info_sorted[0][2]

    # Get the clef of the closest line
    if closest_line_gclef is not None:
        g_clef = closest_line_gclef

    for line in split_lines:
        for x1,y1,x2,y2,rho,theta,line_pos,_ in line:
            intersect = utils.line_circle_intersection((x1,y1),(x2,y2),(x_c,y_c),r)
            
            if intersect and g_clef:
                no_intersection_found = False
                utils.draw_notes_intersetion_gclef(img, line_pos, x_c, y_c)

            if intersect and not g_clef:
                no_intersection_found = False
                utils.draw_notes_intersetion_fclef(img, line_pos, x_c, y_c)

    if no_intersection_found and g_clef:
        utils.draw_notes_no_intersection_gclef(split_lines, img, x_c, y_c, line_spacing, closest_line_pos, closest_line_yvalue, second_closest_line_pos)

    if no_intersection_found and not g_clef:
        utils.draw_notes_no_intersection_fclef(split_lines, img, x_c, y_c, line_spacing, closest_line_pos, closest_line_yvalue, second_closest_line_pos)

# So it's not zoomed in
cv2.namedWindow("hough", cv2.WINDOW_NORMAL) 

# Resize the window to fit screen
if img.shape[0] > 650:
    width = 700
else:
    width = img.shape[0]

if img.shape[1] > 650:
    height = 650
else:
    height = img.shape[1]

cv2.resizeWindow("hough", width, height) 
cv2.imshow('hough',img)
cv2.imwrite('notes_found.jpg', img)
cv2.waitKey(0)
