# Description: This file contains the neural network class and its functions
import random
import utils
from layer import Layer

INITIAL_WEIGHT_RATE = 1.0
BIAS = 1
AMOUNT_ENTRY_NEURON = 4 + BIAS
AMOUNT_HIDDEN_NEURON = [4 + BIAS]
AMOUNT_OUT_NEURON = 5


def relu(x):
    return max(0, x)


def GetEntryParams(character, gamemode):
    (LogXDist, LogYDist) = utils.GetClosestLogDist(character.CurrentLocation, gamemode.CurrentBackground)
    return [
        LogXDist > 0,
        LogXDist == 0,
        LogYDist > 0,
        LogYDist == 0
    ]


class NeuralNetwork:
    EntryLayer = []
    HiddenLayer = []
    OutLayer = []

    LastCalculatedOutput = []

    def __init__(self):
        self.EntryLayer = Layer(AMOUNT_ENTRY_NEURON, 0)
        self.HiddenLayers = [Layer(AMOUNT_HIDDEN_NEURON[i], AMOUNT_ENTRY_NEURON) for i in
                             range(len(AMOUNT_HIDDEN_NEURON))]
        self.OutLayer = Layer(AMOUNT_OUT_NEURON, AMOUNT_HIDDEN_NEURON[-1])

        self.InitializeWeights()

    def InitializeWeights(self):
        for i in range(len(self.HiddenLayers)):
            for j in range(len(self.HiddenLayers[i].Neurons)):
                if i == 0:
                    for k in range(len(self.EntryLayer.Neurons)):
                        self.HiddenLayers[i].Neurons[j].Weights.append(
                            random.uniform(-INITIAL_WEIGHT_RATE, INITIAL_WEIGHT_RATE))
                elif i == len(self.HiddenLayers) - 1:
                    for k in range(len(self.OutLayer.Neurons)):
                        self.HiddenLayers[i].Neurons[j].Weights.append(
                            random.uniform(-INITIAL_WEIGHT_RATE, INITIAL_WEIGHT_RATE))
                else:
                    for k in range(len(self.HiddenLayers[i + 1].Neurons)):
                        self.HiddenLayers[i].Neurons[j].Weights.append(
                            random.uniform(-INITIAL_WEIGHT_RATE, INITIAL_WEIGHT_RATE))
        for j in range(len(self.OutLayer.Neurons)):
            for k in range(len(self.HiddenLayers[-1].Neurons)):
                self.OutLayer.Neurons[j].Weights.append(
                    random.uniform(-INITIAL_WEIGHT_RATE, INITIAL_WEIGHT_RATE))

    def Think(self, character, gamemode):
        self.FeedEntryLayer(character, gamemode)
        self.CalculateWeights()
        self.LastCalculatedOutput = self.GetOutput()

    def FeedEntryLayer(self, character, gamemode):
        EntryParams = GetEntryParams(character, gamemode)
        for i in range(len(self.EntryLayer.Neurons) - BIAS):
            self.EntryLayer.Neurons[i].OutValue = int(EntryParams[i])

    def CalculateWeights(self):
        self.Calculate_First_Hidden_Layer_Weights()
        self.Calculate_Hidden_Layers_Weights()
        self.Calculate_Out_Layer_Weights()

    def Calculate_Out_Layer_Weights(self):
        for j in range(len(self.OutLayer.Neurons)):
            Sum = 0
            for k in range(len(self.OutLayer.Neurons[j].Weights)):
                Sum += self.OutLayer.Neurons[j].Weights[k] * self.HiddenLayers[-1].Neurons[k].OutValue
            self.OutLayer.Neurons[j].OutValue = relu(Sum)

    def Calculate_Hidden_Layers_Weights(self):
        for i in range(1, len(self.HiddenLayers)):
            for j in range(len(self.HiddenLayers[i].Neurons)):
                Sum = 0
                for k in range(len(self.HiddenLayers[i].Neurons[j].Weights)):
                    Sum += self.HiddenLayers[i].Neurons[j].Weights[k] * self.HiddenLayers[i - 1].Neurons[k].OutValue
                self.HiddenLayers[i].Neurons[j].OutValue = relu(Sum)

    def Calculate_First_Hidden_Layer_Weights(self):
        for j in range(len(self.HiddenLayers[0].Neurons)):
            Sum = 0
            for k in range(len(self.HiddenLayers[0].Neurons[j].Weights)):
                HiddenLayerWeight = self.HiddenLayers[0].Neurons[j].Weights[k]
                InputValue = self.EntryLayer.Neurons[k].OutValue
                Sum = Sum + HiddenLayerWeight * InputValue
            self.HiddenLayers[0].Neurons[j].OutValue = relu(Sum)

    def GetOutput(self):
        GreaterOutValueIndex = -1
        Output = []
        for i in range(len(self.OutLayer.Neurons)):
            if self.OutLayer.Neurons[i].OutValue > self.OutLayer.Neurons[GreaterOutValueIndex].OutValue:
                GreaterOutValueIndex = i
        for i in range(len(self.OutLayer.Neurons)):
            if i != GreaterOutValueIndex:
                Output.append(0)
            else:
                Output.append(1)
        if GreaterOutValueIndex == -1:
            Output[-1] = 1
        return Output

    def GetWeightAmount(self):
        Sum = 0
        for i in range(len(self.HiddenLayers)):
            for j in range(len(self.HiddenLayers[i].Neurons)):
                Sum += len(self.HiddenLayers[i].Neurons[j].Weights)

        for j in range(len(self.OutLayer.Neurons)):
            Sum += len(self.OutLayer.Neurons[j].Weights)
        return Sum
