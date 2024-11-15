"""
Brute Force Method to solve TSP
"""

from itertools import permutations
from time import perf_counter

# graph_mat is a 2D numpy array, cutoff_time is in seconds
def solve(graph_mat, cutoff_time):
    time_begin = perf_counter()
    num_nodes = len(graph_mat)
    all_routes = permutations(range(num_nodes))
    
    min_cost = float("inf")
    best_route = None
    for route in all_routes:
        cost = 0
        for i in range(num_nodes-1):
            cost += graph_mat[route[i],route[i+1]]
            if cost >= min_cost:
                break
        else:
            cost += graph_mat[route[-1], route[0]]
            if cost < min_cost:
                min_cost = cost
                best_route = route
        
        time_end = perf_counter()
        if (time_end - time_begin > cutoff_time):
            return min_cost, best_route
    
    return min_cost, best_route