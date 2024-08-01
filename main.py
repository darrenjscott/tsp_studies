# Main file for tsp problem analysis
from nearest_neighbours import nearest_neighbours as nn_algo
from brute_force import brute_force
from circle_algos import circle_algo
import network_construction as netcon
from string import ascii_uppercase
import numpy as np
import matplotlib.pyplot as plt
from plotting_routines import plot_clusters

n_nodes = 4
n_groups = 6
rounding = 2
seed = 1733

# Top level entry
def mainLoop():
    print("Travelling salesman type algorithms")
    available_char = ''
    while True:
        print("")
        print("Please pick an option:")
        print("\t 1 : Generate random network of clustered nodes")
        print("\t 2 : Route finding (generate/provide a network first)")
        print("\t 10 : Plot nodes")

        print("\t -1: Quit")
        userCommand = int(input("Please select an option: "))

        match userCommand:
            case 1:
                # Generates a network of nodes, clustered into groups
                # weights
                cluster_coords, weights = netcon.gen_clustNet()
                available_char = ascii_uppercase[:len(cluster_coords)]

            case 2:
                route_test(weights, available_char)

            case 10:
                plot_clusters(cluster_coords)
            case -1:
                return 0


def get_ordered_weights(weights, route):
    ordered_weights = []
    for idC, char in enumerate(route[:-1]):
        weight_key_raw = char + route[idC+1]
        weight_key_sorted = ''.join(sorted(weight_key_raw))

        if weight_key_raw == weight_key_sorted:
            ordered_weights.append(weights[weight_key_sorted])
        else:
            ordered_weights.append(np.transpose(weights[weight_key_sorted]))

    return ordered_weights


def route_test(weights, available_char):
    print("Pick an algorithm, followed by the sequence you want to follow.")
    print("For example, enter:")
    print("1 ADCBD")
    print("to select algorithm 1 to follow the route A -> D -> C -> B -> D.")
    print("Currently available characters:" + available_char)
    print("Currently available algorithms:")
    print("\t 1. Brute force")
    print("\t 2. Nearest neighbours")
    print("\t 3. Circle algorithm")
    algo_choice, route = input('Enter your selection: ').split()
    algo_choice = int(algo_choice)
    route = route.upper()

    # Gets a list of the relevant weight arrays
    ordered_weights = get_ordered_weights(weights, route)

    print(" Choices per cluster:")
    for w in ordered_weights:
        print(w.shape)

    print("*************")

    match algo_choice:
        case 1:
            # Should be fixed to return weights of individual paths between nodes for a given route
            route_weights, route_paths = brute_force(ordered_weights)
            print("****** Brute Force ******")
            print(f"Route weights: {route_weights}")
            print(f"Route paths: {route_paths}")

        case 2:
            # Should be fixed to return weights of individual paths between nodes for a given route
            route_weight, route_path = nn_algo(ordered_weights)
            print("****** Nearest Neighbour ******")
            print(f"Route weight: {route_weight}")
            print(f"Route path: {route_path}")

        case 3:
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
