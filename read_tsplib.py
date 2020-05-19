import matplotlib.pyplot as plt
from pprint import pprint
import tsplib95
import networkx as nx
from networkx.drawing.nx_pydot import write_dot
problem = tsplib95.load("tsplib/gr17.tsp")
G = problem.get_graph()

print(G.edges[0,2])