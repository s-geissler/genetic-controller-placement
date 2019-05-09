from collections import defaultdict

class Graph(object):
    def __init__(self, nodes=[]):
        self.nodes = set()
        self.neighbours = defaultdict(set)
        self.dist = {}

    def add_node(self, *nodes):
        [self.nodes.add(n) for n in nodes]

    def add_edge(self, frm, to, d=1e309):
        self.add_node(frm, to)
        self.neighbours[frm].add(to)
        self.neighbours[to].add(frm)
        self.dist[ frm, to ] = d
        self.dist[ to, frm ] = d

    def dijkstra(self, start, maxD=1e309):
        tdist = defaultdict(set)
        tdist[start] = 0
        preceding_node = {}
        unvisited = self.nodes.copy()

        while unvisited:
            current = unvisited.intersection(tdist.keys())
            if not current: break
            min_node = min(current, key=tdist.get)
            unvisited.remove(min_node)

            for neighbour in self.neighbours[min_node]:
                d = tdist[min_node] + self.dist[min_node, neighbour]
                if tdist[neighbour] > d and maxD >= d:
                    tdist[neighbour] = d
                    preceding_node[neighbour] = min_node

        return tdist, preceding_node

    def min_path(self, start, end, maxD=1e309):
        tdist, preceding_node = self.dijkstra(start, maxD)
        dist = tdist[end]
        backpath = [end]
        try:
            while end != start:
                end = preceding_node[end]
                backpath.append(end)
            path = list(reversed(backpath))
        except KeyError:
            path = None

        return dist, path

    def get_nodes(self):
        return list(self.nodes)

    def get_adjacency_matrix(self):
        adj_matrix = defaultdict(set)
        for n in self.nodes:
            distances, _ = self.dijkstra(n)
            adj_matrix[int(n)] = distances
        return adj_matrix

