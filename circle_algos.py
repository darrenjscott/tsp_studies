# Possible improvements:
"""
Could cycle through all starting points, find the nearest end point(s) to a given start
and loop round that way.
"""

# To fix:
"""
* Fix incidents of repeated clusters - will currently pick the same node, since it has distance 0
"""

import numpy as np


def circle_algo(weights, se_weights):
    se_shape = se_weights.shape
    se_min_weight = np.min(se_weights)
    se_idx_raw = np.argmin(se_weights)
    start_idx, end_idx = np.unravel_index(se_idx_raw, se_shape)

    route_weight = tuple()
    route_path = (start_idx,)

    # Cycle to second last node
    for w_mat in weights[:-1]:
        route_weight += (np.min(w_mat[route_path[-1]]),)
        route_path += (np.argmin(w_mat[route_path[-1]]),)


    route_weight += (weights[-1][route_path[-1], end_idx],)
    route_path += (end_idx,)

    return route_weight, route_path
