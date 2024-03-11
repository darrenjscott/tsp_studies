# Main file for tsp problem analysis
from nearest_neighbours import nearest_neighbours as nn_algo
from brute_force import brute_force as bf_algo
import network_construction as netcon

rows = 4
columns = 4
n_groups = 6
rounding = 2
seed = 1733

network = netcon.build_test_network(rows, columns, n_groups, rounding, seed)
nn_test = nn_algo(network)
bf_allroutes, bf_test = bf_algo(network)
print(nn_test)
print(bf_test)

