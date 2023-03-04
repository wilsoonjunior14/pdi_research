import cv2 as cv
import numpy as np
from cloud import Cloud
import sys

class Processing():
    filename = ""
    image = ""
    shape = 0
    DIRECTORY = "../database/cloud_directions/"

    def __init__(self, filename) -> None:
        self.filename = filename
        self.image = cv.imread(self.DIRECTORY + filename, 0)
        self.shape = np.shape(self.image)

    def filter(self):
        # filtering the image, removing lines and noises
        imageBlurred = cv.medianBlur(self.image, 7)
        cv.imwrite(self.DIRECTORY + "filter.png", imageBlurred)
        return imageBlurred

    def segmentation(self, image):
        # applying segmentation on image
        ret,imageSegmented = cv.threshold(image, 150, 255, cv.THRESH_BINARY)
        cv.imwrite(self.DIRECTORY + "segmentation.png", imageSegmented)
        return imageSegmented

    def morphology(self, image):
        # applying morphological techniques
        kernel = np.ones((7,7),np.uint8)
        img = cv.morphologyEx(image, cv.MORPH_OPEN, kernel)
        cv.imwrite(self.DIRECTORY + "morphology.png", img)
        return img

    def getSumWhiteValues(self, array):
        x,y = np.shape(array)
        count = 0
        amount = 0
        for i in range(0, x):
            for j in range(0, y):
                amount = amount + 1
                if (array[i,j] == 255):
                    count = count + 1
        return count

    def getCloud(self, image, contour):
        x,y,w,h = cv.boundingRect(contour)
        smallImage = np.zeros((np.shape(image)), np.uint8)
        smallImage[y:y+h, x:x+w] = image[y:y+h, x:x+w]
        #cv.imwrite("cloud.png", smallImage)
        # calculating the area - the amount of pixels which is represented inside the cloud area
        # amountPixelsArea = self.getSumWhiteValues(smallImage)
        amountPixelsArea = w*h

        # calculating the perimeter - the amount of pixels inside edge of the cloud
        smallImageEdges = cv.Canny(smallImage, 150, 255)
        #cv.imwrite("cloud_edge.png", smallImageEdges)
        # amountPixelsPerimeter = self.getSumWhiteValues(smallImageEdges)
        amountPixelsPerimeter = 2 * (w + h)
        cloud = Cloud(x, y, w, h, amountPixelsArea, amountPixelsPerimeter)
        return cloud

    def executeProcess(self):
        imageBlurred = self.filter()
        imageSegmented = self.segmentation(imageBlurred)
        imageReady = self.morphology(imageSegmented)

        imageToBeDrawed = imageReady

        # computing the all contours
        contours, hierarchy = cv.findContours(imageReady, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        allClouds = []
        for contour in contours:
            area = cv.contourArea(contour)
            if (area >= 1000):

                x,y,w,h = cv.boundingRect(contour)
                cv.rectangle(imageToBeDrawed, (x,y), (x+w,y+h), (255, 255, 255), 2)

                cloudObj = self.getCloud(imageReady, contour)
                allClouds.append(cloudObj)

        cv.imwrite(self.DIRECTORY + self.filename + "contoured.png", imageToBeDrawed)
        return allClouds
