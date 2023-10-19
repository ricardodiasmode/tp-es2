import neuron


class Layer:
    def __init__(self, amount_neuron, amount_connections):
        self.neurons = [neuron.Neuron(amount_connections) for i in range(amount_neuron)]
