# Main file for tsp problem analysis
from nearest_neighbours import nearest_neighbours as nn_algo
from brute_force import brute_force as bf_algo
import network_construction as netcon
#import plotting_routines as pr

n_nodes = 4
n_groups = 6
rounding = 2
seed = 1733

# TOp level entry
print("Travelling salesman type algorithms")
print("Here are some options currently available:")
print("1 : Generate random network of clustered nodes")
print("-1: Quit")

userCommand = int(input("Please select an option: "))

match userCommand:
    case 1:
        netcon.gen_clustNet()
    case -1:
        exit()







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

