# Description: This file contains the neural network class and its functions
import random
import utils
from layer import Layer

INITIAL_WEIGHT_RATE = 1.0
BIAS = 1
AMOUNT_ENTRY_NEURON = 6 + BIAS
AMOUNT_HIDDEN_NEURON = [6 + BIAS]
AMOUNT_OUT_NEURON = 6


def relu(x):
    return max(0, x)


def get_entry_params(character, gamemode):
    (log_x_dist, log_y_dist) = utils.get_closest_log_dist(character.current_location, gamemode.current_background)
    (enemy_x_dist, enemy_y_dist) = utils.get_closest_enemy_dist(character, gamemode)
    return [
        log_x_dist > 0,
        log_x_dist == 0,
        log_y_dist > 0,
        log_y_dist == 0,
        abs(enemy_x_dist) <= 64 and abs(enemy_y_dist) <= 64,  # is side by side of an enemy
        character.has_knife
    ]


class NeuralNetwork:
    entry_layer = None
    hidden_layer = []
    out_layer = None

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
                        self.hidden_layers[i].neurons[j].weights.append(
                            random.uniform(-INITIAL_WEIGHT_RATE, INITIAL_WEIGHT_RATE))
                elif i == len(self.hidden_layers) - 1:
                    for k in range(len(self.out_layer.neurons)):
                        self.hidden_layers[i].neurons[j].weights.append(
                            random.uniform(-INITIAL_WEIGHT_RATE, INITIAL_WEIGHT_RATE))
                else:
                    for k in range(len(self.hidden_layers[i + 1].neurons)):
                        self.hidden_layers[i].neurons[j].weights.append(
                            random.uniform(-INITIAL_WEIGHT_RATE, INITIAL_WEIGHT_RATE))
        for j in range(len(self.out_layer.neurons)):
            for k in range(len(self.hidden_layers[-1].neurons)):
                self.out_layer.neurons[j].weights.append(
                    random.uniform(-INITIAL_WEIGHT_RATE, INITIAL_WEIGHT_RATE))

    def think(self, character, gamemode):
        self.feed_entry_layer(character, gamemode)
        self.calculate_weights()
        self.last_calculated_output = self.get_output()

    def feed_entry_layer(self, character, gamemode):
        entry_params = get_entry_params(character, gamemode)
        for i in range(len(self.entry_layer.neurons) - BIAS):
            self.entry_layer.neurons[i].out_value = int(entry_params[i])

    def calculate_weights(self):
        self.calculate_first_hidden_layer_weights()
        self.calculate_hidden_layers_weights()
        self.calculate_out_layer_weights()

    def calculate_out_layer_weights(self):
        for j in range(len(self.out_layer.neurons)):
            weights_sum = 0
            for k in range(len(self.out_layer.neurons[j].weights)):
                weights_sum += self.out_layer.neurons[j].weights[k] * self.hidden_layers[-1].neurons[k].out_value
            self.out_layer.neurons[j].out_value = relu(weights_sum)

    def calculate_hidden_layers_weights(self):
        for i in range(1, len(self.hidden_layers)):
            for j in range(len(self.hidden_layers[i].neurons)):
                weights_sum = 0
                for k in range(len(self.hidden_layers[i].neurons[j].weights)):
                    weights_sum += self.hidden_layers[i].neurons[j].weights[k] * self.hidden_layers[i - 1].neurons[k].out_value
                self.hidden_layers[i].neurons[j].out_value = relu(weights_sum)

    def calculate_first_hidden_layer_weights(self):
        for j in range(len(self.hidden_layers[0].neurons)):
            weights_sum = 0
            for k in range(len(self.hidden_layers[0].neurons[j].weights)):
                hidden_layer_weight = self.hidden_layers[0].neurons[j].weights[k]
                input_value = self.entry_layer.neurons[k].out_value
                weights_sum = weights_sum + hidden_layer_weight * input_value
            self.hidden_layers[0].neurons[j].out_value = relu(weights_sum)

    def get_output(self):
        greater_out_value_index = -1
        output = []
        for i in range(len(self.out_layer.neurons)):
            if self.out_layer.neurons[i].out_value > self.out_layer.neurons[greater_out_value_index].out_value:
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
        weights_sum = 0
        for i in range(len(self.hidden_layers)):
            for j in range(len(self.hidden_layers[i].neurons)):
                weights_sum += len(self.hidden_layers[i].neurons[j].weights)

        for j in range(len(self.out_layer.neurons)):
            weights_sum += len(self.out_layer.neurons[j].weights)
        return weights_sum
