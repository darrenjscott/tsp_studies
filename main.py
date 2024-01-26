# File for testing various algorithms for the 'sequential ordering problem'

import random
import numpy as np

random.seed(1690)

# Might be better to eventually combine the following functions in to a class, so that sets of different weights can be stored for different networks

def build_random_matrix(rows, columns):
    # Settings for random number generation (seed set once)
    alpha = 2
    beta = 5
    return np.array([[random.betavariate(alpha, beta) for _ in range(columns)] for _ in range(rows)], np.float32)


def build_test_network(n_hubs, n_verts):
    weights = {}

    for h1 in range(n_hubs-1):
        for h2 in range(h1+1, n_hubs):
            weights[''.join(sorted(str(h1)+str(h2)))] = build_random_matrix(n_verts, n_verts)

    return weights


weight_dict = build_test_network(4,3)

target_word = '3120'

weight_list = []

for c in range(len(target_word) - 1):
    weight_key = ''.join(sorted(target_word[c] + target_word[c+1]))
    weight_list.append(weight_dict[weight_key])


print(len(weight_list))
test_w = weight_list[0]
for pub_num, pub in enumerate(test_w):
    print(str(pub_num) + " LOL " + str(pub))
