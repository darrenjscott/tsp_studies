# Main file for tsp problem analysis
from keyring.backends.libsecret import available

from nearest_neighbours import nearest_neighbours as nn_algo
from brute_force import brute_force
from circle_algos import circle_algo
import network_construction as netcon
from string import ascii_uppercase
import numpy as np
import clust_io
import matplotlib.pyplot as plt
from plotting_routines import plot_clusters

import pickle

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
            case 0: # DEBUG MODE
                with open('validation_weights.pkl', 'rb') as fp:
                    weights = pickle.load(fp)
                    available_char = ''.join(sorted(set(''.join(weights.keys()))))
                    print('Using validation weights')
                    for key, vals in weights.items():
                        print(f"Distance: {key}")
                        print(vals)

                    print("Available chars:", available_char)

            case 1: # USE RANDOM NETWORK
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

            case 2: # Try some routefinding algorithms
                route_test(weights, available_char)

            case 10: # Node info
                print("** Nodes per cluster **")
                for clust_name, clust_coords in cluster_coords.items():
                    print(f"{clust_name}: {len(clust_coords)}")

                # Can add prints for other info - weights is too much
                print(weights)

            case 11: # Plot nodes
                plot_clusters(cluster_coords)
#            case 12:
#                with open('validation_weights.pkl', 'wb') as fp:
#                    pickle.dump(weights, fp)
#                    print('dictionary saved successfully to file')

            case -1: # Quit
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

        case 3: # Circle
            # Need weights between start and end points for this algorithm
            start_end_nodes = route[0] + route[-1]
            start_end_weights = get_ordered_weights(weights, start_end_nodes)

            route_weights, route_paths, displacement_weights = circle_algo(ordered_weights, start_end_weights[0])
            print("****** Circle ******")
            for idx, specific_path in enumerate(route_paths):
                wgts = route_weights[idx]
                wgts_first_last = displacement_weights[idx]
                print(f"Route: {specific_path}")
                print(f"Route weights: {wgts}")
                print(f"Total weight: {np.sum(wgts)}")
                print(f"Distance between end node and starting node: {wgts_first_last}")


# This is not used yet
class Route:
    def __init__(self, clusters: list, path: list, weights: list):
        self.clusters = clusters
        self.path = path
        self.weights = weights

    def total_weight(self):
        return np.sum(self.weights)


if __name__ == '__main__':
    mainLoop()
