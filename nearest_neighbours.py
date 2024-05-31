# An algorithm which works just by picking the neightbour which is closest
# It does this for each starting pub and returns a list with the shortest route from each starting position
import numpy as np


def nearest_neighbours(weights):
    route_weights = []
    route_paths = []

    for ida, a in enumerate(weights[0]):
        nearest_idx = np.argmin(a)
        route_weight_a, route_path_a = recursive_nearest(nearest_idx, min(a), weights[1:])
        route_weights.append(route_weight_a)
        route_paths.append((ida, nearest_idx) + route_path_a)

    return route_weights, route_paths


def recursive_nearest(idx, current_weight, weight_list):
    if not weight_list:
        return current_weight, tuple()
    else:
        next_weight_matrix = weight_list[0]
        smallest_weight = min(next_weight_matrix[idx])
        nearest_idx = np.argmin(next_weight_matrix[idx])
        new_weight, path_idx = recursive_nearest(nearest_idx, current_weight + smallest_weight, weight_list[1:])
        return new_weight, (nearest_idx,) + path_idx
