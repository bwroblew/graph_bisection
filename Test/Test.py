from abc import ABC, abstractmethod


class Test(ABC):

    def __init__(self):
        self.results = {}

    @abstractmethod
    def set_up(self):
        pass

    @abstractmethod
    def tear_down(self):
        pass

    def run(self):
        self.results = {}
        tests = [func for func in dir(self) if callable(getattr(self, func)) and func.startswith("test")]
        for test in tests:
            failed = False
            try:
                test_method = getattr(self, test)
                self.set_up()
                test_method()
            except Exception as e:
                failed = True
                self.results[test.__name__] = str(e)
            finally:
                self.tear_down()
                if not failed:
                    self.results[test] = "PASSED"
                self.print_results()

    def print_results(self):
        print("\n============================")
        print("Test results:")
        for test in self.results.keys():
            print("Test {} -> {}".format(test, self.results[test]))
        print("============================")

    def fail(self, msg=""):
        raise Exception("-E- Test failed: {}".format(msg))

    def assert_true(self, condition, msg):
        if not condition:
            self.fail(msg)
