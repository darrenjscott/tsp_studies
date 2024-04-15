# Main file for tsp problem analysis
from nearest_neighbours import nearest_neighbours as nn_algo
from brute_force import brute_force
import network_construction as netcon
from string import ascii_uppercase
import numpy as np
import matplotlib.pyplot as plt
#import plotting_routines as pr

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
        print("\t 2 : Route finding (generate/provide a network first")
        print("\t -1: Quit")
        userCommand = int(input("Please select an option: "))
        match userCommand:
            case 1:
                cluster_coords, weights = netcon.gen_clustNet()
                available_char = ascii_uppercase[:len(cluster_coords)]
            case 2:
                route_test(weights, available_char)
            case -1:
                return 0


def get_ordered_weights(weights, route):
    ordered_weights = []
    for idC, char in enumerate(route[:-1]):
        weight_key = char + route[idC+1]
        ordered_weights.append(weights[weight_key])

    return ordered_weights


def route_test(weights, available_char):
    print("Pick an algorithm, followed by the sequence you want to follow.")
    print("For example, enter:")
    print("1 'ADCBD'")
    print("to select algorithm 1 to follow the route A -> D -> C -> B -> D.")
    print("Currently available characters:" + available_char)
    print("Currently available algorithms:")
    print("\t 1. Brute force")
    algo_choice, route = input('Enter your selection: ').split()
    algo_choice = int(algo_choice)
    route = route.upper()

    ordered_weights = get_ordered_weights(weights, route)

    match algo_choice:
        case 1:
            all_route_weights, route_weights_starting_a = brute_force(ordered_weights)





if __name__ == '__main__':
    mainLoop()

# network = netcon.build_test_network(n_nodes, n_groups, rounding, seed)
# nn_test = nn_algo(network)
# bf_allroutes, bf_test = bf_algo(network)
# print(nn_test)
# print(bf_test)
#
# cities = netcon.build_cluster(15)
# print(cities)
# cities_split = netcon.cluster_nodes_randomly(cities,2)
# print(cities_split)
# print('non-split:' + str(len(cities)))
# print('split:' + str(len(cities_split)))
#
# pr.node_coord_plot(cities)

