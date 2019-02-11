import random
from Graph import Graph


class GraphGenerator(object):

    @classmethod
    def __generate_random_spanning_tree(cls, graph):
        """
        http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.47.8598&rep=rep1&type=pdf
        :return:
        """
        vertices = graph.get_vertices()
        to_discover, discovered = set(vertices), set()
        current_vertex = random.sample(to_discover, 1).pop()
        to_discover.remove(current_vertex)
        discovered.add(current_vertex)
        while to_discover:
            neighbour_vertex = random.sample(vertices, 1).pop()
            if neighbour_vertex not in discovered:
                graph.add_edge(current_vertex, neighbour_vertex)
                to_discover.remove(neighbour_vertex)
                discovered.add(neighbour_vertex)
            current_vertex = neighbour_vertex

    @classmethod
    def __generate_edges(cls, graph, n):
        vertices = graph.get_vertices()
        for _ in range(n):
            v1 = random.choice(vertices)
            v2 = random.choice(graph.get_not_neighbours(v1))
            while v2 is v1:
                v1 = random.choice(vertices)
                v2 = random.choice(graph.get_not_neighbours(v1))
            graph.add_edge(v1, v2)

    @classmethod
    def generate(cls, n, m=None, connected=True):
        if m is None:
            m = random.randint(n-1, n*(n-1)/2)
        graph = Graph(n)
        if connected:
            cls.__generate_random_spanning_tree(graph)
        else:
            cls.__generate_edges(graph, n-1)
        edges_remaining = m - (n - 1)
        cls.__generate_edges(graph, edges_remaining)
        return graph


