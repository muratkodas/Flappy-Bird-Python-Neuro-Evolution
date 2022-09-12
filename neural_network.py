import numpy as np


class Layer:
    def __init__(self, name, neuron_p, neuron_n): #neuron_previous, neuron_next
        self.name = name
        self.lr = 1
        self.neuron_p = neuron_p
        self.neuron_n = neuron_n
        self.Layer_Initialization()

    def Layer_Initialization(self):
        self.weights = np.random.rand(self.neuron_p,self.neuron_n)
        self.bias = np.random.rand(1,self.neuron_n)

    def sigmoid(self, x):
        return 1/(1+np.exp(-x))

    def sigmoid_der(self, x):
        return self.sigmoid(x)*(1-self.sigmoid(x))

    def Forward_Propagation(self, input_data):
        self.input_data = input_data
        self.z = self.input_data @ self.weights + self.bias
        self.a = self.sigmoid(self.z)

    def Back_Propagation(self, error):
        # Update the genetic material of the layer via back propagation
        self.error = error
        self.sigmoid_der_z = self.sigmoid_der(self.z)
        self.a_delta = self.error * self.sigmoid_der_z
        self.error_pre = self.weights.transpose() @ self.a_delta # for back propagation loop
        self.weights -=  self.a_delta @ self.input_data.transpose()
        self.bias -= self.lr * self.a_delta
        
        
class Neural_Network:
    def __init__(self, neurons): #neurons:[[16], [10]] means first layer has 16 neurons, 2nd has 10
        self.neurons = neurons
        self.layer_quantity = self.neurons.shape[1] - 1

        
        self.layers = []
        for i in range(self.layer_quantity):
            self.layers.append(Layer(i,neuron_p = self.neurons[0,i], neuron_n = self.neurons[0,i+1]))
 
    def NN_loop(self, input_matrix, learning = True):
        self.Forward_Propagation_Loop(input_matrix)
        if learning:
            self.Back_Propagation_Loop()
            return None
        else:
            return self.layers[-1].a # returns the output of the neural network

    def Forward_Propagation_Loop(self, input_matrix):
        for i in range(self.layer_quantity):
            self.layers[i].Forward_Propagation(input_matrix)
            input_matrix = self.layers[i].a
            
    def Back_Propagation_Loop(self,label):
        #NOT TESTED for Genetic Algorithm
        # Update the genetic material of the layers via back propagation
        for i in range(self.layer_quantity):
            if i ==0:
                self.error = self.layers[i] - label
            self.layers[i].Back_Propagation(self.error)
            self.error = self.layers[i].error_pre
        
