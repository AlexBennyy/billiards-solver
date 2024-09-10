import cv2
import numpy as np
import math
from PIL import Image
from collections import Counter



image_path = '/Users/alexbenny/Downloads/poolproject/sample1.png'

# Load the image
image = cv2.imread(image_path)



# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Threshold the image to get a binary image
ret, thresh = cv2.threshold(gray, 230, 255, cv2.THRESH_BINARY)

# Find contours
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(image, contours, -1, (0, 255, 0), 3)
# Find the largest contour
largest_contour = max(contours, key=cv2.contourArea)
cv2.drawContours(image, [largest_contour], -1, (0, 255, 0), 3)

# Find the second largest contour
contours = [cnt for cnt in contours if not np.array_equal(cnt, largest_contour)]
second_largest_contour = max(contours, key=cv2.contourArea)
cv2.drawContours(image, [second_largest_contour], -1, (255, 0, 0), 3)


# Display the image with the largest contour, the rectangle, and the extended line
cv2.imshow('Image with Contour, Rectange, and Extended Line', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
