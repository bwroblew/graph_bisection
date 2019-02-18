from Graph import *
import random

class Partitioning(object):

    def __init__(self, graph, sizes=None):
        if sizes is None:
            sizes = [50, 50]
        assert len(sizes) >= 2, "Partitions number must be greater or equal 2"
        assert sum(sizes) == 100, "Partitions sizes don't sum to 100"
        self.__graph = graph
        self.__sizes = sizes
        self.__n = len(sizes)
        self.__clear_partitions()

    def __clear_partitions(self):
        self.__partitions = []
        for _ in range(self.__n):
            self.__partitions.append(set())

    def __get_vertices_numbers(self):
        """
        Method calculates number of vertices in each partitions.
        :return: List of numbers of vertices
        """
        vertices = self.__graph.get_n()
        v_sizes = [round(x / 100 * vertices) for x in self.__sizes]
        v_sizes[-1] = vertices - sum(v_sizes[:-1])
        return v_sizes

    def random_partitions(self):
        self.__clear_partitions()
        v_sizes = self.__get_vertices_numbers()
        vertices = set(self.__graph.get_vertices())
        for part_index in range(self.__n):
            for _ in range(v_sizes[part_index]):
                self.__partitions[part_index].add(random.sample(vertices, 1).pop())

