import matplotlib.pyplot as plt
from string import ascii_uppercase

def node_coord_plot(coords):
    fig, ax = plt.subplots()
    x_coords, y_coords = coords.transpose()
    ax.scatter(x_coords, y_coords)
    plt.pause(0.1)
    plt.show()


def plot_clusters(clustered_coords,labels=None):

    if labels is None:
        labels = [c for c in ascii_uppercase]

    fig, ax = plt.subplots()
    for id, cluster in enumerate(clustered_coords):
        x_coords, y_coords = cluster.transpose()
        ax.scatter(x_coords, y_coords, label=labels[id])
        ax.legend()

    plt.show()
