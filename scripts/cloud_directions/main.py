from cloud import Cloud
from processing import Processing
from database import Database
from plot import Plot
import numpy as np
import cv2
import sys

# Global Variables
TAX_VARIATION = 10
AREA_TAX_VARIATION = 0.30
DISTANCE_TAX_VARIATION = 0.15

# Step 1 - Initializing Database
databaseInstance = Database(False)
databaseInstance.dropTable("cloud")
databaseInstance.initialize()

# Step 2, Step 3, Step 4 (Image Acquisition, Image Processing, Data Collection)
imgs = [
    "22_02_23_00_00.png",
    "22_02_23_00_10.png",
    "22_02_23_00_20.png",
    "22_02_23_00_30.png",
    "22_02_23_00_40.png",
    "22_02_23_01_00.png",
    "22_02_23_01_10.png",
    "22_02_23_01_20.png",
    "22_02_23_01_30.png",
    "22_02_23_01_40.png",
    "22_02_23_02_00.png",
    "22_02_23_02_10.png",
    "22_02_23_02_20.png",
    "22_02_23_02_30.png",
    "22_02_23_03_00.png"
]
iteration = 1
for img in imgs:
    print ("### PROCESSING IMAGE "+img+" ###")
    processingInst = Processing(img)
    clouds = processingInst.executeProcess()

    for cloud_v2 in clouds:
        cloud_v2.iterationId = iteration
        databaseInstance.createCloud(cloud_v2)

    iteration = iteration + 1

# Step 5 - Finding similar clouds 
def mountCloud(row) -> Cloud:
    cloud = Cloud(row[1], row[2], row[3], row[4], row[5], row[6])
    cloud.iterationId = row[7]
    cloud.id = row[0]
    cloud.parentId = row[8]
    return cloud

def getClouds(iteration):
    array = []
    cursor = databaseInstance.selectClouds(iteration)
    for row in cursor:
        cloud = mountCloud(row)
        array.append(cloud)
    return array

for i in range(1, len(imgs)):
    previousClouds = getClouds(i)
    nextClouds = getClouds(i + 1)

    if (previousClouds == None or len(previousClouds) == 0
    or nextClouds == None or len(nextClouds) == 0):
        break

    for previous_C in previousClouds:
        print ("   ")
        print ("### Checking cloud "+str(previous_C.id)+" ###")

        approximationFound = (0, 0, 0, 0)
        for next_C in nextClouds:
            areas = [previous_C.amountPixelsArea, next_C.amountPixelsArea]
            area_difference_percentage = np.round(np.abs(1 - (min(areas) / max(areas))), 3)

            std_cloud0 = previous_C.getMetric()
            std_cloud_v2 = next_C.getMetric()

            difference = np.round(np.abs(std_cloud0 - std_cloud_v2), 2)
            differenceArea = np.round(area_difference_percentage, 3)

            distanceAB = np.round(np.sqrt((next_C.x - previous_C.x)**2 + (next_C.y - previous_C.y)**2), 3)

            if (distanceAB > 45 or differenceArea > AREA_TAX_VARIATION):
                continue

            print (
                distanceAB,
                area_difference_percentage,
                " next cloud id = "+str(next_C.id)+" "
            )

            cloudId, parentId, diff, diffArea = approximationFound
            if (parentId == 0):
                approximationFound = (next_C.id, previous_C.id, distanceAB, differenceArea)
            else:
                isLessThan = (distanceAB + differenceArea) < (diff + diffArea) 
                # print (diff + diffArea, distanceAB + differenceArea)
                if (isLessThan):
                        approximationFound = (next_C.id, previous_C.id, difference, differenceArea)


        cloudId, parentId, diff, diffArea = approximationFound
        if (cloudId != 0 and parentId != 0):
            databaseInstance.updateCloud(cloudId, parentId)

# Step 6 - Computing the common clouds after processing
rows = databaseInstance.selectAllClouds()
clouds = []

for row in rows:
    clouds.append(mountCloud(row))

def findNextCloud(id, clouds):
    nextCloud = None
    for cloud in clouds:
        if (cloud.parentId == id):
            nextCloud = cloud
            break
    return nextCloud

points = []
for cloud in clouds:
    if (cloud.iterationId == 1):
        cloudId = cloud.id
        print ("### find points for the cloud "+str(cloudId)+" ")
        cloudPoint = [(cloud.x, cloud.y)]

        nextCloud = findNextCloud(cloudId, clouds)
        while (nextCloud != None):
            cloudPoint.append((nextCloud.x, nextCloud.y))
            nextCloud = findNextCloud(nextCloud.id, clouds)

        if (len(cloudPoint) > 3):
            points.append(cloudPoint)

for point in points:
    print (point)

databaseInstance.close()

plot = Plot((574, 516), points)
plot.plot_results()
