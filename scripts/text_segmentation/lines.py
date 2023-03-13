import cv2 as cv
import numpy as np
import sys

image = cv.imread("../database/text_segmentation/lines/0.png", 0)

# top contour projection
x, y = np.shape(image)
histogram = np.zeros((x, y))
for j in range(0, y):
    for i in range(0, x):
        if (image[i, j] == 255):
            histogram[0:i, j] = 127
            if (i + 1 < x):
                i = i + 1
                j = 0
                break

cv.imwrite("../database/text_segmentation/characters/histogram.png", histogram)

lines_array = []
start_index = -1
end_index = -1
for j in range(0, y):
    if (histogram[0, j] == 127 and start_index == -1):
        start_index = j
    elif (histogram[0, j] == 0 and start_index != -1 and end_index == -1):
        end_index = j
        if (end_index - start_index >= 2):
            lines_array.append((start_index, end_index)) 
        start_index = -1
        end_index = -1

# processing and saving the characters found
index = 0
for item in lines_array:
    yi, yf = item
    cv.imwrite("../database/text_segmentation/characters/"+str(index)+".png", image[:, yi:yf])
    index = index + 1

