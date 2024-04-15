import cv2
import numpy as np

# Create an image canvas
canvas = np.zeros((500, 500, 3), dtype=np.uint8)

# Define a line (two points)
line_start = (0, 200)
line_end = (500, 200)
cv2.line(canvas, line_start, line_end, (0, 255, 0), 1)

# Define a circle (center and radius)
circle_center = (300, 200)
circle_radius = 50
cv2.circle(canvas, circle_center, circle_radius, (0, 0, 255), -1)
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
    
print(line_circle_intersection(line_start, line_end, circle_center, circle_radius))
# Display the canvas
cv2.imshow("Intersection", canvas)
cv2.waitKey(0)
cv2.destroyAllWindows()
