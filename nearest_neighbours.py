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


def constrained_nn(start_id, end_id, weights):
    path = [start_id]
    path_weights = []

    # Lowest weight node from next cluster
    next_weight = np.min(weights[0][start_id])
    next_id = np.argmin(weights[0][start_id])

    path_weights.append(next_weight)
    path.append(next_id)

    # Recursively search through from 2nd to 2nd last node
    if weights[1:-1] != []:
        path, path_weights = recursive_nearest(path, path_weights, weights[1:-1])

    end_weight = weights[-1][path[-1]][end_id]

    path_weights.append(end_weight)
    path.append(end_id)

    return path, path_weights



def recursive_nearest(path, path_weights, weight_list):
    # If no more clusters to visit
    if not weight_list:
        return path, path_weights
    else:
        idx_last = path[-1]
        next_weight_matrix = weight_list[0]
        smallest_weight = np.min(next_weight_matrix[idx_last])
        smallest_weight_idx = np.argmin(next_weight_matrix[idx_last])

        path_weights.append(smallest_weight)
        path.append(smallest_weight_idx)
        path, path_weights = recursive_nearest(path, path_weights, weight_list[1:])

        return path, path_weights
