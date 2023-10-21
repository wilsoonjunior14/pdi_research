import matplotlib.pyplot as plt
import numpy as np
import cv2

class PlotType:
    DIRECTION = 1
    ROUTE = 2

class Plot:
    shape = ()
    coordinates = []
    filename = ""
    color = (255, 255, 255)
    thickness = 1

    def __init__(self, shape, coordinates):
        self.coordinates = coordinates
        self.shape = shape

    def plot_results(self, filename, plotType):
        self.filename = filename

        if (plotType == PlotType.DIRECTION):
            self.plot_direction_results()
        elif (plotType == PlotType.ROUTE):
            self.plot_route_results()
        else:
            print ("no plot results type identified.")

    def plot_direction_results(self): 
        image = np.zeros(self.shape, np.uint8)

        for points in self.coordinates:
            data = []
            for i in range(0, len(points) - 1):
                data.append((points[i], points[i+1]))

            start0, end0 = data[0]
            start1, end1 = data[-1]
            cv2.arrowedLine(image, start0, end1,
                                     self.color, self.thickness)
        
        cv2.imwrite(self.filename, image)

    
    def plot_route_results(self):
        image = np.zeros(self.shape, np.uint8)

        for points in self.coordinates:
            data = []
            for i in range(0, len(points) - 1):
                data.append((points[i], points[i+1]))

            start0, end0 = data[0]
            start1, end1 = data[-1]
            cv2.circle(image, start0, 1, self.color, self.thickness)
            cv2.circle(image, end1, 2, self.color, self.thickness)

            length = len(points) * 10

            for item in data:
               start, end = item
               cv2.line(image, start, end, self.color, self.thickness)
            cv2.putText(image, "~"+str(length)+"min", start0, 0, 0.5, 50)

        cv2.imwrite(self.filename, image)
