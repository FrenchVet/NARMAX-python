from PyQt5 import QtWidgets
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

class PlotSERR(QtWidgets.QWidget):
    def __init__(self, name, signal, pos):
        QtWidgets.QWidget.__init__(self)
        self.fig = plt.figure() #this windows is made of only a plot, its toolbar and a text on the top
        self.canvas = FigureCanvas(self.fig)
        self.axes = self.fig.add_subplot(111)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.initLayout(name, signal)

    def initLayout(self, name, signal):
        self.title = QtWidgets.QLabel(name)
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.title)
        vbox.addWidget(self.canvas)
        vbox.addWidget(self.toolbar)

        tmpToPlot = []

        for sample in range(len(signal)+1):
            tmpToPlot.append(sum(signal[0:sample]))
        self.axes.plot(tmpToPlot, 'ko', tmpToPlot, 'k')
        # self.axes.plot(tmpToPlot)
        plt.xlabel('Model term')
        plt.ylabel('SERR')
        self.canvas.draw()
        self.setLayout(vbox)
        self.show()
