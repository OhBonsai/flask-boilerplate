import pytest


class MyPlugin(object):
    def pytest_sessionfinish(self):
        print("*** test run reporting finishing")

pytest.main(['-s', '-v', 'tests'], plugins=[MyPlugin()])