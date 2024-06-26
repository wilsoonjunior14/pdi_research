import cv2 as cv
import numpy as np
import sys

# Next Steps
# [ ] Load the dataset built by student Gustavo 
# [ ] Evaluate the algorithm of crossing-over to detect the focal points on person body https://www.researchgate.net/figure/Statistical-Method-Crossing-and-Distances-ii-Structural-Method-Characters-can-be_fig3_258029618
# [ ] Use feature extraction (Crossing-Over or another one) to identify the focal points
# [ ] Calculate the degrees of the points
# [ ] Evaluate the usage of Artificial Neural Network
# [ ] Use a machine learning to train and test the approach

image = cv.imread("../database/body_posture/img.png", 0)

hist = cv.equalizeHist(image)
cv.imwrite("../database/body_posture/1.png", hist)

ret,th3 = cv.threshold(hist, 100, 255, cv.THRESH_BINARY)

# filtering image
filtered = cv.medianBlur(th3, 5)
cv.imwrite("../database/body_posture/2.png", filtered)

edges = cv.Canny(filtered, 150, 150)
cv.imwrite("../database/body_posture/3.png", edges)

# applying dilation over the image
kernel = np.ones((3, 3),np.uint8)
dilation = cv.dilate(edges, kernel, iterations = 2)
cv.imwrite("../database/body_posture/4.png", dilation)

# contour projection
x, y = np.shape(dilation)
img_processed = np.zeros((x, y))
for i in range(0, x):
    for j in range(0, y):
        if (dilation[i, j] == 255):
            img_processed[i, 0:j] = 127
            if (i + 1 < x):
                i = i + 1
                j = 0
                break

for i in range(0, x):
    for j in range(y-1, 0, -1):
        if (dilation[i, j] == 255):
            img_processed[i, j:y] = 127
            if (i + 1 < x):
                i = i + 1
                j = y
                break

cv.imwrite("../database/body_posture/contour_projection.png", img_processed)
