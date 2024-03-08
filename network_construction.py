# Different algorithms for building networks to test
import numpy as np


# Constructs a network where weights are randomly chosen from a beta distribution (most nodes are nearer)
# Each cluster of nodes has the same number of samples in it
def build_test_network(rows, columns, n_groups, round=2):
    rng = np.random.default_rng(1733)
    # subtract one from n_groups - we only need as many matrices as gaps
    alpha = 2
    beta = 5
    return [np.around(rng.beta(alpha, beta, size=(rows, columns)), round) for _ in range(n_groups - 1)]