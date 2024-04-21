import cv2
import numpy as np 
from matplotlib import pyplot as plt

# import lineDetection as lines
import note_utils as utils
    
img = cv2.imread('assets/halvor.jpg')
img = cv2.resize(img, (700,700))
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,150,250)
# cv2.imshow('hough',edges)

gris = utils.removeLines(edges)
params = utils.getNoteDetectParams(400,1500)

# Create a notedetector with the parameters 
noteDetector = cv2.SimpleBlobDetector_create(params) 	
# Detect ellipse like shape in the binary image (gris) from the parameters given to the notedetector
keypoints = noteDetector.detect(gris) 
# marks detected notes with red dots
circles = []
radius = 8
for note in cv2.KeyPoint_convert(keypoints):
    image = cv2.circle(img, (round(note[0]),round(note[1])), radius, color=(0,0,255), thickness=-1)
    circles.append((int(note[0]),int(note[1]),radius))
cv2.imshow("Notes found", img)

cv2.waitKey(0)
# Find the lines in the image using the hough transform (output is in polar coordinates)
lines_ro_theta = cv2.HoughLines(edges,1,np.pi/180,200) # 200 is the threshold

lines_x_y = []
for line in lines_ro_theta:
    for rho,theta in line:
        # +-30 degrees buffer from linewidth if lines are not perfectly horizontal.
        epsilon = np.pi/6 
        wanted_angle = np.pi/2
        # Filter out lines that are not horizontal
        if theta < wanted_angle - epsilon or theta > wanted_angle + epsilon: continue 

        # calculate the x and y coordinates of the lines from the rho and theta
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 2000*(-b))
        y1 = int(y0 + 2000*(a))
        x2 = int(x0 - 2000*(-b))
        y2 = int(y0 - 2000*(a))
        lines_x_y.append((x1,y1,x2,y2, rho, theta))

close_threshold = 30
filtered_lines = utils.remove_close_lines(lines_x_y, close_threshold, img)

sorted_lines = sorted(filtered_lines, key=lambda x: x[4], reverse=True)

# Draw the lines!
#test
print("Hei")
for line in sorted_lines:
    x1, y1, x2, y2, rho, theta = line
    cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

split_lines = [sorted_lines[i:i+5] for i in range(0, len(sorted_lines), 5)]

value_to_add = 1
for sublist in split_lines:
    for index, tup in enumerate(sublist):
        sublist[index] = tup + (value_to_add,)
        value_to_add += 1
        if value_to_add > 5:
            value_to_add = 1

for i in range(len(split_lines)):
    if i % 2 == 0:
        g_staff = False
    else:
        g_staff = True
    for j in range(len(split_lines[i])):
        split_lines[i][j] = split_lines[i][j] + (g_staff,)

circle2 = (200,30,14)
cv2.circle(img, (circle2[0],circle2[1]),circle2[2],(0,0,255),-1)
circles.append((circle2[0],circle2[1],circle2[2]))

circle1 = (200,70,14)
cv2.circle(img, (circle1[0],circle1[1]),circle1[2],(0,0,255),-1)
circles.append((circle1[0],circle1[1],circle1[2]))

circle3 = (200,680,14)
cv2.circle(img, (circle3[0],circle3[1]),circle3[2],(0,0,255),-1)
circles.append((circle3[0],circle3[1],circle3[2]))

circle4 = (200,640,14)
cv2.circle(img, (circle4[0],circle4[1]),circle4[2],(0,0,255),-1)
circles.append((circle4[0],circle4[1],circle4[2]))

for circle in circles:
    no_intersection_found = True
    (x_c,y_c,r) = circle
    g_clef = True

    line_spacing = split_lines[0][0][3]-split_lines[0][1][3]

    closest_line = None
    closest_distance = float('inf')

    for line in split_lines:
        for x1, y1, x2, y2, rho, theta, note_pos, g_clef in line:
            distance = abs(y_c - ((y1 + y2) / 2))
            if distance < closest_distance:
                closest_distance = distance
                closest_line = line
    
    if closest_line is not None:
        g_clef = closest_line[0][-1]

    for line in split_lines:
        for x1,y1,x2,y2,rho,theta,note_pos,geir in line:
            intersect = utils.line_circle_intersection((x1,y1),(x2,y2),(x_c,y_c),r)
            
            if intersect and g_clef:
                no_intersection_found = False
                utils.draw_notes_intersetion_gclef(img, note_pos, x_c, y_c)

            if intersect and not g_clef:
                no_intersection_found = False
                utils.draw_notes_intersetion_fclef(img, note_pos, x_c, y_c)

    if no_intersection_found and g_clef:
        utils.draw_notes_no_intersection_gclef(split_lines, img, x_c, y_c, line_spacing)

    if no_intersection_found and not g_clef:
        utils.draw_notes_no_intersection_fclef(split_lines, img, x_c, y_c, line_spacing)

cv2.namedWindow("hough", cv2.WINDOW_NORMAL) #så ikke zoomed-in
cv2.resizeWindow("hough", img.shape[0]-200, img.shape[1]-130) 
cv2.imshow('hough',img)
cv2.imwrite('notes_found.jpg', img)
cv2.waitKey(0)