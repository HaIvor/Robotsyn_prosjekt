import cv2 
import numpy as np 

def draw_notes_intersetion_gclef(img, note_pos,x_c, y_c):
    if note_pos == 1:
        print("note is a E")
        cv2.putText(img, "E", (x_c, y_c), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    elif note_pos == 2:
        print("note is a G")
        cv2.putText(img, "G", (x_c, y_c), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    elif note_pos == 3:
        print("note is a B") 
        cv2.putText(img, "B", (x_c, y_c), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)  
    elif note_pos == 4:
        print("note is a D")
        cv2.putText(img, "D", (x_c, y_c), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    elif note_pos == 5:
        print("note is a F")
        cv2.putText(img, "F", (x_c, y_c), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

def draw_notes_intersetion_fclef(img, note_pos,x_c, y_c):
    if note_pos == 1:
        print("note is a G")
        cv2.putText(img, "G,f", (x_c, y_c), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    elif note_pos == 2:
        print("note is a B")
        cv2.putText(img, "B,f", (x_c, y_c), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    elif note_pos == 3:
        print("note is a D") 
        cv2.putText(img, "D,f", (x_c, y_c), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)  
    elif note_pos == 4:
        print("note is a F")
        cv2.putText(img, "F,f", (x_c, y_c), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    elif note_pos == 5:
        print("note is a A")
        cv2.putText(img, "A,f", (x_c, y_c), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

def draw_notes_no_intersection_gclef(line, split_lines, img, x_c, y_c, line_spacing):
    #code for notes in between lines
    smallest_distance = 1000000
    distances_info = []
    distance_info = ()
    for line in split_lines:
        
        for x1,y1,x2,y2,rho,theta,note_pos in line:
            distance = abs(y2-y_c)
            distance_info = (distance, note_pos, y2)
            distances_info.append(distance_info)
    # print("distances_info:",distances_info)
    distances_info_sorted = sorted(distances_info, key=lambda x: x[0])
    # print("distances_info_sorted:",distances_info_sorted)
    closest_note_pos = distances_info_sorted[0][1]
    second_closest_note_pos = distances_info_sorted[1][1]
    if closest_note_pos == 1 and (y_c > distances_info_sorted[0][2]) and (y_c - distances_info_sorted[0][2] < line_spacing):
        print("Note is D (bottom)")
        cv2.putText(img, "D (bottom)", (x_c, y_c), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        return
    if closest_note_pos == 1 and (y_c > distances_info_sorted[0][2]) and (y_c - distances_info_sorted[0][2] > line_spacing):
        print("Note is C (botbot)")
        cv2.putText(img, "C (botbot)", (x_c, y_c), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        return
    if closest_note_pos == 5 and (y_c < distances_info_sorted[0][2]) and (distances_info_sorted[0][2] - y_c < line_spacing):
        print("Note is G (top)")
        cv2.putText(img, "G (top)", (x_c, y_c), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        return
    if closest_note_pos == 5 and (y_c < distances_info_sorted[0][2]) and (distances_info_sorted[0][2] - y_c > line_spacing):
        print("Note is A (toptop)")
        cv2.putText(img, "A (toptop)", (x_c, y_c), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        return
    
    # print("closest_note_pos and second_closest_note_pos:",closest_note_pos,second_closest_note_pos)
    # print("distances_info_sorted",distances_info_sorted)
    if closest_note_pos == 1 and second_closest_note_pos == 2 or closest_note_pos == 2 and second_closest_note_pos == 1:
        print("note is a F")
        cv2.putText(img, "F", (x_c, y_c), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    elif closest_note_pos == 2 and second_closest_note_pos == 3 or closest_note_pos == 3 and second_closest_note_pos == 2:
        print("note is a A.")
        cv2.putText(img, "A", (x_c, y_c), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    elif closest_note_pos == 3 and second_closest_note_pos == 4 or closest_note_pos == 4 and second_closest_note_pos == 3:
        print("note is a C")
        cv2.putText(img, "C", (x_c, y_c), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    elif closest_note_pos == 4 and second_closest_note_pos == 5 or closest_note_pos == 5 and second_closest_note_pos == 4:
        print("note is a E")
        cv2.putText(img, "E", (x_c, y_c), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    # print("No intersection found")

def draw_notes_no_intersection_fclef(line, split_lines, img, x_c, y_c, line_spacing):
    #code for notes in between lines
    smallest_distance = 1000000
    distances_info = []
    distance_info = ()
    test_distance = []
    for line in split_lines:
        for x1, y1, x2, y2, rho, theta, note_pos in line:
            # print("y2:", y2)
            # print("y_c:", y_c)
            distance = abs(int(y2) - int(y_c))
            # print("distance1:", distance)
            test_distance.append(distance)
            distance_info = (distance, note_pos, y2)
            distances_info.append(distance_info)
            # print("appended:" ,distance_info)
            # print("distances_info for now", distances_info)
    # print("distances_info:",distances_info)
    # print("test_distance:",test_distance)
    # print("distances_info:",distances_info)
    distances_info_sorted = sorted(distances_info, key=lambda x: x[0])
    # print("distances_info_sorted:",distances_info_sorted)
    # print("distances_info_sorted:",distances_info_sorted)
    closest_note_pos = distances_info_sorted[0][1]
    second_closest_note_pos = distances_info_sorted[1][1]
    if closest_note_pos == 1 and (y_c > distances_info_sorted[0][2]) and (y_c - distances_info_sorted[0][2] < line_spacing):
        print("Note is F (bottom)")
        cv2.putText(img, "F,f (bottom)", (x_c, y_c), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        print("values:",x_c, y_c)
        return
    if closest_note_pos == 1 and (y_c > distances_info_sorted[0][2]) and (y_c - distances_info_sorted[0][2] > line_spacing):
        print("Note is E (botbot)")
        cv2.putText(img, "E,f (botbot)", (x_c, y_c), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        return
    if closest_note_pos == 5 and (y_c < distances_info_sorted[0][2]) and (distances_info_sorted[0][2] - y_c < line_spacing):
        print("Note is B (top)")
        cv2.putText(img, "B,f (top)", (x_c, y_c), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        return
    if closest_note_pos == 5 and (y_c < distances_info_sorted[0][2]) and (distances_info_sorted[0][2] - y_c > line_spacing):
        print("Note is C (toptop)")
        cv2.putText(img, "C,f (toptop)", (x_c, y_c), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        return
    # print("closest_note_pos and second_closest_note_pos:",closest_note_pos,second_closest_note_pos)
    # print("distances_info_sorted",distances_info_sorted)
    if closest_note_pos == 1 and second_closest_note_pos == 2 or closest_note_pos == 2 and second_closest_note_pos == 1:
        print("note is a A")
        cv2.putText(img, "A,f", (x_c, y_c), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    elif closest_note_pos == 2 and second_closest_note_pos == 3 or closest_note_pos == 3 and second_closest_note_pos == 2:
        print("note is a C")
        cv2.putText(img, "C,f", (x_c, y_c), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    elif closest_note_pos == 3 and second_closest_note_pos == 4 or closest_note_pos == 4 and second_closest_note_pos == 3:
        print("note is a E")
        cv2.putText(img, "E,f", (x_c, y_c), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    elif closest_note_pos == 4 and second_closest_note_pos == 5 or closest_note_pos == 5 and second_closest_note_pos == 4:
        print("note is a G")
        cv2.putText(img, "G,f", (x_c, y_c), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    # print("No intersection found")