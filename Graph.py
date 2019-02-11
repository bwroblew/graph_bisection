NOT_CONNECTED = 0
CONNECTED = 1


class Vertex(object):
    def __init__(self, prop):
        self.prop = prop


class Graph(object):

    def __init__(self, n):
        self.__n = n
        self.__matrix = [[NOT_CONNECTED for _ in range(n)] for _ in range(n)]
        self.__vertices = [Vertex(-1) for _ in range(n)]

    def add_vertex(self, v):
        self.__n += 1
        self.__vertices.append(v)
        for row in self.__matrix:
            row.append(NOT_CONNECTED)
        self.__matrix.append([NOT_CONNECTED for _ in range(self.__n)])
        return self.__n

    def add_edge(self, v1, v2):
        index_v1 = self.__vertices.index(v1)
        index_v2 = self.__vertices.index(v2)
        self.__matrix[index_v1][index_v2] = CONNECTED
        self.__matrix[index_v2][index_v1] = CONNECTED

    def get_degree(self, v):
        index = self.__vertices.index(v)
        degree = sum(self.__matrix[index])
        return degree

    def get_neighbours(self, v):
        index = self.__vertices.index(v)
        neighbours = [vertex for vertex in self.__vertices
                      if self.__matrix[index][self.__vertices.index(vertex)] == CONNECTED]
        return neighbours

    