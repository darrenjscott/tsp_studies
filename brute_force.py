def brute_force(weight_list):
    """
    Takes an order list of weight matrices and calculates, by brute force (checking all possibilities)
    the shortest path from any of the starting vertices and
    :param weight_list:
    :return:
    """
    num_nodes = len(weight_list)
    path_route = []
    path_weight = 0
    def update_and_move(ind_a, ind_b, ind_mat):
        nonlocal path_weight
        path_weight += ind_mat[ind_a, ind_b]
        path_route.append(ind_b)
        if ind_mat == num_nodes:
            return (path_weight, path_route)
        else:










