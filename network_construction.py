# Different algorithms for building networks to test
import numpy as np


# Constructs a network where weights are randomly chosen from a beta distribution (most nodes are nearer)
# Each cluster of nodes has the same number of samples in it
def build_test_network(rows, columns, n_groups, round=2, seed=None):
    # subtract one from n_groups - we only need as many matrices as gaps
    alpha = 2
    beta = 5
    rng = np.random.default_rng(seed)
    return [np.around(rng.beta(alpha, beta, size=(rows, columns)), round) for _ in range(n_groups - 1)]


def cluster_nodes_randomly(coords, n_groups, seed=None):
    rng = np.random.default_rng(seed)
    split_pos = rng.integers(len(coords), size=n_groups-1)
    # Shuffle the list of coordinates first, since otherwise this would just be cutting a
    # pre-existing order
    rng.shuffle(coords)
    return np.split(coords,split_pos)


def build_cluster(n_points, round=2, seed=None):
    cent = 0.0
    std_dev = 1.0
    rng = np.random.default_rng(seed)
    return np.around(rng.normal(cent, std_dev, size=(n_points, 2)), round)