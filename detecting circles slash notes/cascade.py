import cv2

# Load the cascade classifier for notes
note_cascade = cv2.CascadeClassifier('path/to/notes_cascade.xml')

# Load the image
image = cv2.imread('assets/martin.jpg')

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Detect notes in the image
notes = note_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

# Draw rectangles around the detected notes
for (x, y, w, h) in notes:
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

# Display the image with the detected notes
cv2.imshow('Notes Detection', image)
cv2.waitKey(0)
cv2.destroyAllWindows()