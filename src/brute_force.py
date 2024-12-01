"""
Branch and Bound Method to solve TSP
"""

import heapq
import numpy as np
from time import perf_counter

import approx_algo

class Node:
    def __init__(self, path, cost, bound, level):
        self.path = path        # Current path
        self.cost = cost        # Current cost
        self.bound = bound      # Current bound
        self.level = level      # Current level

    def __lt__(self, other):
        return self.bound < other.bound

def calculate_bound(graph_mat, current_path):
    """
    Calculate the lower bound of the remaining part of the graph
    """
    remaining_nodes = set(range(len(graph_mat))) - set(current_path)
    if not remaining_nodes:
        return 0, []

    sub_graph = graph_mat[np.ix_(list(remaining_nodes), list(remaining_nodes))]

    # Solve the sub-graph using the approximate algorithm
    approx_cost, approx_route = approx_algo.solve(sub_graph)
    # Map sub_graph indices back to original node indices
    remaining_nodes = list(remaining_nodes)
    mapped_route = [remaining_nodes[i] for i in approx_route] if approx_route else []
    return approx_cost, mapped_route

def solve(graph_mat, cutoff_time):
    time_begin = perf_counter()
    num_nodes = len(graph_mat)
    best_cost = float("inf")
    best_route = None
    backup_route = None
    backup_cost = float("inf")

    # Priority queue according to the lower bound
    pq = []

    # Initialize the priority queue with the root node
    initial_path = [0]
    initial_cost = 0
    initial_bound, initial_approx_route = calculate_bound(graph_mat, initial_path)
    initial_node = Node(initial_path, initial_cost, initial_bound, 0)
    heapq.heappush(pq, initial_node)

    while pq:
        current_time = perf_counter()
        if (current_time - time_begin) > cutoff_time:
            break

        # Pop the node with the smallest bound
        current_node = heapq.heappop(pq)

        # If the bound is greater than the best cost, prune the node
        if current_node.bound >= best_cost:
            continue

        # If the current node is a leaf node, update the best cost and route
        if current_node.level == num_nodes - 1:
            last_node = current_node.path[-1]
            total_cost = current_node.cost + graph_mat[last_node][0]
            if total_cost < best_cost:
                best_cost = total_cost
                best_route = current_node.path + [0]
            continue

        # Expand the current node
        for next_node in range(num_nodes):
            if next_node not in current_node.path:
                new_path = current_node.path + [next_node]
                new_cost = current_node.cost + graph_mat[current_node.path[-1]][next_node]

                # Calculate the bound of the new node
                approx_cost, approx_route = calculate_bound(graph_mat, new_path)
                new_bound = new_cost + approx_cost

                if new_bound < best_cost:
                    child_node = Node(new_path, new_cost, new_bound, current_node.level + 1)
                    heapq.heappush(pq, child_node)

                # If the bound is greater than the backup cost, prune the node
                if approx_route:
                    potential_route = new_path + approx_route
                    # Calculate the cost of the potential route
                    potential_cost = new_cost
                    for i in range(len(new_path), len(potential_route)):
                        potential_cost += graph_mat[potential_route[i-1]][potential_route[i]]
                        if potential_cost >= backup_cost:
                            break
                    else:
                        # Add the cost from the last node to the starting node
                        potential_cost += graph_mat[potential_route[-1]][0]
                        if potential_cost < backup_cost:
                            backup_cost = potential_cost
                            backup_route = potential_route + [0]

    # Return the best cost and route
    if best_route is not None:
        return best_cost, best_route
    else:
        # Return the backup route if it exists
        if backup_route is not None:
            return backup_cost, backup_route
        else:
            # Return the approximate solution if no solution is found
            approx_cost, approx_route = approx_algo.solve(graph_mat)
            mapped_route = approx_route + [approx_route[0]] if approx_route else []
            return approx_cost, mapped_route
