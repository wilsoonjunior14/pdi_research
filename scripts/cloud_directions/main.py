from cloud import Cloud
from processing import Processing
from database import Database
from plot import Plot
from plot import PlotType
import numpy as np
from sklearn.neural_network import MLPClassifier

# Step 1 - Initializing Database
databaseInstance = Database(False)
# databaseInstance.dropTable("cloud")
# databaseInstance.initialize()

# Step 2, Step 3, Step 4 (Image Acquisition, Image Processing, Data Collection)
imgs = [
    "test_1_20_06_23/20_06_23_00_00.png",
    "test_1_20_06_23/20_06_23_00_10.png",
    "test_1_20_06_23/20_06_23_00_20.png",
    "test_1_20_06_23/20_06_23_00_30.png"
]
# iteration = 1
# for img in imgs:
#     print ("### PROCESSING IMAGE "+img+" ###")
#     processingInst = Processing(img)
#     clouds = processingInst.executeProcess()

#     for cloud_v2 in clouds:
#         cloud_v2.iterationId = iteration
#         databaseInstance.createCloud(cloud_v2)
#     iteration = iteration + 1

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

def getInputs(clouds):
    inputs = []
    for cloud in clouds:
        inputs.append(cloud.getData())
    return inputs

def decodeResults(clouds, results):
    size = np.size(clouds)
    outputLength = int(np.ceil(np.sqrt(size)))

    for result in results:
        index = 0
        startAt = outputLength - 1
        for i in result:
            index = index + (2 ** startAt) * i
            startAt = startAt - 1
        print (index)


# Step 5 - Finding similar clouds
machine = []
clouds_old_iteration = []
train_inputs = []
train_inputs_normalized = []
train_outputs = []
for i in range(1, 3):
    print ("### Running ANN Step Iteration "+str(i)+" ###")
    rows = databaseInstance.selectClouds(i)
    clouds = buildClouds(rows)

    if (i != 1):
        test_inputs = getInputs(clouds)
        test_inputs_normalized = test_inputs/np.max(test_inputs)
        machine.fit(train_inputs_normalized, train_outputs)
        
        results = machine.predict(test_inputs_normalized)
        print (results)
        decodeResults(clouds_old_iteration, results)

    train_inputs = np.array(getInputs(clouds))
    train_outputs = np.array(generateOutputs(clouds))
    train_inputs_normalized = train_inputs/np.max(train_inputs)
    clouds_old_iteration = clouds
    machine = MLPClassifier(solver='lbfgs', alpha=1e-10, hidden_layer_sizes=(50, 2), random_state=1, max_iter=10000)

# Step 6 - Computing the common clouds after processing

# 0 0 -> 2**0 * 0 + 2**1 * 0 = 0
# 0 1 -> 2**0 * 1 + 2**1 * 0 = 1
# 1 0 -> 2**0 * 0 + 2**1 * 1 = 2
# 1 1 -> 2**0 * 1 + 2**1 * 1 = 3


