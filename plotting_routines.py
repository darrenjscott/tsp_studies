import numpy as np
import matplotlib.pyplot as plt
import pickle
import scienceplots

plt.style.use(['science', 'notebook'])


def node_coord_plot(coords):
    fig, ax = plt.subplots()
    x_coords, y_coords = coords.transpose()
    ax.scatter(x_coords, y_coords)
    plt.pause(0.1)
    plt.show()


def plot_clusters(clusters):
    fig, ax = plt.subplots()
    for clust_name, coords in clusters.items():
        x_coords, y_coords = coords.transpose()
        ax.scatter(x_coords, y_coords, label=clust_name)
        ax.legend(loc='lower right', ncols=4)

    plt.show()


def plot_routes(list_of_routes, clusters):
    with open('node_names.pkl', 'rb') as fp:
        node_names_dict = pickle.load(fp)

    for nth, route in enumerate(list_of_routes):

        fig, ax = plt.subplots()
        for clust_name, coords in clusters.items():
            x_coords, y_coords = coords.transpose()
            ax.scatter(x_coords, y_coords, label=clust_name)
            ax.legend(loc='lower right', ncols=4)



            route_x_coords = np.array([])
            route_y_coords = np.array([])
            for cluster_idx, cluster in enumerate(route.cluster_sequence):
                cluster_node_coord = clusters[cluster][route.path[cluster_idx]]
                route_x_coords = np.append(route_x_coords, cluster_node_coord[0])
                route_y_coords = np.append(route_y_coords, cluster_node_coord[1])


            ax.plot(route_x_coords, route_y_coords)
            ax.set_title(f"Route {nth+1}")
            ax.legend(loc='lower right', ncols=4)

            # Just a bit hacky for incomplete list of names right now
            for clust_idx, clust_name in enumerate(route.cluster_sequence):
                node_names = node_names_dict[clust_name]
                num_nodes_in_cluster = len(clusters[clust_name])
                if num_nodes_in_cluster > len(node_names):
                    extension_amount = num_nodes_in_cluster - len(node_names)
                    node_names.extend([f"{clust_name}{new_idx}" for new_idx in
                                       range(len(node_names) + 1, len(node_names) + extension_amount + 1)])
                else:
                    node_names = node_names[:num_nodes_in_cluster]

                ANNOTATE_ALL_IN_CLUSTER = True
                if ANNOTATE_ALL_IN_CLUSTER:
                    for node_idx, node in enumerate(clusters[clust_name]):
                        x_coord = node[0]
                        y_coord = node[1]
                        ax.annotate(node_names[node_idx], (x_coord, y_coord))

                else:
                    x_coord = clusters[clust_name][route.path[clust_idx]][0]
                    y_coord = clusters[clust_name][route.path[clust_idx]][1]
                    ax.annotate(node_names[route.path[clust_idx]], (x_coord, y_coord))

    plt.show()
