import random
import math


class Partitioning(object):

    def __init__(self, graph, sizes=None):
        if sizes is None:
            sizes = [50, 50]
        assert len(sizes) >= 2, "Number of partitions must be greater or equal 2"
        assert sum(sizes) == 100, "Partitions sizes don't sum to 100"
        self.__graph = graph
        self.__sizes = sizes
        self.__n = len(sizes)
        self.__clear_partitions()

    def __str__(self):
        txt = ""
        for partition in self.__partitions:
            txt += "Partition {}: ".format(self.__partitions.index(partition))
            for vertex in partition:
                txt += "{} ".format(self.__graph.get_vertex_index(vertex))
            txt += "\n"
        cost = self.calc_cost()
        txt += "Cost: {}\n".format(cost)
        return txt

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

    def calc_cost(self):
        """
        Method calculates number of edges between partitions.
        :return:
        """
        # cost is number of edges inside partitions
        cost = 0
        for partition in self.__partitions:
            assert len(partition) >= self.__graph.get_n() / 2 - 1, "Partition too small"
            assert self.__graph.get_n() / 2 + 1 >= len(partition), "Partition too big"
            for v1 in partition:
                for v2 in partition:
                    if self.__graph.is_connected(v1, v2):
                        cost += 1
        # dividing cost by 2 as we counted each edge twice
        assert cost % 2 == 0, "Cost should be an even number!"
        cost /= 2
        # return number of edges between partitions
        return self.__graph.get_m() - cost

    def __swap_vertices(self, v1, v2, p1, p2):
        """
        Method swaps v1 and v2 between their partitions.
        :param v1:
        :param v2:
        :param p1:
        :param p2:
        :return:
        """
        assert v1 in p1 and v2 in p2, "Vertices not inside correct partitions"
        p1.remove(v1)
        p2.remove(v2)
        p1.add(v2)
        p2.add(v1)

    def random_partitions(self):
        self.__clear_partitions()
        v_sizes = self.__get_vertices_numbers()
        vertices = set(self.__graph.get_vertices())
        for part_index in range(self.__n):
            for _ in range(v_sizes[part_index]):
                vertex = random.sample(vertices, 1).pop()
                self.__partitions[part_index].add(vertex)
                vertices.remove(vertex)

    def __get_vertex_cost(self, vertex, partition):
        """
        Method calculates number of edges connecting vertex with partition's vertices.
        If vertex in partition returns inner cost, else outer cost.
        :param vertex:
        :param partition:
        :return:
        """
        assert len(partition) > 0, "Partition is empty"
        cost = 0
        for nb in self.__graph.get_neighbours(vertex):
            if nb in partition:
                cost += 1
        return cost

    def __calculate_sxy(self, v1, v2, p1, p2):
        """
        Method calculates S(x, y) defined in http://snovit.math.umu.se/~gerold/publ/bisection.pdf
        :param v1:
        :param v2:
        :param p1:
        :param p2:
        :return:
        """
        assert (v1 in p1) and (v2 in p2), "Vertices not inside correct partitions"
        # outer costs
        ov1 = self.__get_vertex_cost(v1, p2)
        ov2 = self.__get_vertex_cost(v2, p1)
        # inner costs
        iv1 = self.__get_vertex_cost(v1, p1)
        iv2 = self.__get_vertex_cost(v2, p2)
        # omega = is connected
        omega = 1 if self.__graph.is_connected(v1, v2) else 0
        sxy = ov1 - iv1 + ov2 - iv2 - 2*omega
        return sxy

    def sga(self):
        """
        MIN-BISECTION
        Simple greedy algorithm described in http://snovit.math.umu.se/~gerold/publ/bisection.pdf
        For now implemented for BISECTION only.
        """
        assert self.__n == 2, "This algorithm is implemented only for bisection"
        self.random_partitions()
        # is improvement possible
        impr_poss = True
        while impr_poss:
            impr_poss = False
            for v1 in self.__partitions[0]:
                for v2 in self.__partitions[1]:
                    if self.__calculate_sxy(v1, v2, self.__partitions[0], self.__partitions[1]) > 0:
                        self.__swap_vertices(v1, v2, self.__partitions[0], self.__partitions[1])
                        impr_poss = True
                        break
                # breaking two loops as partitions are changed and we cannot swap more during these iterations
                else:
                    continue
                break

    def kla(self, random=True):
        """
        MIN-BISECTION
        Kernighan-Lin Algorithm described in paper.
        Bisection only
        """
        assert self.__n == 2, "This algorithm is implemented only for bisection"
        if random:
            self.random_partitions()
        best_x, best_y = set(self.__partitions[0]), set(self.__partitions[1])
        best_cost = self.calc_cost()
        improved = True
        while improved:
            improved = False
            x_prim = set(self.__partitions[0])
            y_prim = set(self.__partitions[1])
            while x_prim and y_prim:
                # get first items from x and from y
                for x_elem in x_prim: break
                for y_elem in y_prim: break
                # calculate max sxy based on partitions, not x and y sets
                max_value = self.__calculate_sxy(x_elem, y_elem, self.__partitions[0], self.__partitions[1])
                for v1 in x_prim:
                    for v2 in y_prim:
                        val = self.__calculate_sxy(v1, v2, self.__partitions[0], self.__partitions[1])
                        if val > max_value:
                            max_value = val
                            x_elem = v1
                            y_elem = v2
                self.__swap_vertices(x_elem, y_elem, self.__partitions[0], self.__partitions[1])
                new_cost = self.calc_cost()
                if new_cost < best_cost:
                    best_x, best_y = set(self.__partitions[0]), set(self.__partitions[1])
                    best_cost = new_cost
                    improved = True
                x_prim.remove(x_elem)
                y_prim.remove(y_elem)
            self.__partitions[0], self.__partitions[1] = set(best_x), set(best_y)

    def rbha(self):
        """
        MIN-BISECTION
        Randomized-Black-Holes Algorithm
        """
        x_set, y_set = set(), set()
        sets = [x_set, y_set]
        v_sizes = self.__get_vertices_numbers()
        while len(x_set) < v_sizes[0] or len(y_set) < v_sizes[1]:
            # set X
            for current_set in sets:
                # in case of not equal partition sizes
                if len(current_set) == v_sizes[sets.index(current_set)]:
                    continue
                edges = []
                for x in current_set:
                    nbs = self.__graph.get_neighbours(x)
                    for nb in nbs:
                        if nb not in x_set and nb not in y_set:
                            edges.append((x, nb))
                if len(edges) > 0:
                    vertex = random.choice(edges)[1]
                else:
                    vertices = [v for v in self.__graph.get_vertices() if v not in x_set and v not in y_set]
                    # this partition is full
                    if len(vertices) == 0:
                        break
                    vertex = random.choice(vertices)
                current_set.add(vertex)
        self.__partitions[0] = set(x_set)
        self.__partitions[1] = set(y_set)

    def bfs_partitions(self):
        """
        MAX-BISECTION
        Assigning vertices to partitions based on BFS algorithm.
        MAX BIS
        :return:
        """
        self.__clear_partitions()
        vertices = set(self.__graph.get_vertices())
        root = random.sample(vertices, 1).pop()
        print(self.__graph.get_vertices().index(root))
        vertices.remove(root)
        queue = [(root, 0)]
        while queue:
            (u, p) = queue.pop(0)
            self.__partitions[p].add(u)
            for nb in self.__graph.get_neighbours(u):
                if nb in vertices:
                    queue.append((nb, int(not p)))
                    vertices.remove(nb)

    def lpa_vertex_cost(self, v1, v2, p0, p1, p2, p3):
        ov2p1 = self.__get_vertex_cost(v2, p1)
        ov1p0 = self.__get_vertex_cost(v1, p0)
        iv2p3 = self.__get_vertex_cost(v2, p3)
        iv1p2 = self.__get_vertex_cost(v1, p2)
        omega = 1 if self.__graph.is_connected(v1, v2) else 0
        sxy = ov2p1 + ov1p0 - iv2p3 - iv1p2 - omega
        # maybe 2* omega
        return sxy

    def lpa_calc_cost(self, bis, supgraph):
        cost = 0
        partitions = [self.__partitions[0].union(bis.__partitions[1]), self.__partitions[1].union(bis.__partitions[0])]
        for partition in partitions:
            assert len(partition) > self.__n / 2 - 1, "Partition too small"
            for v1 in partition:
                for v2 in partition:
                    if supgraph.is_connected(v1, v2):
                        cost += 1
        # dividing cost by 2 as we counted each edge twice
        assert cost % 2 == 0, "Cost should be an even number!"
        cost /= 2
        # return number of edges between partitions
        return supgraph.get_m() - cost

    def find_best_lpa(self, bis, supgraph):
        self.random_partitions()
        best_x, best_y = set(self.__partitions[0]), set(self.__partitions[1])
        best_cost = self.lpa_calc_cost(bis, supgraph)
        improved = True
        while improved:
            improved = False
            x_prim = set(self.__partitions[0])
            y_prim = set(self.__partitions[1])
            while x_prim and y_prim:
                # get first items from x and from y
                for x_elem in x_prim: break
                for y_elem in y_prim: break
                # calculate max sxy based on partitions, not x and y sets
                max_value = self.lpa_vertex_cost(x_elem, y_elem, bis.__partitions[0], bis.__partitions[1], self.__partitions[0], self.__partitions[1])
                for v1 in x_prim:
                    for v2 in y_prim:
                        val = self.lpa_vertex_cost(x_elem, y_elem, bis.__partitions[0], bis.__partitions[1], self.__partitions[0], self.__partitions[1])
                        if val > max_value:
                            max_value = val
                            x_elem = v1
                            y_elem = v2
                self.__swap_vertices(x_elem, y_elem, self.__partitions[0], self.__partitions[1])
                new_cost = self.lpa_calc_cost(bis, supgraph)
                if new_cost < best_cost:
                    best_x, best_y = set(self.__partitions[0]), set(self.__partitions[1])
                    best_cost = new_cost
                    improved = True
                x_prim.remove(x_elem)
                y_prim.remove(y_elem)
            self.__partitions[0], self.__partitions[1] = set(best_x), set(best_y)

    def lpa(self):
        """
        Logaritmical Partitioning Algorithm
        :return:
        """
        assert self.__n == 2, "This algorithm is implemented only for bisection"
        if self.__graph.get_n() == 2:
            vertices = self.__graph.get_vertices()
            self.__partitions[0] = set()
            self.__partitions[0].add(vertices[0])
            self.__partitions[1] = set()
            self.__partitions[1].add(vertices[1])
            return
        self.kla()
        s1 = self.__graph.get_subgraph(self.__partitions[0])
        s2 = self.__graph.get_subgraph(self.__partitions[1])

        bis1 = Partitioning(s1)
        bis2 = Partitioning(s2)
        bis1.lpa()
        #bis1.kla()
        bis2.find_best_lpa(bis1, self.__graph)

        self.__partitions[0] = bis1.__partitions[0].union(bis2.__partitions[1])
        self.__partitions[1] = bis1.__partitions[1].union(bis2.__partitions[0])
        self.kla(False)

    def ikla(self):
        self.kla()
        best0 = self.__partitions[0]
        best1 = self.__partitions[1]
        best_cost = self.calc_cost()
        for _ in range(100):
            self.__clear_partitions()
            self.kla()
            cost = self.calc_cost()
            if cost < best_cost:
                best_cost = cost
                best0 = self.__partitions[0]
                best1 = self.__partitions[1]
        self.__partitions[0] = best0
        self.__partitions[1] = best1
