import cv2
import numpy as np
import math


def line_intersection(line1_start, line1_end, line2_start, line2_end):
#Finds the intersection point of two lines.
    x1, y1 = line1_start
    x2, y2 = line1_end
    x3, y3 = line2_start
    x4, y4 = line2_end
    det = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if det == 0:
        return None  # Lines do not intersect
    intersection_x = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / det
    intersection_y = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / det
    return int(intersection_x), int(intersection_y)
image_path = '/Users/alexbenny/Downloads/poolproject/SAMPLE6.png'

# Load the image
image = cv2.imread(image_path)
clean_image = image.copy()

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Threshold the image to get a binary image
ret, thresh = cv2.threshold(gray, 230, 255, cv2.THRESH_BINARY)

# Find contours
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Find the largest contour
largest_contour = max(contours, key=cv2.contourArea)
cv2.drawContours(image, [largest_contour], -1, (0, 255, 0), 3)

# Find the second largest contour
contours = [cnt for cnt in contours if not np.array_equal(cnt, largest_contour)]
second_largest_contour = max(contours, key=cv2.contourArea)
cv2.drawContours(image, [second_largest_contour], -1, (255, 0, 0), 3)

# Find the part of the second largest contour that is closest to the largest contour
closest_distance = float('inf')
closest_point = None
for point in second_largest_contour:
    distance = np.sqrt((largest_contour[0][0][0] - point[0][0]) ** 2 + (largest_contour[0][0][1] - point[0][1]) ** 2)
    if distance < closest_distance:
        closest_distance = distance
        closest_point = point[0]

# Draw a dot at the closest point
cv2.circle(image, (closest_point[0], closest_point[1]), 5, (255, 0, 0), -1)

# Draw a line from the center of the second largest contour to the closest point
M = cv2.moments(second_largest_contour)
cX = int(M["m10"] / M["m00"])
cY = int(M["m01"] / M["m00"])
cv2.line(image, (cX, cY), (closest_point[0], closest_point[1]), (128, 0, 128), 2)

color_to_detect = [255, 0, 255]

# Create a mask for the desired color  
mask = np.all(image == color_to_detect, axis=-1)

# Find contours of the mask
contours, _ = cv2.findContours(mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Draw the contours This contour is called the resultContour
resultContour = contours[0]
cv2.drawContours(image, contours, -1, (0, 255, 0), 3)

# Find the minimum area rectangle that encloses the largest contour
rect = cv2.minAreaRect(largest_contour)
box = cv2.boxPoints(rect)
box = np.int0(box)


# Update the box points based on the closest point
new_box = np.array([box[0], box[1], closest_point, box[3]])

# Draw the modified rectangle on the image
cv2.drawContours(image, [new_box], 0, (0, 0, 255), 2)

cv2.line(image, (closest_point[0], closest_point[1]), (cX, cY), (255, 255, 204), 2)

# Get the image dimensions
image_height, image_width, _ = image.shape

resulting_contour_mask = np.zeros_like(gray)
cv2.drawContours(resulting_contour_mask, contours, -1, 255, thickness=cv2.FILLED)

# Draw a line that extends from the center to the bounds
if cX != closest_point[0]:
    m = (cY - closest_point[1]) / (cX - closest_point[0])  # Calculate slope
    if cX > closest_point[0]:
        for i in range(cX, image_width - 1):
            current_x = i
            current_y = int(cY + m * (current_x - cX))
            if resulting_contour_mask[current_y, current_x] == 255:
                break
            cv2.line(image, (current_x, current_y), (cX, cY), (69, 129, 142), 2)
    else:
        for i in range(cX, 0, -1):
            current_x = i
            current_y = int(cY - m * (cX - current_x))
            if resulting_contour_mask[current_y, current_x] == 255:
                break
            cv2.line(image, (current_x, current_y), (cX, cY), (69, 129, 142), 2)
else:
    if cY > closest_point[1]:
        for i in range(cY, image_height - 1):
            current_y = i
            if resulting_contour_mask[current_y, cX] == 255:
                break
            cv2.line(image, (cX, current_y), (cX, cY), (69, 129, 142), 2)

area = cv2.contourArea(second_largest_contour)
radius = math.sqrt(area / math.pi)

# Calculate the coordinates for the trailing dot
end_x, end_y = current_x, current_y  # Replace with the actual end coordinates of the line

if end_x != cX:
    m_inverse = (end_y - cY) / (end_x - cX)  # Calculate inverse slope
    if end_x > cX:
        back_x = end_x - int(radius / math.sqrt(1 + m_inverse**2))
    else:
        back_x = end_x + int(radius / math.sqrt(1 + m_inverse**2))
    back_y = int(cY + m_inverse * (back_x - cX))
else:
    if end_y > cY:
        back_y = end_y - radius
    else:
        back_y = end_y + radius
    back_x = cX

cv2.circle(image, (back_x, back_y), 5, (255, 0, 0), -1)

area = cv2.contourArea(second_largest_contour)
radius = math.sqrt(area / math.pi)

# Calculate the coordinates for the trailing dot
end_x, end_y = current_x, current_y  # Replace with the actual end coordinates of the line

if end_x != cX:
    m_inverse = (end_y - cY) / (end_x - cX)  # Calculate inverse slope
    if end_x > cX:
        back_x = end_x - int(radius / math.sqrt(1 + m_inverse**2))
    else:
        back_x = end_x + int(radius / math.sqrt(1 + m_inverse**2))
    back_y = int(cY + m_inverse * (back_x - cX))
else:
    if end_y > cY:
        back_y = end_y - radius
    else:
        back_y = end_y + radius
    back_x = cX

cv2.circle(image, (back_x, back_y), 5, (255, 0, 255), -1)

# Calculate the slope of the line passing through the trailing dot and the center of the resultContour
result_contour_center = cv2.moments(resultContour)
result_cX = int(result_contour_center["m10"] / result_contour_center["m00"])
result_cY = int(result_contour_center["m01"] / result_contour_center["m00"])

if result_cX != back_x:
    m_result = (result_cY - back_y) / (result_cX - back_x)  # Calculate slope
    if result_cX > back_x:
        extended_line_end_x = image_width - 1
        extended_line_end_y = int(back_y + m_result * (extended_line_end_x - back_x))
    else:
        extended_line_end_x = 0
        extended_line_end_y = int(back_y - m_result * (back_x - extended_line_end_x))
else:
    extended_line_end_x = back_x
    if result_cY > back_y:
        extended_line_end_y = image_height - 1
    else:
        extended_line_end_y = 0

#image = clean_image
cv2.line(image, (extended_line_end_x, extended_line_end_y), (back_x, back_y), (0, 255, 255), 2)


# Display the image with the largest contour, the rectangle, and the extended line
cv2.imshow('Image with Contour, Rectangle, and Extended Line', image)
cv2.waitKey(0)
cv2.destroyAllWindows()

