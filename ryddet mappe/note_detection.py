import cv2
import numpy as np 
from matplotlib import pyplot as plt

# import lineDetection as lines
import note_utils as utils

def line_circle_intersection(line_start, line_end, circle_center, circle_radius):
    # Vector representation of the line
    line_vec = np.array(line_end) - np.array(line_start)
    
    # Vector from line start to circle center
    start_to_center = np.array(circle_center) - np.array(line_start)
    
    # Projection of start_to_center vector onto line_vec
    projection = np.dot(start_to_center, line_vec) / np.dot(line_vec, line_vec) * line_vec
    
    # Closest point on the line to the circle center
    closest_point = np.array(line_start) + projection
    
    # Distance between closest point and circle center
    distance = np.linalg.norm(closest_point - circle_center)
    
    # If the distance is less than or equal to the circle radius, there's an intersection
    if distance <= circle_radius:
        return True
    else:
        return False
    
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
    # if note[1] > 500: continue
    image = cv2.circle(img, (round(note[0]),round(note[1])), radius, color=(0,0,255), thickness=-1)
    circles.append((int(note[0]),int(note[1]),radius))
cv2.imshow("Notes found", img)
#bruteforce circle for now
#(300,210,14) -> bugs to be A...ok if switch to y2..
# circle1 = (300,210,14)
# cv2.circle(img, (circle1[0],circle1[1]),circle1[2],(0,0,255),-1)
# circles.append((circle1[0],circle1[1],circle1[2]))
# print(circles)

cv2.waitKey(0)
lines_ro_theta = cv2.HoughLines(edges,1,np.pi/180,200) # 200 is the threshold
# print(lines_ro_theta)
lines_x_y = []
for line in lines_ro_theta:
    for rho,theta in line:
        epsilon = np.pi/4 # +-45 degrees buffer from linewidth
        # If vertical line:continue
        # if theta < np.pi/2 - epsilon or theta > np.pi/2 + epsilon: continue 
        wanted_angle = np.pi/2
        # If horizontal line: continue
        if theta < wanted_angle - epsilon or theta > wanted_angle + epsilon: continue 

        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 2000*(-b))
        y1 = int(y0 + 2000*(a))
        x2 = int(x0 - 2000*(-b))
        y2 = int(y0 - 2000*(a))
        lines_x_y.append((x1,y1,x2,y2, rho, theta))


def remove_close_lines(lines, treshold):
    filter_lines = [lines[0]]
    for line in lines:
        is_close = check_close_line(line,filter_lines,treshold)
        if not is_close: filter_lines.append(line)
    return filter_lines

def check_close_line(line,filter_lines,treshold):
    x1,y1,x2,y2, rho, theta = line
    avg_y = (y1 + y2) / 2
    for filter_line in filter_lines:
        avg_y_filter = (filter_line[1] + filter_line[3]) / 2
        #True: close line, False: not close line
        #last two conditions are for lines that are close to the top or bottom of the image
        if abs(avg_y - avg_y_filter) < treshold or abs(y1 - img.shape[0]) < 20 or (y1 < 20): 
            return True
    return False

filtered_lines = remove_close_lines(lines_x_y,30)
# print(len(filtered_lines))

for lin in filtered_lines:
    x1,y1,x2,y2,rho,theta = lin
    sorted_lines = sorted(filtered_lines, key=lambda x: x[4], reverse=True)
    
    for lin in sorted_lines:
        x1, y1, x2, y2, rho, theta = lin
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
    cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)
# print("number of lines:", len(sorted_lines))
#split into 5 lines
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

# print("split_lines:", split_lines)
print("\nsplit_lines:\n", split_lines)
print("\n\n\n")
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
# print(len(circles))
# Classify notes
# cv2.circle(img, (333, 333), 8, (255, 0, 0), -1)
# cv2.circle(img, (730, 557), 8, (0, 0, 230), -1)

# print("hei:",circles)
for circle in circles:
    no_intersection_found = True
    (x_c,y_c,r) = circle
    g_clef = True

    # print("split_lines123",split_lines)
    # print(split_lines[0])
    #y pos first line
    # print(split_lines[0][0][3])
    line_spacing = split_lines[0][0][3]-split_lines[0][1][3]

    closest_line = None
    closest_distance = float('inf')
    for line in split_lines:
        # print(line)
        for x1, y1, x2, y2, rho, theta, note_pos, g_clef in line:
            distance = abs(y_c - ((y1 + y2) / 2))
            if distance < closest_distance:
                closest_distance = distance
                closest_line = line
    
    if closest_line is not None:
        g_clef = closest_line[0][-1]
    print(g_clef)

    for line in split_lines:
        for x1,y1,x2,y2,rho,theta,note_pos,geir in line:
            intersect = line_circle_intersection((x1,y1),(x2,y2),(x_c,y_c),r)
            
            if intersect and g_clef:
                no_intersection_found = False
                # print(f"intersection at note_pos {note_pos}")
                utils.draw_notes_intersetion_gclef(img, note_pos, x_c, y_c)
            if intersect and not g_clef:
                no_intersection_found = False
                # print(f"intersection at note_pos {note_pos}")
                utils.draw_notes_intersetion_fclef(img, note_pos, x_c, y_c)
    if no_intersection_found and g_clef:
        utils.draw_notes_no_intersection_gclef(split_lines, img, x_c, y_c, line_spacing)
    if no_intersection_found and not g_clef:
        utils.draw_notes_no_intersection_fclef(split_lines, img, x_c, y_c, line_spacing)
# print("\n\n",split_lines)
cv2.namedWindow("hough", cv2.WINDOW_NORMAL) #så ikke zoomed-in
cv2.resizeWindow("hough", img.shape[0]-200, img.shape[1]-130) 
cv2.imshow('hough',img)
cv2.imwrite('notes_found.jpg', img)
cv2.waitKey(0)
