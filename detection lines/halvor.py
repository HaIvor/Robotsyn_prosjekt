import cv2
import numpy as np 

img = cv2.imread('assets/martin.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,50,150,apertureSize = 3)
print("width, height: ", edges.shape[0], edges.shape[1])
# cv2.imshow('hough',edges)
cv2.waitKey(0)
# HoughLines(image, rho, theta, threshold) -> lines
lines_ro_theta = cv2.HoughLines(edges,1,np.pi/180,250)

approved_lines = []
for line in lines_ro_theta:
    for rho,theta in line:
        epsilon = np.pi/4 # +-45 degrees buffer from linewidth
        want_angle = np.pi/2
    
        #filter unwanted lines
        if theta < want_angle - epsilon or theta > want_angle + epsilon: continue
        
        # if approved_lines is not empty (first line is always approved)
        if approved_lines:
            # check if the new line is close to any of the approved lines
            for approved_line in approved_lines:
                rho_approved, theta_approved = approved_line
                # if the new line is close to an approved line, break the loop
                if abs(rho - rho_approved) < 100 and abs(theta - theta_approved) < 0.1: break
            # if the loop was broken, continue to the next line
            else:
                approved_lines.append((rho,theta))
            

        approved_lines.append((rho,theta)) 
        print("rho, theta: ", rho, theta)
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 800*(-b))
        y1 = int(y0 + 800*(a))
        x2 = int(x0 - 800*(-b))
        y2 = int(y0 - 800*(a))
        
        cv2.line(img,(x1,y1),(x2,y2),(0,0,255),1)

print(approved_lines)

cv2.namedWindow("hough", cv2.WINDOW_NORMAL) #så ikke zoomed-in
cv2.resizeWindow("hough", img.shape[0]-100, img.shape[1]-120) 
cv2.imshow('hough',img)
cv2.waitKey(0)