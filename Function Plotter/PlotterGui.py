import re
import sys

from PySide2.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from Plotter import Plotter


class PlotterGUI(QWidget):
    """
    Plotter Gui for plotting functions for a given range of input.

    """

    def __init__(self):
        self.qt_app = QApplication(sys.argv)
        QWidget.__init__(self)
        self.setWindowTitle('Plotter GUI')
        self.setMinimumWidth(400)

        self.init_labels()
        self.init_fields()
        self.init_canvas()
        self.init_btn()
        self.init_layouts()

    def init_labels(self):

        self.function_label = QLabel(self)
        self.min_label = QLabel(self)
        self.max_label = QLabel(self)

        self.function_label.setText("Function : ")
        self.min_label.setText("min : ")
        self.max_label.setText("max : ")

    def init_fields(self):

        self.wrongMinMax = False
        self.wrongFn = False

        self.function_in = QLineEdit(self)
        self.min_in = QLineEdit(self)
        self.max_in = QLineEdit(self)

        self.min_in.textChanged[str].connect(self.textChanged)
        self.max_in.textChanged[str].connect(self.textChanged)
        self.function_in.textChanged[str].connect(self.functionTextChanged)

    def init_canvas(self):

        self.canvas = MplCanvas(self, width=10, height=10, dpi=120)

    def init_btn(self):

        self.plt_btn = QPushButton("plot", self)
        self.plt_btn.clicked.connect(self.plot)

    def init_layouts(self):

        self.vbox = QVBoxLayout()
        self.hbox = QHBoxLayout()

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

        self.wrongMinMax = False

        if not self.wrongFn:
            self.plt_btn.clicked.disconnect()
            self.plt_btn.clicked.connect(self.plot)

        self.min_in.setStyleSheet('color: green')
        self.max_in.setStyleSheet('color: green')

        if not (self.min_in.text().strip('-').isnumeric()):
            self.min_in.setStyleSheet('color: red')
            self.plt_btn.clicked.disconnect()
            self.plt_btn.clicked.connect(self.show_warning)
            self.wrongMinMax = True

        if not (self.max_in.text().strip('-').isnumeric()):
            self.max_in.setStyleSheet('color: red')
            self.plt_btn.clicked.disconnect()
            self.plt_btn.clicked.connect(self.show_warning)
            self.wrongMinMax = True

    def functionTextChanged(self):

        self.wrongFn = False

        if not self.wrongMinMax:
            self.plt_btn.clicked.disconnect()
            self.plt_btn.clicked.connect(self.plot)

        self.function_in.setStyleSheet('color: green')

        reg = "(([/])?([\+-\-])?(([0-9])+[*])?([a-zA-Z])+((\^)[\+-\-]?[0-9]+)?)+"
        match = re.search(reg, self.function_in.text())
        txtLen = len(self.function_in.text())

        if not (match is None):

            regLen = match.span()[1]

            if not (txtLen == regLen):
                self.function_in.setStyleSheet('color: red')
                self.plt_btn.clicked.disconnect()
                self.plt_btn.clicked.connect(self.show_warning)

                self.wrongFn = True

    def plot(self):

        plotter = Plotter()

        func = self.function_in.text()
        minX = int(self.min_in.text())
        maxX = int(self.max_in.text())

        plotter(func, minX, maxX, self.canvas.axes)
        self.canvas.draw()

    def show_warning(self):

        if self.wrongMinMax:
            self.warning_txt = "min and max values should take integer values ! "

        elif self.wrongFn:
            self.warning_txt = " Function must be in this format : 2*x^0+x+2*x^2 or -x^-1/x^2 "

        QMessageBox.warning(self, "Wrong input", self.warning_txt)

    def run(self):
        # Show the form
        self.show()
        # Run the qt application
        self.qt_app.exec_()


class MplCanvas(FigureCanvasQTAgg):
    """
        A matplotlib canvas class to be passed as argument to the plotter class
        and to be embedded on the plotter GUI.

    """

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111, xlabel="X", ylabel="Y")
        super(MplCanvas, self).__init__(fig)


if __name__ == "__main__":
    app = PlotterGUI()
    app.run()
