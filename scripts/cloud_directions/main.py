import numpy as np
from sklearn.neural_network import MLPClassifier

from modules.data_acquisition import DataAcquisition
from modules.processing import Processing
from modules.database import Database
from modules.plot import Plot
from modules.plot import PlotType

from models.cloud import Cloud

# Building the cloud
def buildCloud(row):
    cloud = Cloud(row[1], row[2], row[3], row[4], row[5])
    cloud.id = row[0]
    return cloud

# Generating the clouds
def buildClouds(rows):
    clouds = []
    for row in rows:
        cloud = buildCloud(row)
        clouds.append(cloud)
    return clouds

# Generating the outputs to ANN
def generateOutputs(clouds):
    size = np.size(clouds)
    outputLength = np.ceil(np.sqrt(size))

    output = []
    for i in range(0, size):
        value = bin(i).replace('0b', '')
        limit = int(outputLength - len(value))
        for zero in range(0, limit):
            value = "0"+value

        value = [eval(i) for i in list(value)]
        output.append(value)
    return output

# Get inputs from cloud objects
def getInputs(clouds):
    inputs = []
    for cloud in clouds:
        inputs.append(cloud.getData())
    return inputs

# Decoding the results
def decodeResults(old_clouds, clouds, results):
    size = np.size(clouds)
    outputLength = int(np.ceil(np.sqrt(size)))

    currentIndex = 0
    for result in results:
        index = 0
        startAt = outputLength - 1
        for i in result:
            index = index + (2 ** startAt) * i
            startAt = startAt - 1
        databaseInstance.updateCloud(clouds[currentIndex].id, old_clouds[index].id)
        currentIndex = currentIndex + 1

# Step 1 - Initializing Database
databaseInstance = Database(False)
databaseInstance.dropTable("cloud")
databaseInstance.initialize()

# Step 2, Step 3, Step 4 (Image Acquisition, Image Processing, Data Collection)
dataAcquisition = DataAcquisition()
imgs = dataAcquisition.images
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
machine = []
clouds_old_iteration = []
train_inputs = []
train_inputs_normalized = []
train_outputs = []
for i in range(1, iteration):
    print ("### Running ANN Step Iteration "+str(i)+" ###")
    rows = databaseInstance.selectClouds(i)
    clouds = buildClouds(rows)

    if (i != 1):
        print ("### Training ANN ###")
        test_inputs = getInputs(clouds)
        test_inputs_normalized = test_inputs/np.max(test_inputs)
        machine.fit(train_inputs_normalized, train_outputs)
        
        print ("### Testing ANN ###")
        results = machine.predict(test_inputs_normalized)
        print (results)
        decodeResults(clouds_old_iteration, clouds, results)

    train_inputs = np.array(getInputs(clouds))
    train_outputs = np.array(generateOutputs(clouds))
    train_inputs_normalized = train_inputs/np.max(train_inputs)
    clouds_old_iteration = clouds
    machine = MLPClassifier(solver='adam', 
                            random_state=1, 
                            verbose=False, 
                            tol=0.01, 
                            n_iter_no_change=10000, 
                            hidden_layer_sizes=(50, 2), 
                            max_iter=10000)

# Step 6 - Computing the common clouds after processing
# [
#     [207, 97, 92, 94, 1.44]
#     [204, 96, 93, 95, 1.48]
#     [202, 90, 95, 100, 1.53]
#     [199, 90, 96, 102, 1.57]
#     [197, 89, 97, 103, 1.61]
# ]
databaseInstance.close()

# plot
points = [
    [(207, 97), (204, 96)], [(204, 96), (202, 90)], [(202, 90), (190, 90)], [(199, 90), (197, 89)]
]
plot = Plot((574, 516), points)
plot.plot_results("results_ann_direction.png", PlotType.DIRECTION)
plot.plot_results("results_ann_route.png", PlotType.ROUTE)



