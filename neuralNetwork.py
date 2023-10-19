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


def get_entry_params(character, gamemode):
    (log_x_dist, log_y_dist) = utils.get_closest_log_dist(character.current_location, gamemode.current_background)
    return [
        log_x_dist > 0,
        log_x_dist == 0,
        log_y_dist > 0,
        log_y_dist == 0
    ]


class NeuralNetwork:
    entry_layer = []
    hidden_layer = []
    out_layer = []

    last_calculated_output = []

    def __init__(self):
        self.entry_layer = Layer(AMOUNT_ENTRY_NEURON, 0)
        self.hidden_layers = [Layer(AMOUNT_HIDDEN_NEURON[i], AMOUNT_ENTRY_NEURON) for i in
                              range(len(AMOUNT_HIDDEN_NEURON))]
        self.out_layer = Layer(AMOUNT_OUT_NEURON, AMOUNT_HIDDEN_NEURON[-1])

        self.initialize_weights()

    def initialize_weights(self):
        for i in range(len(self.hidden_layers)):
            for j in range(len(self.hidden_layers[i].neurons)):
                if i == 0:
                    for k in range(len(self.entry_layer.neurons)):
                        self.hidden_layers[i].neurons[j].Weights.append(
                            random.uniform(-INITIAL_WEIGHT_RATE, INITIAL_WEIGHT_RATE))
                elif i == len(self.hidden_layers) - 1:
                    for k in range(len(self.out_layer.neurons)):
                        self.hidden_layers[i].neurons[j].Weights.append(
                            random.uniform(-INITIAL_WEIGHT_RATE, INITIAL_WEIGHT_RATE))
                else:
                    for k in range(len(self.hidden_layers[i + 1].neurons)):
                        self.hidden_layers[i].neurons[j].Weights.append(
                            random.uniform(-INITIAL_WEIGHT_RATE, INITIAL_WEIGHT_RATE))
        for j in range(len(self.out_layer.neurons)):
            for k in range(len(self.hidden_layers[-1].neurons)):
                self.out_layer.neurons[j].Weights.append(
                    random.uniform(-INITIAL_WEIGHT_RATE, INITIAL_WEIGHT_RATE))

    def Think(self, character, gamemode):
        self.feed_entry_layer(character, gamemode)
        self.calculate_weights()
        self.last_calculated_output = self.get_output()

    def feed_entry_layer(self, character, gamemode):
        entry_params = get_entry_params(character, gamemode)
        for i in range(len(self.entry_layer.neurons) - BIAS):
            self.entry_layer.neurons[i].OutValue = int(entry_params[i])

    def calculate_weights(self):
        self.calculate_first_hidden_layer_weights()
        self.calculate_hidden_layers_weights()
        self.calculate_out_layer_weights()

    def calculate_out_layer_weights(self):
        for j in range(len(self.out_layer.neurons)):
            sum = 0
            for k in range(len(self.out_layer.neurons[j].Weights)):
                sum += self.out_layer.neurons[j].Weights[k] * self.hidden_layers[-1].neurons[k].OutValue
            self.out_layer.neurons[j].OutValue = relu(sum)

    def calculate_hidden_layers_weights(self):
        for i in range(1, len(self.hidden_layers)):
            for j in range(len(self.hidden_layers[i].neurons)):
                sum = 0
                for k in range(len(self.hidden_layers[i].neurons[j].Weights)):
                    sum += self.hidden_layers[i].neurons[j].Weights[k] * self.hidden_layers[i - 1].neurons[k].OutValue
                self.hidden_layers[i].neurons[j].OutValue = relu(sum)

    def calculate_first_hidden_layer_weights(self):
        for j in range(len(self.hidden_layers[0].neurons)):
            sum = 0
            for k in range(len(self.hidden_layers[0].neurons[j].Weights)):
                hidden_layer_weight = self.hidden_layers[0].neurons[j].Weights[k]
                input_value = self.entry_layer.neurons[k].OutValue
                sum = sum + hidden_layer_weight * input_value
            self.hidden_layers[0].neurons[j].OutValue = relu(sum)

    def get_output(self):
        greater_out_value_index = -1
        output = []
        for i in range(len(self.out_layer.neurons)):
            if self.out_layer.neurons[i].OutValue > self.out_layer.neurons[greater_out_value_index].OutValue:
                greater_out_value_index = i
        for i in range(len(self.out_layer.neurons)):
            if i != greater_out_value_index:
                output.append(0)
            else:
                output.append(1)
        if greater_out_value_index == -1:
            output[-1] = 1
        return output

    def get_weight_amount(self):
        sum = 0
        for i in range(len(self.hidden_layers)):
            for j in range(len(self.hidden_layers[i].neurons)):
                sum += len(self.hidden_layers[i].neurons[j].Weights)

        for j in range(len(self.out_layer.neurons)):
            sum += len(self.out_layer.neurons[j].Weights)
        return sum
