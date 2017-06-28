from PyQt5 import QtWidgets
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

class PlotSignalPredictionWindow(QtWidgets.QWidget):
    def __init__(self, name, testData, simulatedData, pos):
        QtWidgets.QWidget.__init__(self)
        self.fig = plt.figure() #this windows is made of only a plot, its toolbar and a text on the top
        self.canvas = FigureCanvas(self.fig)
        self.axes = self.fig.add_subplot(111)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.initLayout(name, testData, simulatedData, pos)

    def initLayout(self, name, testData, simulatedData, pos):
        self.title = QtWidgets.QLabel(name)
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.title)
        vbox.addWidget(self.canvas)
        vbox.addWidget(self.toolbar)

        self.axes.plot(testData, label='Signal')
        self.axes.plot(simulatedData, label='Model prediction')
        if pos:#if a position is provided, a vertical line is ploted in order to distinguish model from the simulation
            plt.axvline(x=pos, linewidth=1, color='r', linestyle='--')
        plt.legend(loc=1)
        plt.xlabel('Sample number')
        plt.ylabel('Signal value')
        self.canvas.draw()
        self.setLayout(vbox)
        self.show()
