from PyQt5 import QtWidgets
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from math import sqrt

class PlotCorrelationWindow(QtWidgets.QWidget):
    def __init__(self, name, signal):
        QtWidgets.QWidget.__init__(self)
        self.fig = plt.figure()#this windows is made of only a plot, its toolbar and a text on the top
        self.canvas = FigureCanvas(self.fig)
        self.axes = self.fig.add_subplot(111)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.initLayout(name, signal)

    def initLayout(self, name, signal):

        upperLimit = 1.96/sqrt(len(signal)) #there limits are considered as 95% certainty areas for the correlation to
                                            #not show non-linearities or poor modelling
        lowerLimit = -upperLimit

        self.title = QtWidgets.QLabel(name)
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.title)
        vbox.addWidget(self.canvas)
        vbox.addWidget(self.toolbar)

        middle = round(len(signal)/2) #middle of the signal, since correlation is calculated from zero to both sides

        x = list(range(-20, 20)) #the area of interest
        y = []
        for i in x:
            y.append(signal[middle+i+1])

        self.axes.plot(x, y, 'ko', x, y, 'k')
        plt.xlabel('Lags')
        plt.ylabel('Cross correlation')
        plt.axhline(y=upperLimit, linewidth=1, color='r', linestyle='--')
        plt.axhline(y=lowerLimit, linewidth=1, color='r', linestyle='--')
        self.canvas.draw()
        self.setLayout(vbox)
        self.show()
