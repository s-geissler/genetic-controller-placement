import random
from operator import add
from collections import defaultdict
import numpy
import sys

class Genetics:

    def __init__(self, p_size, i_size, retain, mutate, random_select):
        self.p_size = p_size
        self.i_size = i_size
        self.retain = retain
        self.mutate = mutate
        self.random_select = random_select
        self.optimum = []
        self.optimum_value = sys.maxint

    def individual(self, nodes):
        """
        Create a single individual
        count: the number of selected vertices
        nodes: a list of vertices
        """
        return random.sample(xrange(int(min(nodes)), int(max(nodes))+1), self.i_size)
    
    def population(self, nodes):
        """
        Create a number of individuals (i.e. a population).
        
        nodes: a list of vertices
        """
        return [self.individual(nodes) for x in xrange(self.p_size)]
    
    def fitness(self, individual, matrix):
        """
        Determine the fitness of an individual. Higher is better.
        
        individual: the individual to evaluate
        """
        fitness = defaultdict(set)
        for v in individual:

            for k in matrix[v].keys():
                if fitness[k] > matrix[v][k]:
                    fitness[k] = matrix[v][k]
        mean = numpy.mean(fitness.values())
        if (mean < self.optimum_value):
            self.optimum = individual
            self.optimum_value = mean
        return mean

    def grade(self, pop, matrix):
        'Find average fitness for a population.'
        sum = 0
        sum = reduce(add, (self.fitness(p, matrix) for p in pop))
        return sum / len(pop)
    
    def evolve(self, pop, matrix, nodes):
        graded = [ (self.fitness(p, matrix), p) for p in pop]
        graded = [ p[1] for p in sorted(graded)]
        retain_length = int(len(graded)*self.retain)
        parents = graded[:retain_length]
        # randomly add other individuals to
        # promote genetic diversity
        for individual in graded[retain_length:]:
            if self.random_select > random.random():
                parents.append(individual)
        # mutate some individuals
        for individual in parents:
            if self.mutate > random.random():
                pos_to_mutate = random.randint(0, len(individual)-1)
                individual[pos_to_mutate] = random.randint(
                    min(matrix.keys()), max(matrix.keys()))
        # crossover parents to create children
        parents_length = len(parents)
        desired_length = self.p_size - parents_length
        children = []
        while len(children) < desired_length:
            male = random.randint(0, parents_length-1)
            female = random.randint(0, parents_length-1)
            if male != female:
                male = parents[male]
                female = parents[female]
                half = len(male) / 2
                child = male[:half] + female[half:]
                if len(list(set(child))) == self.i_size:
                    children.append(child)        
        parents.extend(children)

        # Eliminate duplicates
#        parents = [list(x) for x in set(tuple(x) for x in parents)]

        return parents
            
