# Train an MLP regression model for the Boston Housing Dataset
# Dylan Greene (dgreene2)

import numpy as np
from pybrain.datasets import SupervisedDataSet
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
import pickle

if __name__ == '__main__':
    # Load and prepare training and validation files
    train_f = 'housing-training.csv'
    validation_f = 'housing-validation.csv'
    train_data = np.loadtxt(train_f, delimiter=',')
    validation_data = np.loadtxt(validation_f, delimiter=',')
    data = np.vstack((train_data, validation_data))
    X = data[::, :-1] # feature vectors
    y = data[::, -1] # target vector
    y = y.reshape(-1, 1) # transform shape to (n,1) for training

    # Prepare the dataset for pybrain
    input_size = len(X[0])
    target_size = len(y[0])
    ds = SupervisedDataSet(input_size, target_size)
    for inpt, target in zip(X, y):
        ds.addSample(inpt, target)

    # Build the pybrain network
    # source (http://pybrain.org/docs/quickstart/network.html)
    n_input = 13 # 12 features so 12 input neurons
    n_hidden = 100 # Network spec: 100 hidden units
    n_output = 1 # 1 target so a single output neuron
    net = buildNetwork(n_input, n_hidden, n_output)

    # Train the network on the dataset
    trainer = BackpropTrainer(net, ds)
    for epoch in range(1000):
        print(trainer.train())

    # Save model via pickle
    output_file = 'model.pkl'
    with open(output_file, 'wb') as f:
        pickle.dump(net, f)
