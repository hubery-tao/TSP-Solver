"""
This main source file reads the command line arguments, 
converts the input file into an adjacency matrix, and 
invokes the appropriate functions from other modules to solve TSP.

The dataset files are expected to be located in the working directory.
Output files are also generated in the working directory.
"""

import argparse
import sys
import numpy as np

import brute_force
import approx_algo
import local_search

# create parser and parse the command line arguments
parser = argparse.ArgumentParser(description="a TSP solver")
parser.add_argument("-inst", type=str, required=True,
                    help="The filename of a dataset")
parser.add_argument("-alg", type=str, required=True, choices=["BF","Approx","LS"],
                    help="Method to use: BF, Approx, or LS")
parser.add_argument("-time", type=str, required=False,
                    help="The cut-off time (in seconds)")
parser.add_argument("-seed", type=int, required=False,
                    help="A random seed (optional, only needed for LS)")
args = parser.parse_args()


# handle the command line arguments
instance = args.inst
if instance.endswith(".tsp"):
    instance = instance[:-4]
input_file = instance + ".tsp"

solver_type = args.alg

cutoff_time = float("inf")
if solver_type == "BF" or solver_type == "LS":
    if args.time == None:
        print(f"Missing cut-off time for algorithm {solver_type}", file=sys.stderr)
        exit(1)
    cutoff_time = float(args.time)

if solver_type == "LS":
    if args.seed == None:
        print(f"Missing random seed for algorithm {solver_type}", file=sys.stderr)
        exit(1)
rand_seed = args.seed


# read the file to generate a list of locations
loc_ls = []
with open(input_file, "r") as file:
    line = file.readline()
    while not line.startswith("NODE_COORD_SECTION"):
        line = file.readline()
    
    line = file.readline()
    while not line.startswith("EOF"):
        elems = line.split()
        loc = [elems[0], float(elems[1]), float(elems[2])]
        loc_ls.append(loc)
        line = file.readline()


# scan the location list to genrate an adjacency matrix
num_nodes = len(loc_ls)
graph_mat = np.zeros((num_nodes, num_nodes))
for i in range(num_nodes):
    for j in range(i+1, num_nodes):
        n1, x1, y1 = loc_ls[i]
        n2, x2, y2 = loc_ls[j]
        dist = np.sqrt((x1-x2)**2+(y1-y2)**2)
        int_dist = round(dist)
        graph_mat[i, j] = int_dist
        graph_mat[j, i] = int_dist


# call the corresponding solver and get output filename
if solver_type == "BF":
    cost, route = brute_force.solve(graph_mat, cutoff_time)
    output_file = f"{instance}_{solver_type}_{args.time}.sol"
    
elif solver_type == "Approx":
    cost, route = approx_algo.solve(graph_mat)
    output_file = f"{instance}_{solver_type}.sol"
    
elif solver_type == "LS":
    cost, route = local_search.solve(graph_mat, cutoff_time, rand_seed)
    output_file = f"{instance}_{solver_type}_{args.time}_{rand_seed}.sol"

# convert indices in route to node ids in the input file
route = [loc_ls[i][0] for i in route]
if route[0] != route[-1]:
    route.append(route[0])

# write the output file in the working directory
with open(output_file, "w") as file:
    file.write(f"{cost}\n")
    file.write(",".join(route))
