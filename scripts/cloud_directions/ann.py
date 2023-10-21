from sklearn.neural_network import MLPClassifier
import numpy as np

x = [
    [ 207, 97, 92, 94, 1.44 ],
    [ 138, 61, 50, 56, 0.41 ],
    [ 106, 53, 39, 52, 0.4 ],
    [ 0, 4, 82, 128, 1.83 ]
]
y = [[0,0], [0, 1], [1, 0], [1, 1]]

xNormalized = x/np.max(x)

machine = MLPClassifier(solver='lbfgs', alpha=1e-10, hidden_layer_sizes=(50, 2), random_state=1, max_iter=10000)
machine.fit(xNormalized, y)

xTest = [
    [ 204, 96, 93, 95, 1.48 ],
    [ 138, 60, 47, 55, 0.35 ],
    [ 103, 51, 39, 55, 0.39 ],
    [ 0, 3, 79, 128, 1.8 ]
]

xTestNormalized = xTest/np.max(xTest)

print (machine.predict(xNormalized))

print (machine.predict([xTestNormalized[0]]))
print (machine.predict([xTestNormalized[1]]))
print (machine.predict([xTestNormalized[2]]))
print (machine.predict([xTestNormalized[3]]))