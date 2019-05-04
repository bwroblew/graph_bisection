from GraphLib.GraphGenerator import *
from Partitioning import *
from Test import Test
from statistics import mean, stdev

DEFAULT_GRAPHS_NUMBER = 100


class SpecificSizeQualityTest(Test):

    def __init__(self, size_n=10, bisection_methods=None, graphs_number=DEFAULT_GRAPHS_NUMBER):
        if bisection_methods is None:
            self.fail("No bisection methods provided")
        self.bisection_methods = bisection_methods
        self.size_n = size_n
        self.graphs_number = graphs_number
        self.costs_results = {}
        for method in self.bisection_methods:
            self.costs_results[method.__name__] = []
        self.graphs = None

        self.graphs_edges = None

    def set_up(self):
        self.graphs = []
        for _ in range(self.graphs_number):
            self.graphs.append(GraphGenerator.generate(self.size_n))
        self.graphs_edges = []
        for graph in self.graphs:
            self.graphs_edges.append(graph.get_m())

    def tear_down(self):
        print("\n============================")
        for test in self.costs_results.keys():
            print("\nFUNCTION {}".format(test))
            print("Average:\t{}\tall:\t{}".format(mean(self.costs_results[test]), mean(self.graphs_edges)))
            print("Std dev:\t{}".format(stdev(self.costs_results[test])))
        print("============================")

    def test_basic_performance(self):
        for method in self.bisection_methods:
            for graph in self.graphs:
                bis = Partitioning(graph)
                getattr(bis, method.__name__)()
                cost = bis.calc_cost()
                self.costs_results[method.__name__].append(cost)
