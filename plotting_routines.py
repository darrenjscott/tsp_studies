import matplotlib.pyplot as plt

def node_coord_plot(coords):
    fig, ax = plt.subplots()
    x_coords, y_coords = coords.transpose()
    ax.scatter(x_coords, y_coords)
    plt.show()


def plot_clusters(clustered_coords):
    fig, ax = plt.subplots()
    for cluster in clustered_coords:
        x_coords, y_coords = cluster.transpose()
        ax.scatter(x_coords, y_coords)

    plt.show()