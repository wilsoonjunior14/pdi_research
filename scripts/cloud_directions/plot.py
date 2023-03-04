import matplotlib.pyplot as plt
import numpy as np
import cv2

class Plot:
    shape = ()
    coordinates = []

    def __init__(self, shape, coordinates):
        self.coordinates = coordinates
        self.shape = shape

    def plot_results(self):
        image = np.zeros((574, 516), np.uint8)
        radius = 2
        color = (255, 255, 255)
        thickness = 1

        for points in self.coordinates:
            data = []
            for i in range(0, len(points) - 1):
                data.append((points[i], points[i+1]))

            start0, end0 = data[0]
            start1, end1 = data[-1]
            cv2.circle(image, start0, 1, color, thickness)
            cv2.circle(image, end1, 2, color, thickness)

            for item in data:
                start, end = item
                cv2.line(image, start, end, color, thickness)
        
        cv2.imwrite("chart_results.png", image)
