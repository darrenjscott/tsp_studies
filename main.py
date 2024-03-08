# File for testing various algorithms for the 'sequential ordering problem'

import numpy as np
import network_construction as netcon
from brute_force import brute_force
#from plotting_routines import plot_timings
import time
import csv
import pandas as pd
import matplotlib.pyplot as plt

results_full = []
with open('./output/timings.csv','w') as file:
    writer = csv.writer(file)
    fields = ['n_groups', 'n_rows', 'n_cols', 'first_time', 'avg_time']
    writer.writerow(fields)


    for n_groups in range(3,11):
        group_size = 3
        rows = group_size
        columns = group_size
        #weights = netcon.build_test_network(rows, columns, n_groups)
        #routes = brute_force(weights)

        times = []
        s_routes = []
        for _ in range(10):
            weights = netcon.build_test_network(rows, columns, n_groups)
            start = time.perf_counter()
            routes = brute_force(weights)
            shortest = min(routes)
            time_elapsed = time.perf_counter() - start
            times.append(time_elapsed)
            s_routes.append(shortest)

        first_time = times[0]
        other_time = np.mean(times[1:])
        results = [n_groups, rows, columns, first_time, other_time]
        results_full.append(results)
        writer.writerow(results)



timings_df = pd.read_csv('output/timings.csv')

timings_df.plot(x='n_groups',y=['first_time','avg_time'])
plt.xlabel('Number of nodes per cluster')
plt.ylabel('Time taken (s)')
plt.show()