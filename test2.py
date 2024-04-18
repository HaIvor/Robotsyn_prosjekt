import cv2
import numpy as np

img = cv2.imread("assets/halvor.jpg")
img_2 = cv2.imread("assets/abc.jpg")

# Check if images are loaded correctly
if img is None:
    print("Error: Unable to load image halvor.jpg")
    exit()
elif img_2 is None:
    print("Error: Unable to load image abc.jpg")
    exit()

# Resize images to have the same height (optional)
min_height = min(img.shape[0], img_2.shape[0])
img = cv2.resize(img, (int(img.shape[1] * min_height / img.shape[0]), min_height))
img_2 = cv2.resize(img_2, (int(img_2.shape[1] * min_height / img_2.shape[0]), min_height))

# Concatenate images horizontally
img_hor = np.hstack((img, img_2))

# Display concatenated image
cv2.imshow("Two Pictures", img_hor)
cv2.waitKey(0)
cv2.destroyAllWindows()