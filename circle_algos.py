import numpy as np
from nearest_neighbours import constrained_nn, back_iteration
from route_classes import Route

# Still to fix:
# Implement recursive correction (including visited nodes)

def circle_algo(weights, start_end_weights, cluster_sequence):

    list_of_routes = []

    for start_id, start_node in enumerate(weights[0]):

        route = Route(cluster_sequence)

        # Find end node nearest starting node
        end_dist = np.min(start_end_weights[start_id])
        end_id = np.argmin(start_end_weights[start_id])

        route.start_end_weight = end_dist

        # Perform NN from start node to 2nd last node
        constrained_nn(start_id, end_id, weights, route)

        # recursively search nodes either side (except start and end) of highest weight segment
        # Recall constraints related to previously visited nodes
        back_iteration(weights, route)


        list_of_routes.append(route)


    return list_of_routes