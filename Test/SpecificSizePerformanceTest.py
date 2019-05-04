from GraphLib.GraphGenerator import *
from Partitioning import *
from Test import Test
from statistics import mean, stdev

import time

DEFAULT_GRAPHS_NUMBER = 100


class SpecificSizePerformanceTest(Test):

    def __init__(self, size_n=10, bisection_methods=None, graphs_number=DEFAULT_GRAPHS_NUMBER):
        if bisection_methods is None:
            self.fail("No bisection methods provided")
        self.bisection_methods = bisection_methods
        self.size_n = size_n
        self.graphs_number = graphs_number
        self.time_results = {}
        for method in self.bisection_methods:
            self.time_results[method.__name__] = []
        self.graphs = None

    def set_up(self):
        self.graphs = []
        for _ in range(self.graphs_number):
            self.graphs.append(GraphGenerator.generate(self.size_n))

    def tear_down(self):
        print("\n============================")
        for test in self.time_results.keys():
            print("\nFUNCTION {}".format(test))
            print("Average:\t{}".format(mean(self.time_results[test])))
            print("Std dev:\t{}".format(stdev(self.time_results[test])))
            print("Min:\t{}".format(min(self.time_results[test])))
            print("Max:\t{}".format(max(self.time_results[test])))
        print("============================")

    def test_basic_performance(self):
        for method in self.bisection_methods:
            for graph in self.graphs:
                bis = Partitioning(graph)
                before = time.time()
                getattr(bis, method.__name__)()
                after = time.time()
                self.time_results[method.__name__].append(after-before)
