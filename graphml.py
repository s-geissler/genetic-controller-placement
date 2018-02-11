import networkx as nx
import pygraphml as gml
from graph import *

def read_graphml(file):

    parser = gml.GraphMLParser()

    g = parser.parse(file)
    edges = g.edges()

    wg = Graph()
    for e in edges:
        # Creation of a new graph with constant edge weight 1
        wg.add_edge(e.node1.id, e.node2.id, 1)

    return wg
        

    
