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


def constrained_nn(start_id, end_id, weights, route):
    # Track visited clusters
    # -> Avoid visiting the same node for repeated clusters
    # Keeps a dictionary where the keys are the cluster names and the values are a list of the nodes visited
    visited_cluster_nodes = {cluster: [] for cluster in set(route)}
    visited_cluster_nodes[route.cluster_sequence[0]].append(start_id)

    # Lowest weight node from next cluster
    # Updated to avoid rare case of repeated first two letters
    # The first part of this logic is unnecessary on entering the loop
    next_cluster = route.cluster_sequence[1]
    if visited_cluster_nodes[next_cluster] != []:
        idx_nearest = np.argsort(weights[0][start_id])
        for n, idx in enumerate(idx_nearest):
            if idx not in visited_cluster_nodes[next_cluster]:
                next_id = idx
                next_weight = weights[0][start_id][idx]
                break

            # If we exhausted the list, just reuse the nearest node, provided it is not the same as the current one
            # (There has to be a better way to do this)
            if (n == len(idx_nearest) - 1):
                # This first if statement should always fire for repeated first clusters:
                # The smallest element would be 0 for repeated letters and be on the diagonal.
                # So we pick the second smallest
                if idx_nearest[0] == start_id:
                    next_id = idx_nearest[1]
                    next_weight = weights[0][start_id][next_id]
                else:
                    next_id = idx_nearest[0]
                    next_weight = weights[0][start_id][next_id]

    else:
        next_weight = np.min(weights[0][start_id])
        next_id = np.argmin(weights[0][start_id])








    route.add_node(start_id)
    route.add_weight(next_weight)
    route.add_node(next_id)

    # Cycle through remaining weights
    # Do not include last node as this is preset
    remaining_weights = weights[1:-1]

    while remaining_weights:
        idx_last = route.path[-1]
        next_weight_matrix = remaining_weights[0]
        smallest_weight = np.min(next_weight_matrix[idx_last])
        smallest_weight_idx = np.argmin(next_weight_matrix[idx_last])

        route.add_weight(smallest_weight)
        route.add_node(smallest_weight_idx)
        remaining_weights = remaining_weights[1:]


    end_weight = weights[-1][route.path[-1]][end_id]

    route.add_weight(end_weight)
    route.add_node(end_id)

    #return route



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
