import cv2
import numpy as np 

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
    
img = cv2.imread('assets/martin.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,50,150,apertureSize = 3)
# cv2.imshow('hough',edges)
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
# print("split_lines:", split_lines)
circles = []
#bruteforce circle for now
#(300,210,14) -> bugs to be A...ok if switch to y2..
circle1 = (300,213,14)
cv2.circle(img, (circle1[0],circle1[1]),circle1[2],(0,0,255),-1)
circles.append((circle1[0],circle1[1],circle1[2]))

circle2 = (300,100,14)
cv2.circle(img, (circle2[0],circle2[1]),circle2[2],(0,0,255),-1)
circles.append((circle2[0],circle2[1],circle2[2]))

# Classify notes
for circle in circles:
    no_intersection_found = True
    (x_c,y_c,r) = circle
    for line in split_lines:
        for x1,y1,x2,y2,rho,theta,note_pos in line:
            intersect = line_circle_intersection((x1,y1),(x2,y2),(x_c,y_c),r)
            if intersect:
                no_intersection_found = False
                print(f"intersection at note_pos {note_pos}")
                if note_pos == 1:
                    print("note is a E")
                elif note_pos == 2:
                    print("note is a G")
                elif note_pos == 3:
                    print("note is a B")   
                elif note_pos == 4:
                    print("note is a D")
                elif note_pos == 5:
                    print("note is a F")
    if no_intersection_found:
        #code for notes in between lines
        for line in split_lines:
            smallest_distance = 1000000
            distances_info = []
            distance_info = ()
            for x1,y1,x2,y2,rho,theta,note_pos in line:
                distance = abs(y2-y_c)
                distance_info = (distance, note_pos, y1)
                distances_info.append(distance_info)
        # print("distances_info:",distances_info)
        distances_info_sorted = sorted(distances_info, key=lambda x: x[0])
        # print("distances_info_sorted:",distances_info_sorted)
        closest_note_pos = distances_info_sorted[0][1]
        second_closest_note_pos = distances_info_sorted[1][1]
        if closest_note_pos == 1 and (y_c > distances_info_sorted[0][2]):
            print("Note is D (bottom)")
            break
        if closest_note_pos == 5 and (y_c < distances_info_sorted[0][2]):
            print("Note is G (top)")
            break
        # print("closest_note_pos and second_closest_note_pos:",closest_note_pos,second_closest_note_pos)
        # print("distances_info_sorted",distances_info_sorted)
        if closest_note_pos == 1 and second_closest_note_pos == 2 or closest_note_pos == 2 and second_closest_note_pos == 1:
            print("note is a F")
        elif closest_note_pos == 2 and second_closest_note_pos == 3 or closest_note_pos == 3 and second_closest_note_pos == 2:
            print("note is a A.")
        elif closest_note_pos == 3 and second_closest_note_pos == 4 or closest_note_pos == 4 and second_closest_note_pos == 3:
            print("note is a C")
        elif closest_note_pos == 4 and second_closest_note_pos == 5 or closest_note_pos == 5 and second_closest_note_pos == 4:
            print("note is a E")
        # print("No intersection found")
# print("\n\n",split_lines)
cv2.namedWindow("hough", cv2.WINDOW_NORMAL) #så ikke zoomed-in
cv2.resizeWindow("hough", img.shape[0]-200, img.shape[1]-130) 
cv2.imshow('hough',img)
cv2.waitKey(0)
