import numpy as np
from nearest_neighbours import constrained_nn


def circle_algo(weights, start_end_weights):

    routes = {}
    for start_id, start_node in enumerate(weights[0]):
        # Find end node nearest starting node
        end_dist = np.min(start_end_weights[start_id])
        end_id = np.argmin(start_end_weights[start_id])

        # Perform NN from start node to 2nd last node
        paths, path_weights = constrained_nn(start_id, end_id, weights)

        # recursively search nodes either side (except start and end) of highest weight segment

        #DEBUG COMMENT
        break

    #route_weight = tuple()
    #route_path = []
    route_weight = path_weights
    route_path = paths
    return route_weight, route_path
    #print("")
    #print("path (for b0)")
    #print("")