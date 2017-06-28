import design
from PyQt5 import QtWidgets
import sys

class NARMAX(QtWidgets.QMainWindow, design.NARMAX_MainWindow):
    def __init__(self, parent=None):
        super(NARMAX, self).__init__(parent)
        self.setupUi(self)

def main():
    app = QtWidgets.QApplication(sys.argv)  # A new instance of QApplication
    form = NARMAX()                 # We set the form to be our ExampleApp (design)
    form.setWindowTitle("NARMAX")
    form.show()                         # Show the form
    app.exec_()                         # and execute the app

if __name__ == '__main__':              # if we're running file directly and not importing it
    main()