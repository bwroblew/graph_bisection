import random


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
        for vp in partition:
            if self.__graph.is_connected(vertex, vp):
                cost += 1
        return cost

    def __calculate_sxy(self, v1, v2, p1, p2):
        """
        Method calculates S(x, y) defined in https://www.informatik.uni-kiel.de/~gej/publ/bisection.pdf
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
        Simple greedy algorithm described in https://www.informatik.uni-kiel.de/~gej/publ/bisection.pdf
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

    def kla(self):
        """
        Kernighan-Lin Algorithm described in paper.
        Bisection only
        """
        assert self.__n == 2, "This algorithm is implemented only for bisection"
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
        Randomized-Black-Holes Algorithm
        """
        x_set, y_set = set(), set()
        sets = [x_set, y_set]
        v_sizes = self.__get_vertices_numbers()
        while len(x_set) < v_sizes[0] or len(y_set) < v_sizes[1]:
            # set X
            for current_set in sets:
                # in case of non-equal partition sizes
                if len(current_set) == v_sizes[sets.index(current_set)]:
                    continue
                edges = []
                vertex = None
                for x in current_set:
                    nbs = self.__graph.get_neighbours(x)
                    for nb in nbs:
                        if nb not in x_set and nb not in y_set:
                            edges.append((x, nb))
                if len(edges) > 0:
                    vertex = random.choice(edges)[1]
                else:
                    vertices = [v for v in self.__graph.get_vertices() if v not in x_set and v not in y_set]
                    if len(vertices) == 0:
                        # this partition is full
                        break
                    vertex = random.choice(vertices)
                current_set.add(vertex)
        self.__partitions[0] = set(x_set)
        self.__partitions[1] = set(y_set)


