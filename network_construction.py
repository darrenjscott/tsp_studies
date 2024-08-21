# Different algorithms for building networks to test
import numpy as np
from plotting_routines import plot_clusters
from string import ascii_uppercase


# Entry point from user commands
def gen_clustNet():
    seed = 173

    # Get network size from user
    n_nodes = int(input("How many total nodes in the network: "))
    n_clust = int(input("How many clusters: "))

    # For testing we want no "clusters" of one node.
    while n_nodes < 2 * n_clust:
        print("For testing, allow for at least two nodes per cluster")
        print("Try again..")
        n_nodes = int(input("How many total nodes: "))
        n_clust = int(input("How many clusters: "))

    # Scatter points randomly
    # node_coords is a Nx2 numpy array - array of 2D coordinates
    node_coords = node_gen(n_nodes, seed)

    # Take previously generated coords and assign to clusters
    # 'cluster_nodes_randomly' groups so that each cluster
    # contains a random number of the points (at least two per cluster)
    # Returns a dict() where:
    #       key:   Cluster name (upper case ascii characters for now)
    #       value: nx2 numpy array of coords (n can be different for different clusters)
    clusters_coords = cluster_nodes_randomly(node_coords, n_clust)

    # This can be used to set a minimum number per cluster - sometimes two is too few
    MIN_PER_CLUSTER = 2
    #MAX_PER_CLUSTER = 15
    def wrongSize(x: dict):
        for thing in x.values():
            if (len(thing) < MIN_PER_CLUSTER): #or (len(thing) > MAX_PER_CLUSTER):
                return True

        return False

    while wrongSize(clusters_coords):
        clusters_coords = cluster_nodes_randomly(node_coords, n_clust)

    # Calculate distances
    # This is a dictionary:
    #       key:   Cluster pair (e.g. 'AD' or 'BB'). Keys always alphabetical - no 'DA' as this is identical to 'AD'
    #       value: 2d nxm numpy array of weights between all nodes in the pair of clusters considered.
    #               the matrix for 'AA' for example, just gives the distances between all the points within that cluster.
    weights = calc_network_weights(clusters_coords)

    plot_clusters(clusters_coords)

    return clusters_coords, weights


def cluster_nodes_randomly(coords, n_groups, seed=None):
    """
    Takes a set of 2D coords and separates them into n_groups clusters - no clusters of size 0 or 1
    :param coords: Nx2 numpy array of coordinates (floats)
    :param n_groups: integer, number of groups to split the coords into
    :param seed: random seed for cluster splitting
    :return: dict, key = cluster name, value = nx2 numpy array of coords in that cluster. n can be different for different clusters
    """

    # Checks sorted np.array of ints for consecutive values
    def consecutive(array):
        for idx, i in enumerate(array[:-1]):
            if i == array[idx+1] - 1:
                return True

        return False

    rng = np.random.default_rng(seed)
    # Want to avoid splits which generate clusters of size 0 or 1.
    # This following should be rewritten - potential to end up in infinite loop
    # if the number of groups requested is larger than the number of nodes - try to avoid at input, but rewrite anyway.


    # The loop will generate positions to split the coordinates at to build clusters
    # Splits no use if:
    #       two split positons are identical (creates and empty cluster)
    #       two split positons are one unit apart (creates clusters of size 1)
    fail_unique = True
    fail_len = True
    split_pos = np.array([])
    while fail_unique or fail_len:
        # Start at 2 and end one below length (which is the upper non-inclusive range)
        # to avoid generating clusters of one at either end
        split_pos = np.sort(rng.integers(2, len(coords)-1, size=n_groups - 1))
        fail_unique = len(np.unique(split_pos)) != n_groups-1
        fail_len = consecutive(split_pos)

    # Not needed here, but if necessary to shuffle list before cutting..
    # rng.shuffle(coords)
    list_of_clusters = np.split(coords, split_pos)

    # Name the clusters by consecutive letters of the alphabet
    # Limits number of clusters to 26 for now - use custom function for other applications
    cluster_dict = dict(zip(ascii_uppercase[:n_groups], list_of_clusters))

    return cluster_dict


def node_gen(n_points, rounding=2, seed=None):
    """
    Returns coordinates for n_nodes normally distributed on a 2D plane.
    :param n_points: Number of points to generate
    :param rounding: Decimal points to keep per node coordinate
    :param seed: Random seed
    :return: 2D NumPy array of coordinates (Nx2)
    """

    # Parameters for random sample (normal distribution - keeps it 'centric'
    # with more nodes clustered tighter around the center
    cent = 0.0
    std_dev = 1
    rng = np.random.default_rng(seed)
    return np.around(rng.normal(cent, std_dev, size=(n_points, 2)), rounding)


def calc_weights(coords1, coords2):
    """
    Builds a numpy array of weights between two clusters of nodes
    :param coords1: NumPy array of coords in cluster 1
    :param coords2: NumPy array of coords in cluster 2
    :return weight_matrix: Matrix of weights between points in cluster 1 and points in cluster 2.
    weight_matrix[ia,ib] gives the weight between point ia in cluster 1 and point ib in cluster 2.
    """
    weight_matrix = np.zeros(shape=(len(coords1), len(coords2)))
    # Works out the distance between all sets of two points
    for id1, p1 in enumerate(coords1):
        for id2, p2 in enumerate(coords2):
            distance = np.sqrt(np.sum((p1 - p2)**2))
            weight_matrix[id1, id2] = distance

    return weight_matrix


def calc_network_weights(set_of_clusters):
    """
    Returns a dictionary which defines the distances between all possible points

    :param set_of_clusters: a Python dict, where each value is M[i]x2 NumPy array
        where M[i] signifies the number of nodes for cluster i. The keys are the cluster names.
    :return: A dictionary of the form {'AA':weightsAA, 'AB':weightsAB, 'AC':weightsAC, ....}
    weightsAB will be a numpy array giving the weights between nodes in cluster A and cluster B etc
    """

    # In Python 3.7 and above dictionaries are actually ordered
    # with that, this could be written more efficiently
    weights = {}
    for clust1_name in set_of_clusters.keys():
        for clust2_name in set_of_clusters.keys():
            # Characters are ordered: 'A' < 'B'
            # avoid computing distance matrix for AB and BA - same thing
            if clust1_name <= clust2_name:
                dist_name = clust1_name + clust2_name
                weights[dist_name] = calc_weights(set_of_clusters[clust1_name], set_of_clusters[clust2_name])

    return weights

#####################################################
# OTHER FUNCTIONS WHICH CAN BE USED FOR TESTING ETC #
#####################################################


# Constructs a network where weights are randomly chosen from a beta distribution (most nodes are nearer)
# Each cluster of nodes has the same number of samples in it
def build_random_weight(n_starts, n_ends, rounding=2, seed=None):
    # subtract one from n_groups - we only need as many matrices as gaps
    alpha = 2
    beta = 5
    rng = np.random.default_rng(seed)
    return np.around(rng.beta(alpha, beta, size=(n_starts, n_ends)), rounding)
