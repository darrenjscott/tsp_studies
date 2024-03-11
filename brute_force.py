def brute_force(weights):
    """
    Takes an order list of weight matrices and calculates, by brute force (checking all possibilities)
    the shortest path from any of the starting vertices and
    :param weights: list of matrices describing the weights between nodes
    :return:
    """

    all_route_weights = []
    route_weights_starting_a = []
    all_route_sequences = []
    start_mat = weights[0]

    for ida, a in enumerate(start_mat):
        route_weights_a = []
        for idb, b in enumerate(a):
            for r in remaining_routes(idb, weights[1:]):
                all_route_weights.append(b + r)
                route_weights_a.append(b + r)
                #all_route_sequences.append((ida, idb) + idr)
        route_weights_starting_a.append(min(route_weights_a))

    return all_route_weights, route_weights_starting_a #, all_route_sequences



def remaining_routes(id, weight_list):
    if weight_list == []:
        yield 0
    else:
        current_weights = weight_list[0]
        # Making sure to loop along only the correct row
        for idb, b in enumerate(current_weights[id]):
            for r in remaining_routes(idb,weight_list[1:]):
                yield b + r











