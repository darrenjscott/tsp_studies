# Different algorithms for building networks to test
import numpy as np
from plotting_routines import plot_clusters

# Entry point from user commands
def gen_clustNet():
    n_nodes = 200
    seed = 173
    n_clust = int(input("How many clusters: "))
    # Scatter points randomly
    node_coords = build_cluster(n_nodes, n_clust, seed)
    # Cluster according to requirements
    clusters_coords = cluster_nodes_randomly(node_coords, n_clust, seed)
    # Calculate distances
    # weights = calc_weights(clusters_coords)
    # Plot
    plot_clusters(clusters_coords)


# Constructs a network where weights are randomly chosen from a beta distribution (most nodes are nearer)
# Each cluster of nodes has the same number of samples in it
def build_random_weight(n_starts, n_ends, round=2, seed=None):
    # subtract one from n_groups - we only need as many matrices as gaps
    alpha = 2
    beta = 5
    rng = np.random.default_rng(seed)
    return np.around(rng.beta(alpha, beta, size=(n_starts, n_ends)), round)


def cluster_nodes_randomly(coords, n_groups, seed=None):
    rng = np.random.default_rng(seed)
    # Want to avoid splits which generate empty lists - avoid consecutive numbers
    split_pos = rng.integers(len(coords), size=n_groups-1)
    while len(np.unique(split_pos)) != n_groups-1:
        split_pos = rng.integers(len(coords), size=n_groups - 1)

    # Shuffle the list of coordinates first, since otherwise this would just be cutting a
    # pre-existing order
    rng.shuffle(coords)
    return np.split(coords,np.sort(split_pos))


def build_cluster(n_points, round=2, seed=None):
    """
    Returns coordinates for n_nodes normally distributed on a 2D plane.
    :param n_points: Number of points to generate
    :param round: Decimal points to keep per node coordinate
    :param seed: Random seed
    :return: 2D NumPy array of coordinates
    """
    cent = 0.0
    std_dev = 1
    rng = np.random.default_rng(seed)
    return np.around(rng.normal(cent, std_dev, size=(n_points, 2)), round)