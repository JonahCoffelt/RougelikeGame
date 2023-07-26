import numpy as np

def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))

class Network(object):
    def __init__(self, layerData):
        self.layers = len(layerData)
        self.biases = [np.random.randn(y, 1) for y in layerData[1:]]
        self.weights = [np.random.randn(y, x) for y, x in zip(layerData[1:], layerData[:-1])]
    
    def feedforward(self, a):
        for w, b in zip(self.weights, self.biases):
            a = sigmoid(np.dot(w, a) + b)
        return a
