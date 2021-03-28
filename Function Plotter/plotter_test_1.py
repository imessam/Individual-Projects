import Plotter
import pytest

@pytest.fixture
def app(qtbot):

    test_plotter=Plotter.Plotter()

    return test_plotter



def test_function_in(app):
   
    Y=app(function = "x", minX = 1, maxX = 2, canvas = None)
   
    assert Y==[1,2]



