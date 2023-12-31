import neuralNetwork

class TestNeuralNet:

    def test_layers_initialization(self):
        neural_network = neuralNetwork.NeuralNetwork()
        assert neural_network.entry_layer is not None
        assert len(neural_network.hidden_layers) > 0
        assert neural_network.out_layer is not None

    def test_neurons_initialization(self):
        neural_network = neuralNetwork.NeuralNetwork()
        assert len(neural_network.entry_layer.neurons) == neuralNetwork.AMOUNT_ENTRY_NEURON
        for i in range(len(neural_network.hidden_layers)):
            assert len(neural_network.hidden_layers[i].neurons) == neuralNetwork.AMOUNT_HIDDEN_NEURON[i]
        assert len(neural_network.out_layer.neurons) == neuralNetwork.AMOUNT_OUT_NEURON

    def test_weights_initialization(self):
        neural_network = neuralNetwork.NeuralNetwork()
        assert len(neural_network.entry_layer.neurons) == len(neural_network.hidden_layers[0].neurons[0].weights)
        assert len(neural_network.out_layer.neurons) == len(neural_network.hidden_layers[0].neurons[0].weights) - 1
