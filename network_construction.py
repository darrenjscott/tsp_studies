# Different algorithms for building networks to test
import numpy as np
from plotting_routines import plot_clusters
from string import ascii_uppercase

# Entry point from user commands
def gen_clustNet():
    seed = 173
    n_nodes = int(input("How many total nodes: "))
    n_clust = int(input("How many clusters: "))

    while n_clust > n_nodes:
        print("Can't make more clusters than there are nodes.")
        print("Try again..")
        n_nodes = int(input("How many total nodes: "))
        n_clust = int(input("How many clusters: "))


    # Scatter points randomly
    node_coords = node_gen(n_nodes, seed)

    # Take previously generated coords and assign to clusters
    # 'cluster_nodes_randomly' clusters so that each group
    # contains a random number of the points
    # Returns a list() of numpy arrays of coords - each np.array() object refers to a separate cluster
    clusters_coords = cluster_nodes_randomly(node_coords, n_clust)

    # Calculate distances
    weights = calc_network_weights(clusters_coords)
    # Plot
    plot_clusters(clusters_coords)

    return clusters_coords, weights


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
    # This needs to be rewritten - potential to end up in infinite loop
    # if the number of groups requested is larger than the number of nodes - try to avoid at input, but rewrite anyway.
    split_pos = rng.integers(1, len(coords), size=n_groups-1)
    while len(np.unique(split_pos)) != n_groups-1:
        split_pos = rng.integers(len(coords), size=n_groups - 1)

    # Shuffle the list of coordinates first, since otherwise this would just be cutting a
    # pre-existing order (not so relevant for randomly generated list, but for other inputs perhaps)
    rng.shuffle(coords)
    return np.split(coords, np.sort(split_pos))


def node_gen(n_points, round=2, seed=None):
    """
    Returns coordinates for n_nodes normally distributed on a 2D plane.
    :param n_points: Number of points to generate
    :param round: Decimal points to keep per node coordinate
    :param seed: Random seed
    :return: 2D NumPy array of coordinates (Nx2)
    """
    cent = 0.0
    std_dev = 1
    rng = np.random.default_rng(seed)
    return np.around(rng.normal(cent, std_dev, size=(n_points, 2)), round)


def calc_weights(coords1, coords2):
    """
    Builds a numpy array of weights between two clusters of nodes
    :param coords1: NumPy array of coords in cluster 1
    :param coords2: NumPy array of coords in cluster 1
    :return weight_matrix: Matrix of weights between points in cluster 1 and points in cluster 2.
    weight_matrix[a,b] gives the weight between point a in cluster 1 and point b in cluster 2.
    """
    weight_matrix = np.zeros(shape=(len(coords1), len(coords2)))
    distance = 0
    # Works out the distance between all sets of two points
    for id1, p1 in enumerate(coords1):
        for id2, p2 in enumerate(coords2):
            distance = np.sqrt(np.sum((p1 - p2)**2))
            weight_matrix[id1,id2] = distance

    return weight_matrix



def calc_network_weights(set_of_clusters):
    """
    Returns a dictionary which defines the distances between all possible points

    :param set_of_clusters: a Python list, where each element is M[i]x2 NumPy array
        where M[i] signifies the number of nodes for cluster i.
    :return: A dictionary of the form {'AA':weightsAA, 'AB':weightsAB, 'AC':weightsAC, ....}
    weightsAB will be a numpy array giving the weights between nodes in cluster A and cluster B
    """
    weights = {}
    for id1, cluster in enumerate(set_of_clusters):
        for id2, next_cluster in enumerate(set_of_clusters[id1:]):
            this_key = ascii_uppercase[id1] + ascii_uppercase[id1 + id2]
            weights[this_key] = calc_weights(cluster, next_cluster)

    return weights


