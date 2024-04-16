#from skimage.transform import (hough_line, hough_line_peaks)
#https://www.youtube.com/watch?v=OchCsSiffeE
#https://www.geeksforgeeks.org/line-detection-python-opencv-houghline-method/
import numpy as np
import cv2
import math
from matplotlib import pyplot as plt
'''
num_of_lines = 0
new_staff = []

#note = cv2.imread('sheet.jpg')
note = cv2.imread('noisystaff.jpg')
#note = cv2.imread('jingle.png')
#note = cv2.imread('emptystaff.jpg')

notesheet = cv2.resize(note, (500,500))
gris = cv2.cvtColor(notesheet, cv2.COLOR_BGR2GRAY)
cansheet = cv2.Canny(gris,150,250)
cv2.imshow("ost",cansheet)
cv2.waitKey(0)

staff = cv2.HoughLines(cansheet, 1,np.pi/180,170,np.array([]))#95 is the length of line i think...
staff_copy = staff
'''
def getLineCalc(line):
    rho,theta =line[0]
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0+1000*(-b))
    y1 = int(y0 +1000*(a))
    x2 = int(x0-1000*(-b))
    y2 = int(y0-1000*(a))
    ang = math.atan2(y2-y1,x2-x1)*180.0/np.pi

    return ang,x1,x2,y1,y2

def removeDuplicates(staff, new_staff):
    for line in staff:
        if not new_staff:
            new_staff.append((line))
        else:
            matched = False   
            for new_line in new_staff: 
                if abs(new_line[0][0]-line[0][0])<20. and abs(new_line[0][1]-line[0][1])<np.pi/180*10:#checking difference in rho and theta
                    matched = True
                    break
            if not matched:

                new_staff.append((line))
    print("Num of lines after removing duplicates:") 
    print(len(new_staff))

    return new_staff
'''
new_staff = removeDuplicates(staff)
final_staff = np.array([line for line in new_staff], dtype=np.float32) #converts to np array

sorted_lines = np.argsort(final_staff[:,0,0])
sorted_lines = final_staff[sorted_lines]

for line in sorted_lines[6:]:
    ang,x1,x2,y1,y2 = getLineCalc(line)
    if ang > -85: #check angle of line
        cv2.line(notesheet, (x1,y1),(x2,y2), (0,0,255),1)#draws line
        num_of_lines+=1   
print("number of lines:")
print(num_of_lines)
#print(final_staff)
#print(sorted_lines)



cv2.imshow("detected", notesheet)
cv2.waitKey(0)
cv2.destroyAllWindows()


'''
