"""
a heuristic algorithm with no guarantees, but that is effective in practice.
"""

import numpy as np
import pandas as pd
import random
import math
import time
import os

def dist(route, graph_mat):
    res=0
    for i in range(len(route)):
        res+=graph_mat[route[i], route[(i+1)%len(route)]]
    return res

def swap(route):
    res=route.copy()
    i, j=random.sample(range(len(route)), 2)
    res[i], res[j]=res[j], res[i]
    return res

def solver(graph_mat, cutoff_time, rand_seed):
    
    k=1.5
    M=1000
    ini_temp=10000
    cooling_rate=0.99
    max_iter=1000000
    
    if rand_seed is not None:
        random.seed(rand_seed)
        np.random.seed(rand_seed)
        
    res_route=list(range(len(graph_mat)))
    random.shuffle(res_route)
    res_dist=dist(res_route, graph_mat)
    
    temp=ini_temp
    
    start=time.time()
    
    for iteration in range(max_iter):
        elapsed=time.time()-start
        if elapsed>cutoff_time:
            #print(f"Stopping early after {elapsed:.2f} seconds.")
            break
        
        temp_route=swap(res_route)
        temp_dist=dist(temp_route, graph_mat)
        
        if temp_dist<=res_dist:
            #print("temp_dist: "+str(temp_dist)+"< res_dist: "+str(res_dist))
            res_route=temp_route
            res_dist=temp_dist
        else:
            deltaE=temp_dist-res_dist
            p=np.exp(-deltaE/(k*temp))
            if random.random()<p:
                res_route=temp_route
                res_dist=temp_dist
        if(iteration%M==0):
            temp=temp*cooling_rate
    #print('Route: '+str(res_route)+', Distance: '+str(res_dist))
    return res_dist, res_route
