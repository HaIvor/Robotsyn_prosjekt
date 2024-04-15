import cv2
import numpy as np 

img = cv2.imread('assets/martin.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,50,150,apertureSize = 3)
# cv2.imshow('hough',edges)
cv2.waitKey(0)
lines_ro_theta = cv2.HoughLines(edges,1,np.pi/180,200) # 200 is the threshold
print(lines_ro_theta)
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
print(len(filtered_lines))

for lin in filtered_lines:
    x1,y1,x2,y2,rho,theta = lin
    sorted_lines = sorted(filtered_lines, key=lambda x: x[4], reverse=True)
    for lin in sorted_lines:
        x1, y1, x2, y2, rho, theta = lin
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
    cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)
print("number of lines:", len(sorted_lines))
#split into 5 lines
split_lines = [sorted_lines[i:i+5] for i in range(0, len(sorted_lines), 5)]
cv2.circle(img, (300,300),8,(0,0,255),-1)
print("\n\n",split_lines)
cv2.namedWindow("hough", cv2.WINDOW_NORMAL) #så ikke zoomed-in
cv2.resizeWindow("hough", img.shape[0]-200, img.shape[1]-130) 
cv2.imshow('hough',img)
cv2.waitKey(0)
