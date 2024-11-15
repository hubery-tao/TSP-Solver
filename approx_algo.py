"""
2-Approximation using MST

"""

import heapq

def solve(graph_mat):
    num_nodes = len(graph_mat)
    tree = [[] for i in range(num_nodes)]     # adjacency list
    pq = []
    for i in range(1, num_nodes):
        heapq.heappush(pq, (graph_mat[0,i], 0, i))
    visited = [False] * num_nodes
    visited[0] = True
    num_visited = 1
    
    while num_visited < num_nodes:
        weight, prev, curr = heapq.heappop(pq)
        if not visited[curr]:
            tree[prev].append(curr)
            tree[curr].append(prev)
            visited[curr] = True
            num_visited += 1
            for neigh in range(num_nodes):
                if not visited[neigh]:
                    heapq.heappush(pq, (graph_mat[curr,neigh], curr, neigh))
                
    # starting from any node in the MST, 
    # the depth-first serach will give a 2-approximation
    # so pick the one with the minimum cost
    min_cost = float("inf")
    best_route = None
    for root in range(num_nodes):
        route = []
        visited = [False] * num_nodes
        stack = [root]
        while stack:
            curr = stack.pop()
            route.append(curr)
            visited[curr] = True
            for neigh in tree[curr]:
                if not visited[neigh]:
                    stack.append(neigh)
        cost = 0
        for i in range(num_nodes-1):
            cost += graph_mat[route[i], route[i+1]]
            if cost >= min_cost:
                break
        else:
            if cost < min_cost:
                min_cost = cost
                best_route = tuple(route)
    
    return min_cost, best_route
            
        
    
    
    