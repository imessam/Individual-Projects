import Plotter
import pytest

@pytest.fixture
def app(qtbot):

    test_plotter=Plotter.Plotter()

    return test_plotter



def test_function_in(app):
   
    Y=app(function = "x^2+x/x", minX = 1, maxX = 2, canvas = None) # function is : (x^2+x)/x => x+1
   
    assert Y==[2,3]



