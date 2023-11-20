class Neuron:
    def __init__(self, in_connection_amount):
        self.weights = []
        self.error = 0.0
        self.out_value = 1.0
        self.connection_amount = in_connection_amount
