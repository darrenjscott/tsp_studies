# File for holding large chunks of repeated text away from the main loop
# Helps for decluttering

def print_options_main():
    print("")
    print("Please pick an option:")
    print("\t 1 : Generate random network of clustered nodes")
    print("\t 2 : Route finding (generate/provide a network first)")
    print("\t 10 : Plot nodes")

    print("\t -1: Quit")
    userCommand = int(input("Please select an option: "))
    return userCommand


def print_options_route_test(available_clusts):
    print("Pick an algorithm, followed by the sequence you want to follow.")
    print("For example, enter:")
    print("1 ADCBD")
    print("to select algorithm 1 to follow the route A -> D -> C -> B -> D.")
    print("Currently available characters:" + available_clusts)
    print("Currently available algorithms:")
    print("\t 1. Brute force")
    print("\t 2. Nearest neighbours")
    print("\t 3. Circle algorithm")
    algo_choice, route = input('Enter your selection: ').split()
    algo_choice = int(algo_choice)
    route = route.upper()

    return algo_choice, route


def print_clusters_info(cluster_coords):
    print("")
    print("** Number of nodes per cluster **")
    for clust_name, coords in cluster_coords.items():
        print(f"Cluster {clust_name}: {len(coords)}")

    print("")


def print_cluster_seq_info(ordered_weights, route):
    print(" Choices per cluster:")
    for idx, w in enumerate(ordered_weights):
        from_clust_num = w.shape[0]
        to_clust_num = w.shape[1]
        print(f"{route[idx]} to {route[idx+1]}: {from_clust_num} -> {to_clust_num}")

    print("*************")
