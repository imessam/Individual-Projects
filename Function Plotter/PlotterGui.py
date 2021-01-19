import sys
from Plotter import Plotter

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure



class PlotterGUI(QWidget):
    
    ''' 
    Plotter Gui for plotting functions for a given range of input.
    
    '''
 
    def __init__(self):
        
        
        QWidget.__init__(self)
        self.setWindowTitle('Plotter GUI')
        self.setMinimumWidth(400)
 
        self.init_labels()
        self.init_validator()
        self.init_fields()
        self.init_canvas()
        self.init_btn()
        self.init_layouts()
        
        
    def init_labels(self):
        
        self.function_label=QLabel(self)
        self.min_label=QLabel(self)
        self.max_label=QLabel(self)
        
        self.function_label.setText("Function : ")
        self.min_label.setText("min : ")
        self.max_label.setText("max : ")
        
    def init_validator(self):
        
        qregx=QRegExp("[0-9]+")
        self.validator=QRegExpValidator(qregx,self)
        
    def init_fields(self):
        
        self.function_in=QLineEdit(self)
        self.min_in=QLineEdit(self)
        self.max_in=QLineEdit(self)
        
        self.max_in.setValidator(self.validator)
        self.min_in.setValidator(self.validator)
        
        self.max_in.textChanged[str].connect(self.textChanged)
        
    def init_canvas(self):
        
        self.canvas = MplCanvas(self, width=10, height=10, dpi=120)
        
    def init_btn(self):
        
        self.plt_btn=QPushButton("plot",self)
        self.plt_btn.clicked.connect(self.plot)
        
    def init_layouts(self):
        
        self.vbox = QVBoxLayout()
        self.hbox=QHBoxLayout()
        
        self.hbox.addWidget(self.function_label)
        self.hbox.addWidget(self.function_in)
        self.hbox.addWidget(self.min_label)
        self.hbox.addWidget(self.min_in)
        self.hbox.addWidget(self.max_label)
        self.hbox.addWidget(self.max_in)
        self.hbox.addWidget(self.plt_btn)
        
        self.vbox.addLayout(self.hbox)
        self.vbox.addWidget(self.canvas)
        
        self.setLayout(self.vbox)
    
    def textChanged(self):
        
        self.max_in.setStyleSheet('background-color: red')
    
    
    def plot(self):
        
        plotter=Plotter()
        
        func=self.function_in.text()
        minX=int(self.min_in.text())
        maxX=int(self.max_in.text())
         
        plotter(func,minX,maxX,self.canvas.axes)   
        self.canvas.draw()
        
    
    def run(self):
        # Show the form
        self.show()
        # Run the qt application
        
        

        
class MplCanvas(FigureCanvasQTAgg):
    
    '''
        A matplotlib canvas class to be passed as argument to the plotter class
        and to be embedded on the plotter GUI.
    
    '''

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111,xlabel="X",ylabel="Y")
        super(MplCanvas, self).__init__(fig)
        
        
if __name__== "__main__":
    qt_app = QApplication(sys.argv)
    app = PlotterGUI()
    app.run()
    qt_app.exec_()
    
    
    
    
    
    
    
    
    
    
        
