import numpy as np

class Route:
    def __init__(self, cluster_sequence: list):
        self.cluster_sequence = cluster_sequence
        self.path = [] # Could maybe be a tuple, but might want to edit routes
        self.weights = []
        self.start_end_weight = 0

    def add_node(self, idx):
        self.path.append(idx)

    def add_weight(self, weight):
        self.weights.append(weight)

    def add_start_end_weight(self, weight):
        self.start_end_weight = weight


    def total_weight(self):
        return np.sum(self.weights)


# Class to implement for storing individual routes and sorting, ordering them, whatever
class Route_collection(Route):
    pass
