#!/usr/bin/python

from graph import *
from genetics import *
from graphml import read_graphml
import matplotlib.pyplot as plot
import numpy as np
import plotly.plotly as py

def main():

    # Read the graph and generate a adjacency matrix
    g = read_graphml("data/Intellifiber.graphml")
    matrix = g.get_adjacency_matrix()

    """
    Initialize the genetics module with parameters
    1: Number of individuals in a population
    2: Number of elements in one individual
    3: Percentage of parents to retain
    4: Mutation rate
    5: Random selection rate
    """
    gen = Genetics(100, 3, 0.1, 0.05, 0.01)

    # Generate initial population based on available graph vertices
    p = gen.population(g.get_nodes())

    generation_history = []

    # Evolve
    for i in xrange(1000):
        p = gen.evolve(p, matrix, g.get_nodes())
        grade = gen.grade(p, matrix)
        print("Generation (" + str(i) + ") ==> " +str(grade))
        generation_history.append(grade)
    # Print best individual across all generations
    print(str(gen.optimum) + " with a value of " + str(gen.optimum_value))

    # Plot grade over generation
    x = range(0,len(generation_history))
    plot.plot(x, generation_history, linewidth=2)
    plot.xlabel("Generation")
    plot.ylabel("Average Fitness")
    plot.grid(True)
    plot.savefig("Result.png")
    plot.show()
    

    
if __name__ == "__main__": main()
