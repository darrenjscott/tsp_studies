import tracemalloc

def brute_force(weights, return_all=True):
    """
    Takes an order list of weight matrices and calculates, by brute force (checking all possibilities)
    the shortest path from any of the starting vertices to any vertex in the end cluster.
    It ignores weights which are 0 (since this will represent the same node, for repeated consecutive nodes.
    :param weights: list of matrices describing the weights between nodes
    :return:
    """

    all_route_weights = []
    route_weights_starting_a = []
    all_route_sequences = []
    start_mat = weights[0]
    tracemalloc.start()
    for ida, a in enumerate(start_mat):
        route_weights_a = []
        print(f"Calculating routes starting from a{ida}")
        mem_use = tracemalloc.get_traced_memory()
        print(f"Current memory usage: {mem_use[0]/(1024)**2} MB")
        print(f"Peak memory usage: {mem_use[1]/(1024)**2} MB")
        print("\n")
        for idb, b in enumerate(a):
            if b == 0:
                continue

            for r in remaining_routes(idb, weights[1:]):
                all_route_weights.append(b + r)
                route_weights_a.append(b + r)
                #all_route_sequences.append((ida, idb) + idr)
        route_weights_starting_a.append(min(route_weights_a))

    if return_all:
        return all_route_weights, route_weights_starting_a #, all_route_sequences
    else:
        return 0, 0


def remaining_routes(id, weight_list):
    if weight_list == []:
        yield 0
    else:
        current_weights = weight_list[0]
        # Making sure to loop along only the correct row
        for idb, b in enumerate(current_weights[id]):
            if b == 0:
                continue

            for r in remaining_routes(idb,weight_list[1:]):
                yield b + r











