# Make regression predictions using the trained MLP regression model from trainNet.py
# Dylan Greene (dgreene2)

import numpy as np
import pickle
from pybrain.datasets import SupervisedDataSet
from pybrain.structure.networks import FeedForwardNetwork
import math

if __name__ == '__main__':
    # Load and prepare the test file
    test_f = 'housing-testing.csv'
    test_data = np.loadtxt(test_f, delimiter=',')
    X = test_data[::, :-1] # feature vectors
    y = test_data[::, -1] # target vector
    y = y.reshape(-1, 1) # transform shape to (n,1) for training
    y_dummy = np.zeros(y.shape) # dummy labels for pybrain

    # Format the test input dataset for pybrain
    input_size = len(X[0])
    target_size = len(y_dummy[0])
    ds = SupervisedDataSet(input_size, target_size)
    for inpt, target in zip(X, y_dummy):
        ds.addSample(inpt, target)

    # Load the trained model
    model_file = 'model.pkl'
    with open(model_file, 'rb') as f:
        net = pickle.load(f)

    # Calculate regression predictions
    pred = net.activateOnDataset(ds)

    # Save predictions
    np.savetxt('predictions.txt', np.array(list(zip(pred, y.flatten()))), fmt='%f', header='y_pred, y_act')

    # See how well we did
    # First calculate Root-Mean-Squared-Error
    sum_squares_error = 0
    for y_pred, y_actual in zip(pred.flatten(), y.flatten()):
        sum_squares_error += (y_pred - y_actual)**2
    rmse = math.sqrt(sum_squares_error / len(y))
    print('Root-Mean-Squared-Error:', rmse)
