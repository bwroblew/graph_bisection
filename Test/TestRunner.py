from SpecificSizePerformanceTest import SpecificSizePerformanceTest
from SpecificSizeQualityTest import SpecificSizeQualityTest
from Partitioning import *


class TestRunner:
    def __init__(self):
        self.tests = [SpecificSizeQualityTest(30, bisection_methods=[Partitioning.sga, Partitioning.kla,
                                                                     Partitioning.rbha],
                                              graphs_number=100)
                      ]

    def run(self):
        for test in self.tests:
            test.run()


if __name__ == "__main__":
    TestRunner().run()
