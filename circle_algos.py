import numpy as np

def circle_algo(weights, start_end_weights):
    start_end_shape = start_end_weights.shape
    start_end_min_weight = np.min(start_end_weights)
    start_end_idx_raw = np.argmin(start_end_weights)
    start_idx, end_idx = np.unravel_index(start_end_idx_raw, start_end_shape)
    print(start_end_weights)
    print("***************")
    print(start_end_min_weight)
    print(start_end_idx_raw)
    print(start_idx)
    print(end_idx)

    return 0, tuple()

# Work out mid points
# Work backwards from end points to mid points using nn