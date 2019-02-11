class Vertex(object):
    def __init__(self, prop):
        self.prop = prop


class Graph(object):
    def __init__(self, n):
        self.matrix = [[0 for _ in range(n)] for _ in range(n)]
