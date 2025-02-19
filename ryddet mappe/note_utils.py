import cv2 
import numpy as np 
def removeLines(imageCanny):
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7,7))#kernel for rectangle
	imageNoLines = cv2.morphologyEx(imageCanny, cv2.MORPH_OPEN, kernel)#fills inn lines

	imageNoLines = cv2.threshold(imageNoLines,150,255,cv2.THRESH_BINARY)[1]

	return imageNoLines

def getNoteDetectParams(minAreal,maxAreal):
	#filter for a note like shape (ellipse)
	params = cv2.SimpleBlobDetector_Params() 

	# Set Area 
	params.filterByArea = True
	params.minArea = minAreal
	params.maxArea = maxAreal

	# Set Circularity 
	params.filterByCircularity = True
	params.minCircularity = 0.63
	params.maxCircularity = 0.9

	# Set Convexity (the larger -> more like a cricle)
	params.filterByConvexity = True
	params.minConvexity = 0.84
		
	# Set inertia (this gives ellipse like shape between zero and one i think... cicle is 1)
	params.filterByInertia = True
	params.minInertiaRatio = 0.2
	params.maxInertiaRatio = 0.55
	return params

def getLinePosition(rho, theta):
    # See hough line transform theory
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    #make line 2000 pixels long
    x1 = int(x0 + 2000*(-b))
    y1 = int(y0 + 2000*(a))
    x2 = int(x0 - 2000*(-b))
    y2 = int(y0 - 2000*(a))
    return x1, y1, x2, y2

#True: close line, False: not close line
def check_close_line(line,filter_lines,treshold, img):
    x1,y1,x2,y2, rho, theta = line
    avg_y = (y1 + y2) / 2
    for filter_line in filter_lines:
        avg_y_filter = (filter_line[1] + filter_line[3]) / 2
        #last two conditions are for lines that are close to the top or bottom of the image
        if abs(avg_y - avg_y_filter) < treshold or abs(y1 - img.shape[0]) < 20 or (y1 < 20): 
            return True
    return False

# Remove lines that are close to each other
def remove_close_lines(lines, treshold, img):
    filter_lines = [lines[0]]
    for line in lines:
        is_close = check_close_line(line,filter_lines,treshold, img)
        if not is_close: filter_lines.append(line)
    return filter_lines

# True: there's an intersection between the line and the circle
def line_circle_intersection(line_start, line_end, circle_center, circle_radius):
    
    # Line in vector form
    line_vec = np.array(line_end) - np.array(line_start)
    
    # Line start to circle center vector
    start_to_center = np.array(circle_center) - np.array(line_start)
    
    # Projection, vector that goes from line start to the closest point on the line to the circle center
    projection = np.dot(start_to_center, line_vec) / np.dot(line_vec, line_vec) * line_vec

    # Closest point on the line to the circle center
    closest_point = np.array(line_start) + projection
    
    # Distance between closest point and circle center
    distance = np.linalg.norm(closest_point - circle_center)
    
    # True: there's an intersection
    if distance <= circle_radius:
        return True
    else:
        return False

# Draw notes who intersects with lines (for g clef)
def draw_notes_intersetion_gclef(img, line_pos,x_c, y_c):
    if line_pos == 1:
        print("note is a E")
        cv2.putText(img, "E", (x_c, y_c), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    elif line_pos == 2:
        print("note is a G")
        cv2.putText(img, "G", (x_c, y_c), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    elif line_pos == 3:
        print("note is a B") 
        cv2.putText(img, "B", (x_c, y_c), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)  
    elif line_pos == 4:
        print("note is a D")
        cv2.putText(img, "D", (x_c, y_c), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    elif line_pos == 5:
        print("note is a F")
        cv2.putText(img, "F", (x_c, y_c), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

# Draw notes who intersects with lines (for f clef)
def draw_notes_intersetion_fclef(img, line_pos,x_c, y_c):
    if line_pos == 1:
        print("note is a G")
        cv2.putText(img, "G,f", (x_c, y_c), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    elif line_pos == 2:
        print("note is a B")
        cv2.putText(img, "B,f", (x_c, y_c), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    elif line_pos == 3:
        print("note is a D") 
        cv2.putText(img, "D,f", (x_c, y_c), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)  
    elif line_pos == 4:
        print("note is a F")
        cv2.putText(img, "F,f", (x_c, y_c), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    elif line_pos == 5:
        print("note is a A")
        cv2.putText(img, "A,f", (x_c, y_c), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

# Draw notes in between lines and over staff (for g clef)
def draw_notes_no_intersection_gclef(split_lines, img, x_c, y_c, line_spacing, closest_line_pos, closest_line_yvalue, second_closest_line_pos):
    
    # For notes over/under the lines
    if closest_line_pos == 1 and (y_c > closest_line_yvalue) and (y_c - closest_line_yvalue < line_spacing):
        print("Note is D (bottom)")
        cv2.putText(img, "D (bottom)", (x_c, y_c), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        return
    if closest_line_pos == 1 and (y_c > closest_line_yvalue) and (y_c - closest_line_yvalue > line_spacing):
        print("Note is C (botbot)")
        cv2.putText(img, "C (botbot)", (x_c, y_c), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        return
    if closest_line_pos == 5 and (y_c < closest_line_yvalue) and (closest_line_yvalue - y_c < line_spacing):
        print("Note is G (top)")
        cv2.putText(img, "G (top)", (x_c, y_c), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        return
    if closest_line_pos == 5 and (y_c < closest_line_yvalue) and (closest_line_yvalue - y_c > line_spacing):
        print("Note is A (toptop)")
        cv2.putText(img, "A (toptop)", (x_c, y_c), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        return

    # For notes in between the lines
    if closest_line_pos == 1 and second_closest_line_pos == 2 or closest_line_pos == 2 and second_closest_line_pos == 1:
        print("note is a F")
        cv2.putText(img, "F", (x_c, y_c), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    elif closest_line_pos == 2 and second_closest_line_pos == 3 or closest_line_pos == 3 and second_closest_line_pos == 2:
        print("note is a A.")
        cv2.putText(img, "A", (x_c, y_c), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    elif closest_line_pos == 3 and second_closest_line_pos == 4 or closest_line_pos == 4 and second_closest_line_pos == 3:
        print("note is a C")
        cv2.putText(img, "C", (x_c, y_c), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    elif closest_line_pos == 4 and second_closest_line_pos == 5 or closest_line_pos == 5 and second_closest_line_pos == 4:
        print("note is a E")
        cv2.putText(img, "E", (x_c, y_c), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

# Draw notes in between lines and over staff (for f clef)
def draw_notes_no_intersection_fclef(split_lines, img, x_c, y_c, line_spacing, closest_line_pos, closest_line_yvalue, second_closest_line_pos):
    
    # For notes over/under the lines
    if closest_line_pos == 1 and (y_c > closest_line_yvalue) and (y_c - closest_line_yvalue < line_spacing):
        print("Note is F (b)")
        cv2.putText(img, "F,f (b)", (x_c, y_c), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        print("values:",x_c, y_c)
        return
    if closest_line_pos == 1 and (y_c > closest_line_yvalue) and (y_c - closest_line_yvalue > line_spacing):
        print("Note is E (bb)")
        cv2.putText(img, "E,f (bb)", (x_c, y_c), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        return
    if closest_line_pos == 5 and (y_c < closest_line_yvalue) and (closest_line_yvalue - y_c < line_spacing):
        print("Note is B (top)")
        cv2.putText(img, "B,f (t)", (x_c, y_c), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        return
    if closest_line_pos == 5 and (y_c < closest_line_yvalue) and (closest_line_yvalue - y_c > line_spacing):
        print("Note is C (toptop)")
        cv2.putText(img, "C,f (tt)", (x_c, y_c), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        return
    
    # For notes in between the lines
    if closest_line_pos == 1 and second_closest_line_pos == 2 or closest_line_pos == 2 and second_closest_line_pos == 1:
        print("note is a A")
        cv2.putText(img, "A,f", (x_c, y_c), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    elif closest_line_pos == 2 and second_closest_line_pos == 3 or closest_line_pos == 3 and second_closest_line_pos == 2:
        print("note is a C")
        cv2.putText(img, "C,f", (x_c, y_c), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    elif closest_line_pos == 3 and second_closest_line_pos == 4 or closest_line_pos == 4 and second_closest_line_pos == 3:
        print("note is a E")
        cv2.putText(img, "E,f", (x_c, y_c), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    elif closest_line_pos == 4 and second_closest_line_pos == 5 or closest_line_pos == 5 and second_closest_line_pos == 4:
        print("note is a G")
        cv2.putText(img, "G,f", (x_c, y_c), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)