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
    path = []
    path_weights = []

    for node, weight in enumerate(weights[0][start_id]):
        # Lowest weight node from next cluster
        next_weight = np.min(weight)
        next_id = np.argmin(weight)

        # Recursively search through from 2nd to 2nd last node
        if weights[1:-1] != []:
            path_weight_a, path_a = recursive_nearest(next_id, next_weight, weights[1:-1])
        else:
            path_weight_a = [next_id]
            path_a = [next_id]

        end_weight = weights[-1][path_a[-1]][end_id]

        path_weights.append([path_weight_a + end_weight])
        path.append([start_id, next_id] + path_a + [end_id])

    return path, path_weights



def recursive_nearest(idx, current_weight, weight_list):
    # If no more clusters to visit
    if not weight_list:
        return current_weight, []
    else:
        next_weight_matrix = weight_list[0]
        smallest_weight = np.min(next_weight_matrix[idx])
        nearest_idx = np.argmin(next_weight_matrix[idx])
        new_weight, path_idx = recursive_nearest(nearest_idx, current_weight + smallest_weight, weight_list[1:])
        return new_weight, [nearest_idx] + [path_idx]
