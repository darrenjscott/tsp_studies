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
    visited_cluster_nodes = {cluster: [] for cluster in set(route.cluster_sequence)}
    visited_cluster_nodes[route.cluster_sequence[0]].append(start_id)

    route.add_node(start_id)

    # Cycle through remaining weights
    # Do not include last node as this is preset
    remaining_weights = weights[:-1]
    current_place = 0
    end_cluster = route.cluster_sequence[-1]
    while remaining_weights:
        next_cluster = route.cluster_sequence[current_place + 1]
        idx_previous = route.path[-1]
        next_weight_matrix = remaining_weights[0]

        # If we have visited this cluster before
        # try and avoid visiting the same node
        # Also try and avoid visiting the last node, which is preset
        if visited_cluster_nodes[next_cluster] != [] or next_cluster == end_cluster:
            forbidden_nodes = visited_cluster_nodes[next_cluster]
            if next_cluster == end_cluster:
                forbidden_nodes.append(end_id)

            # Go through nearest nodes in order to find one not on the forbidden list
            idx_nearest = np.argsort(next_weight_matrix[idx_previous])
            for n, idx in enumerate(idx_nearest):
                if idx not in forbidden_nodes:
                    smallest_weight = next_weight_matrix[idx_previous][idx]
                    smallest_weight_idx = idx
                    break

                # If we exhaust the list use the nearest node again provided it is not the node we are already on
                # (unless it is the only node..)
                if n == (len(idx_nearest) - 1):
                    if idx_nearest[0] == idx_previous and n != 0:
                        smallest_weight = next_weight_matrix[idx_previous][idx_nearest[1]]
                        smallest_weight_idx = idx_nearest[1]
                        # No break required. End of loop
                    else:
                        smallest_weight = next_weight_matrix[idx_previous][idx_nearest[0]]
                        smallest_weight_idx = idx_nearest[0]

        else:
            smallest_weight = np.min(next_weight_matrix[idx_previous])
            smallest_weight_idx = np.argmin(next_weight_matrix[idx_previous])


        route.add_weight(smallest_weight)
        route.add_node(smallest_weight_idx)
        visited_cluster_nodes[next_cluster].append(smallest_weight_idx)

        remaining_weights = remaining_weights[1:]
        current_place += 1

    end_weight = weights[-1][route.path[-1]][end_id]

    route.add_weight(end_weight)
    route.add_node(end_id)
    visited_cluster_nodes[route.cluster_sequence[-1]].append(end_id)

    # No longer return - just use function for its side effect
    #return route


def back_iteration(weights, route):
    # Cycle over weight matrix backwards
    # Do not include first matrix, since we back propagate
    for matrix_idxR, weight_matrix in enumerate(reversed(weights[1:])):

        # Get index of canonical ordering
        n_weights = len(weights)
        matrix_idx = n_weights - 1 - matrix_idxR

        end_node = route.path[matrix_idx+1]
        old_start_node_idx = route.path[matrix_idx]

        forbidden_nodes_dict = route.cluster_nodes_visited()
        forbidden_nodes = forbidden_nodes_dict[route.cluster_sequence[matrix_idx]]

        improvement_made = False
        for new_start_node_idx, weight in enumerate(weight_matrix.T[end_node]):
            # If the weight is larger, don't bother testing it (there are scenarios where this could
            # lead to overall improvements, but for now we want to reduce the length of the last leg)
            if (weight >= route.weights[matrix_idx]) or (new_start_node_idx in forbidden_nodes):
                continue

            if (overall_lower_weight(route, weights, matrix_idx, old_start_node_idx, new_start_node_idx)):
                improvement_made = True
                route.path[matrix_idx] = new_start_node_idx
                route.weights[matrix_idx] = weight
                route.weights[matrix_idx - 1] = weights[matrix_idx - 1][route.path[matrix_idx - 1]][new_start_node_idx]

        # If previous node not improved upon then others will not change
        # They were already constructed to be NN
        if not improvement_made:
            break



# RE THINK ABOUT THIS, ALMOST CERTINALY NOT GOING TO WORK - GET INDICIES RIGHT
def overall_lower_weight(route, weights, cluster_idx, old_idx, new_idx):
    old_total_weight = route.total_weight()
    old_weights = route.weights
    old_path = route.path
    weights_beyond = weights[cluster_idx]
    weights_before = weights[cluster_idx - 1]

    new_before_weight = weights_before[old_path[cluster_idx - 1]][new_idx]
    new_beyond_weight = weights_beyond[new_idx][old_path[cluster_idx + 1]]


    new_weights = old_weights.copy()
    new_weights[cluster_idx] = new_beyond_weight
    new_weights[cluster_idx - 1] = new_before_weight

    return np.sum(new_weights) < old_total_weight





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
