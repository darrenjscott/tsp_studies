########
# To implement:
# 1. If visiting the same cluster more than once non-consecutively, avoid previously visited nodes.


import tracemalloc  # testing memory issues
import profiler
import gc


def brute_force(weights):
    """
    Takes an order list of weight matrices and calculates, by brute force (checking all possibilities)
    the shortest path from any of the starting vertices to any vertex in the end cluster.
    It ignores weights which are 0 (since this will represent the same node, for repeated consecutive nodes.
    :param weights: list of matrices describing the weights between nodes
    :param return_all: Whether to return the list of all routes (not implemented)
    :return:
    """

    min_route_a_weights = []
    min_route_a_paths = []

    start_mat = weights[0]
    tracemalloc.start()
    for ida, a in enumerate(start_mat):

        route_weights_temp = []
        route_paths_temp = []
        print(f"Calculating routes starting from a{ida}")
        #mem_use = tracemalloc.get_traced_memory()
        #print(f"Current memory usage: {mem_use[0]/(1024)**2} MB")
        #print(f"Peak memory usage: {mem_use[1]/(1024)**2} MB")
        #print("\n")
        for idb, b in enumerate(a):
            # For repeated clusters, don't pick the same node
            if b == 0:
                continue

            # remaining_routes returns the route weight and the sequence of nodes visited
            for r, idr in remaining_routes(idb, weights[1:]):
                route_weights_temp.append(b + r)
                route_paths_temp.append((ida, idb) + idr)

        min_weight = min(route_weights_temp)
        min_route_a_weights.append(min_weight)
        min_route_a_paths.append(route_paths_temp[route_weights_temp.index(min_weight)])
        #gc.collect()
        #profiler.snapshot()

    #route_min_weight = min(min_route_a_weights)
    #min_route_path = min_route_a_paths[min_route_a_weights.index(route_min_weight)]

    #profiler.display_stats()
    #profiler.compare()
    #profiler.print_trace()

    return min_route_a_weights, min_route_a_paths


def remaining_routes(id, weight_list):
    if not weight_list:
        yield 0, tuple()
    else:
        current_weights = weight_list[0]
        # Making sure to loop along only the correct row
        for idb, b in enumerate(current_weights[id]):
            # Avoid same node twice for consecutively repeated clusters
            if b == 0:
                continue

            for r, idr in remaining_routes(idb,weight_list[1:]):
                yield b + r, (idb,) + idr


