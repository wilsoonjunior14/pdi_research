import numpy as np

class Cloud():
    id = 0
    x = 0
    y = 0
    width = 0
    height = 0
    cloudCover = 0
    iterationId = 0
    parentId = 0
    points = []

    def __init__(self, x, y, width, height, cloudCover) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.cloudCover = cloudCover

    # return the data list
    def getData(self):
        return [self.x, self.y, self.width, self.height, self.cloudCover]
    
    def getDirection(self):
        if (self.points == [] or len(self.points) == 0):
            return "direction not computed."
        
        xi, yi = self.points[0]
        xf, yf = self.points[-1]

        xR = xf - xi
        yR = yf - yi

        # x zero, y zero         => no displacement
        if (xR == 0 and yR == 0):
            return "no displacement"
        
        # x zero, y negative     => west direction
        # x zero, y positive     => east direction
        if (xR == 0):
            if (yR < 0):
                return "west"
            else:
                return "east"
        
        # x negative, y zero     => north direction
        # x positive, y zero     => south direction
        if (yR == 0):
            if (xR < 0):
                return "north"
            else:
                return "south"
    
        # x negative, y negative => northest direction west
        # x negative, y positive => northeast direction east
        if (xR < 0):
            if (yR < 0): 
                return "northest"
            else:
                return "northeast"
            
        # x positive, y negative => southest direction west
        # x positive, y positive => southeast direction east
        if (xR > 0):
            if (yR < 0): 
                return "southest"
            else:
                return "southeast"