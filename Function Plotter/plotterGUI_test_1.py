import PlotterGui
import pytest
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

@pytest.fixture

def app(qtbot):

    test_plotter_app=PlotterGui.PlotterGUI()
    qtbot.addWidget(test_plotter_app)

    return test_plotter_app



def test_function_in(app):
   
    app.function_in.setText("x^")
   
    assert app.wrongFn==True
    
def test_min_max_in(app):
    
    app.min_in.setText("1")
    app.max_in.setText("10")
   
    
    assert app.wrongMinMax==False


