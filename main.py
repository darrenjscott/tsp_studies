# File for testing various algorithms for the 'sequential ordering problem'

import numpy as np
import network_construction as netcon
from brute_force import brute_force


rows = 2
columns = 2
n_groups = 3
weights = netcon.build_test_network(rows, columns, n_groups)

routes = brute_force(weights)
print("Routes")
print(routes)
