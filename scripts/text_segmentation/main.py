import cv2 as cv
import numpy as np
import sys

originalImage = cv.imread("../database/text_segmentation/a01-122.jpg", 0)

ret,originalImage = cv.threshold(originalImage, 155, 255, cv.THRESH_BINARY_INV)
cv.imwrite("../database/text_segmentation/0.png", originalImage)

# equalizes the histogram
image = cv.equalizeHist(originalImage)
cv.imwrite("../database/text_segmentation/1.png", image)

# left contour projection
x, y = np.shape(image)
histogram = np.zeros((x, y))
for i in range(0, x):
    for j in range(0, y):
        if (image[i, j] == 255):
            histogram[i, 0:j] = 127
            if (i + 1 < x):
                i = i + 1
                j = 0
                break

cv.imwrite("../database/text_segmentation/2.png", histogram)

# identifying lines
lines_array = []
start_index = -1
end_index = -1
for i in range(0, x):
    if (histogram[i, 0] == 127 and start_index == -1):
        start_index = i
    elif (histogram[i,0] == 0 and start_index != -1 and end_index == -1):
        end_index = i
        if (end_index - start_index > 2):
            lines_array.append((start_index, end_index)) 
        start_index = -1
        end_index = -1

print (lines_array)

# processing and saving the lines found
index = 0
for item in lines_array:
    xi,xf = item
    cv.imwrite("../database/text_segmentation/lines/"+str(index)+".png", originalImage[xi:xf, :])
    index = index + 1



