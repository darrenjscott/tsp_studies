import matplotlib.pyplot as plt

def node_coord_plot(coords):
    fig, ax = plt.subplots()
    x_coords, y_coords = coords.transpose()
    ax.scatter(x_coords, y_coords)
    plt.show()