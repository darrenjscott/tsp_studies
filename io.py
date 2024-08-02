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
