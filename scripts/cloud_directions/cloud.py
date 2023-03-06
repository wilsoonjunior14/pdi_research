import numpy as np

class Cloud():
    id = 0
    x = 0
    y = 0
    width = 0
    height = 0
    amountPixelsArea = 0
    amountPixelsPerimeter = 0
    iterationId = 0
    parentId = 0

    def __init__(self, x, y, width, height, amountPixelsArea, amountPixelsPerimeter) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.amountPixelsArea = amountPixelsArea
        self.amountPixelsPerimeter = amountPixelsPerimeter

    # calculates the metric to be compared
    def getMetric(self):
        data = [self.x, self.y, self.width, self.height, self.amountPixelsPerimeter]
        return np.std(data) # return the standard deviation

    # return the data list
    def getData(self):
        return [self.x, self.y, self.width, self.height, self.amountPixelsArea, self.amountPixelsPerimeter]