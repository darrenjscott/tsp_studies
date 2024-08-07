# Main file for tsp problem analysis
from nearest_neighbours import nearest_neighbours as nn_algo
from brute_force import brute_force
from circle_algos import circle_algo
import network_construction as netcon
from string import ascii_uppercase
import numpy as np
import clust_io
import matplotlib.pyplot as plt
from plotting_routines import plot_clusters

n_nodes = 4
n_groups = 6
rounding = 2
seed = 1733


# Top level entry
def mainLoop():
    print("'Travelling salesman'-like algorithms")
    available_char = ''
    weights = dict()
    cluster_coords = dict()
    while True:
        userCommand = clust_io.print_options_main()

        match userCommand:
            case 1:
                # Generates a network of nodes, clustered into groups
                # cluster_coords is a dictionary:
                #       key:   cluster name (uppercase ascii for now 'A', 'B', etc)
                #       value: numpy array of 2D coords part of that cluster
                # weights is a dictionary of all possible weights between points, listed by cluster:
                #       key:   cluster pair (e.g. 'AB', 'BB', etc)
                #       value: 2d numpy array of weights between all possible points
                cluster_coords, weights = netcon.gen_clustNet()
                available_char = ''.join(list(cluster_coords.keys()))

                clust_io.print_clusters_info(cluster_coords)

            case 2:
                route_test(weights, available_char)

            case 10:
                plot_clusters(cluster_coords)
            case -1:
                return 0


def get_ordered_weights(weights, route):
    ordered_weights = []

    # Since we only construct weight matrices once for each pair (i.e. A->B is just the transpose of B->A)
    # we check if we need to order the two characters and subsequentially transpose the weight matrix
    for idC, char in enumerate(route[:-1]):
        weight_key_raw = char + route[idC+1]
        weight_key_sorted = ''.join(sorted(weight_key_raw))

        if weight_key_raw == weight_key_sorted:
            ordered_weights.append(weights[weight_key_sorted])
        else:
            ordered_weights.append(np.transpose(weights[weight_key_sorted]))

    return ordered_weights


def route_test(weights, available_char):
    # route is a string with the sequence of clusters to visit
    algo_choice, route = clust_io.print_options_route_test(available_char)

    # Gets a list() of the relevant weight arrays, in the order needed
    ordered_weights = get_ordered_weights(weights, route)

    # Print info about cluster sequence
    clust_io.print_cluster_seq_info(ordered_weights, route)

    match algo_choice:
        case 1: # Brute force
            # Should be fixed to return weights of individual paths between nodes for a given route
            route_weights, route_paths = brute_force(ordered_weights)
            print("****** Brute Force ******")
            print(f"Route weights: {route_weights}")
            print(f"Route paths: {route_paths}")
            print("*"*20)
            print(f"Smallest weight: {np.min(route_weights)}")
            print(f"Path: {route_paths[route_weights.index(np.min(route_weights))]}")
            print("*" * 20)

        case 2: # Nearest neighbour
            # TO UPDATE
            # Should be fixed to return weights of individual paths between nodes for a given route
            route_weight, route_path = nn_algo(ordered_weights)
            print("****** Nearest Neighbour ******")
            print(f"Route weight: {route_weight}")
            print(f"Route path: {route_path}")

        case 3: # Circle - to implement
            # Need weights between start and end points for this algorithm
            start_end_nodes = route[0] + route[-1]
            start_end_weights = get_ordered_weights(weights, start_end_nodes)

            route_weight, route_path = circle_algo(ordered_weights, start_end_weights[0])
            tot_weight = np.sum(np.array(route_weight))
            print("****** Circle ******")
            print(f"Total weight: {tot_weight}")
            print(f"Route weights: {route_weight}")
            print(f"Route path: {route_path}")


if __name__ == '__main__':
    mainLoop()
