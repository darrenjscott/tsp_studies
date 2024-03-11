# An algorithm which works just by picking the neightbour which is closest
# It does this for each starting pub and returns a list with the shortest route from each starting position
import numpy as np


def nearest_neighbours(weights):
    nn_routes = []
    for a in weights[0]:
        nearest_idx = np.argmin(a)
        route_weight = recursive_nearest(nearest_idx, min(a), weights[1:])
        nn_routes.append(route_weight)

    return nn_routes


def recursive_nearest(idx, current_weight, weight_list):
    if weight_list == []:
        return current_weight
    else:
        next_weights = weight_list[0]
        smallest_weight = min(next_weights[idx])
        nearest_idx = np.argmin(next_weights[idx])
        current_weight = recursive_nearest(nearest_idx, current_weight + smallest_weight, weight_list[1:])
        return current_weight
