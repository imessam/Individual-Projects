import Plotter
import pytest

@pytest.fixture
def app(qtbot):

    test_plotter=Plotter.Plotter()

    return test_plotter



def test_function_in(app):
   
    Y=app(function = "1*x+2*x^2/3*x^3", minX = 1, maxX = 2, canvas = None) # function is : (x+2x^2)/(3x^3) => (1+2x)/(3x^2)
   
    assert Y==[1,(5/12)]



