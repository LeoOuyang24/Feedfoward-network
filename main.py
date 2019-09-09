'''
Created on Jul 12, 2019

@author: leoou
'''
import math
import random
import functools
import numpy

def sigmoid(x):
    return 1/(1+pow(math.e,-x))

class Neuron:
    def __init__(self, inputN):
        self.bias = 0
        self.biasAvg = 0;
        self.output = 1;
        self.inputs = {} #consists of nodes in the immediate previous layer and their weights
        self.error  = 1#(dError/dOuput)*(dOuput/dAverage). Useful for backpropagation
        for i in range(len(inputN)):
            self.inputs[inputN[i]] = [random.random(),0]
    def feed(self, num):
        self.output = num 
    def spit(self):
        wavg = 0;
        for i in self.inputs:
            wavg += i.output*self.inputs[i][0]
        self.output = sigmoid(wavg + self.bias) 
        return self.output;

class Network:
    def __init__(self, nums,rate): #pass in a list of how many neurons there should be per layer
        self.neurons = [] #2d list of neurons
        self.lastError = 0 #error of the last input
        self.lRate = rate#learning rate
        index = 0;
        for i in nums:
            lst = []
            for j in range(i):
                if index > 0:
                    lst.append(Neuron(self.neurons[index-1]))
                else:
                    lst.append(Neuron([]))
            self.neurons.append(lst)
            index += 1
    def feed(self, input, answer):
        for n in range(len(self.neurons[0])):
            self.neurons[0][n].feed(input[n])
        for i in range(1,len(self.neurons)):
            for j in range(len(self.neurons[i])):
                neuron = self.neurons[i][j]
                neuron.spit()
                if i == len(self.neurons)-1:
                    self.lastError += pow(neuron.output - answer[j],2)
        self.lastError /= 2*len(answer)
        self.__backProp(answer)
        return self.__getOuput()
    def __backProp(self, answer):
        for layer in range(len(self.neurons)-1,-1,-1):
            dedo = 0 #de/do
            outermostLayer = layer == len(self.neurons)-1 #whether or not this is the outermost layer
            vec = [] #vector of error of each neuron in this layer. Only used if this is not the outermost layer
            if not outermostLayer:
                for neuron in self.neurons[layer+1]:
                    vec.append(neuron.error)
            for num in range(len(self.neurons[layer])):
                neuron = self.neurons[layer][num]
                if outermostLayer:
                    dedo = (neuron.output - answer[num])
                else:
                    weights = list(map(lambda x: x.inputs[neuron][0],self.neurons[layer + 1])) #weights between all neurons in the next layer and this neuron
                    for i in range(len(weights)):
                        dedo += weights[i]*vec[i]
                neuron.error = dedo*neuron.output*(1-neuron.output)
                for input in neuron.inputs:
                    neuron.inputs[input][0] += -self.lRate*neuron.error*input.output
                neuron.bias += -self.lRate*neuron.error
        
                
    def __getOuput(self):
        lst = []
        for i in self.neurons[-1]:
            lst.append(i.output)
        return lst
random.seed()
network = Network([2,10,1],.1)
for i in range(100000):
    num1 = random.randint(0,10)
    num2 = num1
    if random.randint(0,1)==0:
        num2 = random.randint(0,10)
    answer = num1 == num2
    print (num1,num2,answer,network.feed([num1,num2],[answer]), network.lastError)
    #network.update(1000)
while input("Type quit to quit or press enter to continue") != "quit":
    num1 = int(input("Type number 1"))
    num2 = int(input("Type number 2"))
    answer = num1 == num2
    print (num1,num2,answer,network.feed([num1,num2],[answer]),network.lastError)
        