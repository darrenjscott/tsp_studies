import matplotlib.pyplot as plt


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
        ax.legend()

    plt.show()
