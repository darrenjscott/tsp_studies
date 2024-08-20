import numpy as np
from nearest_neighbours import constrained_nn

# Still to fix
# Avoid visiting nodes already visited within the same group
# As above but for start end nodes if they are in the same group
# Implement recursive correction (including visited nodes)

def circle_algo(weights, start_end_weights):

    route_paths = []
    route_weights = []
    start_end_weight = []
    for start_id, start_node in enumerate(weights[0]):
        # Find end node nearest starting node
        end_dist = np.min(start_end_weights[start_id])
        end_id = np.argmin(start_end_weights[start_id])

        # Perform NN from start node to 2nd last node
        path, path_weight = constrained_nn(start_id, end_id, weights)

        # recursively search nodes either side (except start and end) of highest weight segment
        # TO IMPLEMENT


        route_paths.append(path)
        route_weights.append(path_weight)
        start_end_weight.append(end_dist)



    return route_weights, route_paths, start_end_weight