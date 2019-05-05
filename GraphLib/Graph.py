NOT_CONNECTED = 0
CONNECTED = 1


class Vertex(object):
    def __init__(self, prop):
        self.prop = prop


class Graph(object):

    def __init__(self, n):
        self.__n = n
        self.__m = 0
        self.__matrix = [[NOT_CONNECTED for _ in range(n)] for _ in range(n)]
        self.__vertices = [Vertex(-1) for _ in range(n)]

    def __str__(self):
        txt = "Graph with {} vertices\nAnd {} edges\n".format(self.__n, self.__m)
        for row in self.__matrix:
            for cell in row:
                txt += str(cell)
            txt += "\n"
        return txt

    def get_subgraph(self, vertex_set):
        subgraph = Graph(0)
        for vertex in vertex_set:
            subgraph.add_vertex(vertex)
        for vertex in vertex_set:
            for neigh in self.get_neighbours(vertex):
                if neigh in vertex_set and not subgraph.is_connected(vertex, neigh):
                    subgraph.add_edge(vertex, neigh)
        return subgraph

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
        assert self.__matrix[index_v1][index_v2] == NOT_CONNECTED, "Edge exists!"
        self.__m += 1
        self.__matrix[index_v1][index_v2] = CONNECTED
        self.__matrix[index_v2][index_v1] = CONNECTED

    def get_vertices(self):
        return self.__vertices

    def is_connected(self, v1, v2):
        """
        Method checks if there is an edge connecting v1 and v2.
        Returns false if v1 and v2 are the same vertex.
        :param v1:
        :param v2:
        :return:
        """
        index_v1 = self.__vertices.index(v1)
        index_v2 = self.__vertices.index(v2)
        return True if self.__matrix[index_v1][index_v2] == 1 else False

    def get_degree(self, v):
        index = self.__vertices.index(v)
        degree = sum(self.__matrix[index])
        return degree

    def get_neighbours(self, v):
        index = self.__vertices.index(v)
        neighbours = [vertex for vertex in self.__vertices
                      if self.__matrix[index][self.__vertices.index(vertex)] == CONNECTED]
        return neighbours

    def get_not_neighbours(self, v):
        index = self.__vertices.index(v)
        not_neighbours = [vertex for vertex in self.__vertices
                          if self.__matrix[index][self.__vertices.index(vertex)] == NOT_CONNECTED]
        return not_neighbours

    def get_n(self):
        return self.__n

    def get_m(self):
        return self.__m

    def get_vertex_index(self, v):
        return self.__vertices.index(v)

    def get_complement(self):
        rev = Graph(0)
        for vertex in self.__vertices:
            rev.add_vertex(vertex)
        rev.__m = self.__n * (self.__n - 1) / 2 - self.__m
        for i in range(len(self.__matrix)):
            for j in range(len(self.__matrix[i])):
                if self.__matrix[i][j] == NOT_CONNECTED:
                    rev.__matrix[i][j] = CONNECTED
                else:
                    rev.__matrix[i][j] = NOT_CONNECTED
        return rev

