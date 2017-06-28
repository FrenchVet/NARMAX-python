import ntpath
from solver import *
import numpy
import csv
from PlotCorrelationWindow import *
from PlotSignalPredictionWindow import *
from PlotResiduals import *
from PlotSERR import *
from PyQt5 import QtWidgets, QtCore

class NARMAX_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("NARMAX")
        MainWindow.resize(1280, 720)

        ########
        self.mainSolver = Solver() #variables
        self.yTitle = '' #name of the file containing the signal(y)
        self.xTitles = [] #array with the external inputs (x)
        self.mode = 2 #mode is automatically set as 2-step
        self.plotsWindows = [] #storage for handles of the plots generated in new windows
        ########
        self.initiate_layout(MainWindow)
        self.connectSignalsAndSlots()
        self.refresh()

    def initiate_layout(self, MainWindow):

        self.centralwidget = QtWidgets.QWidget(MainWindow)  # central widget ini
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setMinimumSize(QtCore.QSize(800, 600))

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget) #main layout is horizontal
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.centralwidget.setLayout(self.horizontalLayout)

        self.verticalLayout = QtWidgets.QVBoxLayout() #left column of widgets#######################################
        self.leftLabel = QtWidgets.QLabel("Input parameters")
        self.leftLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.addWidget(self.leftLabel)

        self.tableWidget1 = QtWidgets.QTableWidget(self.centralwidget) #table with uploaded data
        self.tableWidget1.setObjectName("tableWidget")
        self.tableWidget1.setColumnCount(2)
        self.tableWidget1.setRowCount(2)
        self.tableWidget1.horizontalScrollBar().hide()
        self.tableWidget1.horizontalHeader().hide()
        self.tableWidget1.verticalHeader().hide()
        self.tableWidget1.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.verticalLayout.addWidget(self.tableWidget1)
        self.tableWidget1.setMaximumWidth(200)

        self.Parameters = QtWidgets.QGroupBox() #box with editable parameters of modelling
        self.Parameters.setMaximumWidth(200)
        self.maxLagLabel = QtWidgets.QLabel('Max Lag')
        self.maxLevelLabel = QtWidgets.QLabel('Max level')
        self.modelTestRatioLabel = QtWidgets.QLabel('Model-To-Test data ratio')

        self.maxLagEdit = QtWidgets.QLineEdit('7')
        self.maxLevelEdit = QtWidgets.QLineEdit('2')
        self.modelTestRatioEdit = QtWidgets.QLineEdit('0.8')
        self.maxLagEdit.setMaximumWidth(30)
        self.maxLevelEdit.setMaximumWidth(30)

        self.grid = QtWidgets.QGridLayout()
        self.grid.addWidget(self.maxLagLabel, 1, 0)
        self.grid.addWidget(self.maxLagEdit, 1, 1)
        self.grid.addWidget(self.maxLevelLabel, 2, 0)
        self.grid.addWidget(self.maxLevelEdit, 2, 1)
        self.grid.addWidget(self.modelTestRatioLabel, 3, 0)
        self.grid.addWidget(self.modelTestRatioEdit, 3, 1)
        self.grid.setAlignment(QtCore.Qt.AlignRight)
        self.Parameters.setLayout(self.grid)
        self.verticalLayout.addWidget(self.Parameters)

        self.horizontalLayout.addLayout(self.verticalLayout)#####################################################

        self.verticalLayout2 = QtWidgets.QVBoxLayout() #central column of widgets

        self.horizontalButtonLayout = QtWidgets.QHBoxLayout() #buttons for modelling steps
        self.startNextButton = QtWidgets.QPushButton("Start")
        self.undoButton = QtWidgets.QPushButton("Undo")
        self.startNextButton.setMaximumWidth(150)
        self.undoButton.setMaximumWidth(150)
        self.horizontalButtonLayout.addWidget(self.undoButton)
        self.horizontalButtonLayout.addWidget(self.startNextButton)
        self.undoButton.setEnabled(False)
        self.startNextButton.setEnabled(False)

        self.fig = plt.figure() #plot area with toolbar
        self.canvas = FigureCanvas(self.fig)
        self.axes = self.fig.add_subplot(111)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.canvas.setObjectName("graphicsView")

        self.verticalLayout2.addLayout(self.horizontalButtonLayout)
        self.verticalLayout2.addWidget(self.canvas)
        self.verticalLayout2.addWidget(self.toolbar)

        self.horizontalLayout.addLayout(self.verticalLayout2)###########################################################

        self.verticalLayout3 = QtWidgets.QVBoxLayout() #right column of widdgets
        self.verticalLayout3.setObjectName("verticalLayout_2")
        self.rightLabel = QtWidgets.QLabel("Outcome Model")
        self.rightLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout3.addWidget(self.rightLabel)

        self.tableWidget3 = QtWidgets.QTableWidget(self.centralwidget) #calculated model parameters
        self.tableWidget3.setObjectName("tableWidget")
        self.tableWidget3.setColumnCount(3)
        self.tableWidget3.setRowCount(1)
        self.tableWidget3.horizontalScrollBar().hide()
        self.tableWidget3.horizontalHeader().hide()
        self.tableWidget3.verticalHeader().hide()
        self.tableWidget3.horizontalScrollBar().setEnabled(True)
        self.tableWidget3.setItem(0, 0, QtWidgets.QTableWidgetItem("Term"))
        self.tableWidget3.setItem(0, 1, QtWidgets.QTableWidgetItem("Parameter"))
        self.tableWidget3.setItem(0, 2, QtWidgets.QTableWidgetItem("ERR"))
        self.tableWidget3.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tableWidget3.resizeColumnsToContents()
        self.tableWidget3.setMaximumWidth(400)
        self.verticalLayout3.addWidget(self.tableWidget3)

        self.Statistics = QtWidgets.QGroupBox() #statistics about the model
        self.Statistics.setMaximumWidth(200)

        self.curreentSERRlabel = QtWidgets.QLabel('Current SERR')
        self.prevSERRvalue = QtWidgets.QLabel('0')
        self.curSERRlabel = QtWidgets.QLabel('Previous SERR')
        self.curSERRvalue = QtWidgets.QLabel('0')

        self.grid2 = QtWidgets.QGridLayout()
        self.grid2.addWidget(self.curreentSERRlabel, 1, 0)
        self.grid2.addWidget(self.prevSERRvalue, 1, 1)
        self.grid2.addWidget(self.curSERRlabel, 2, 0)
        self.grid2.addWidget(self.curSERRvalue, 2, 1)

        # self.grid2.setAlignment(QtCore.Qt.AlignRight)
        self.Statistics.setLayout(self.grid2)

        self.verticalLayout3.addWidget(self.Statistics)

        self.horizontalLayout.addLayout(self.verticalLayout3)
        MainWindow.setCentralWidget(self.centralwidget)#set the layout###############################################

        self.statusbar = QtWidgets.QStatusBar(MainWindow) #status bar
        self.statusbar.setObjectName("statusbar")
        self.statusLabel = QtWidgets.QLabel("Ready.")
        self.statusbar.addWidget(self.statusLabel)


        self.menubar = QtWidgets.QMenuBar(MainWindow)#menu ###################################################
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")

        self.menuStatistics = QtWidgets.QMenu(self.menubar)
        self.menuStatistics.setObjectName("menuStatistics")

        self.menuCorrelation = QtWidgets.QMenu(self.menubar)
        self.menuCorrelation.setObjectName("menuCorrelation")

        self.actionCorrResRes = QtWidgets.QAction(MainWindow)
        self.actionCorrResRes.setObjectName("actionCorrResRes")
        self.actionCorrSigSig = QtWidgets.QAction(MainWindow)
        self.actionCorrSigSig.setObjectName("actionCorrSigSig")

        self.actionPlotResiduals = QtWidgets.QAction(MainWindow)
        self.actionPlotResiduals.setObjectName("actionPlotResiduals")

        self.actionPlotPrediction = QtWidgets.QAction(MainWindow)
        self.actionPlotPrediction.setObjectName("actionPlotPrediction")

        self.actionPlotPredictionResiduals = QtWidgets.QAction(MainWindow)
        self.actionPlotPredictionResiduals.setObjectName("actionPlotPredictionResiduals")

        self.actionPlotSERR = QtWidgets.QAction(MainWindow)
        self.actionPlotSERR.setObjectName("actionPlotSERR")

        self.menuCorrelation.addAction(self.actionCorrResRes)
        self.menuCorrelation.addAction(self.actionCorrSigSig)
        self.menuStatistics.addMenu(self.menuCorrelation)
        self.menuStatistics.addAction(self.actionPlotResiduals)
        self.menuStatistics.addAction(self.actionPlotPrediction)
        self.menuStatistics.addAction(self.actionPlotPredictionResiduals)
        self.menuStatistics.addAction(self.actionPlotSERR)

        self.actionUpload = QtWidgets.QAction(MainWindow)
        self.actionUpload.setObjectName("actionUpload")
        self.actionUpload_input = QtWidgets.QAction(MainWindow)
        self.actionUpload_input.setObjectName("actionUpload_input")
        self.actionClearInputs = QtWidgets.QAction(MainWindow)
        self.actionClearInputs.setObjectName("actionClearInputs")

        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")

        self.menuChooseMode = QtWidgets.QMenu(self.menubar)
        self.menuChooseMode.setObjectName("actionChooseMode")

        self.actionOneStepMode = QtWidgets.QAction(MainWindow)
        self.actionOneStepMode.setObjectName("actiononeStepMode")

        self.actionTwoStepMode = QtWidgets.QAction(MainWindow)
        self.actionTwoStepMode.setObjectName("actionTwoStepMode")

        self.menuChooseMode.addAction(self.actionOneStepMode)
        self.menuChooseMode.addAction(self.actionTwoStepMode)

        self.menuFile.addAction(self.actionUpload)
        self.menuFile.addAction(self.actionUpload_input)
        self.menuFile.addAction(self.actionClearInputs)
        self.menuFile.addMenu(self.menuChooseMode)
        self.menuFile.addAction(self.actionSave)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuStatistics.menuAction())

        MainWindow.setMenuBar(self.menubar)
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)#initialisation of the gui
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow): #add labels to the menu
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuChooseMode.setTitle(_translate("MainWindow", "Choose mode"))
        self.menuStatistics.setTitle(_translate("MainWindow", "Statistics"))
        self.menuCorrelation.setTitle(_translate("MainWindow", "Cross-Correlation"))
        self.actionUpload.setText(_translate("MainWindow", "Upload signal (y)"))
        self.actionUpload_input.setText(_translate("MainWindow", "Upload input (x)"))
        self.actionClearInputs.setText(_translate("MainWindow", "Clear inputs"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionCorrSigSig.setText(_translate("MainWindow", "Correlation SigSig"))
        self.actionCorrResRes.setText(_translate("MainWindow", "Correlation ResRes"))
        self.actionPlotResiduals.setText(_translate("MainWindow", "Model residuals"))
        self.actionOneStepMode.setText(_translate("MainWindow", "One step mode"))
        self.actionTwoStepMode.setText(_translate("MainWindow", "Two step mode"))
        self.actionPlotPrediction.setText(_translate("MainWindow", "Model-based prediction"))
        self.actionPlotPredictionResiduals.setText(_translate("MainWindow", "Model-based prediction residuals"))
        self.actionPlotSERR.setText(_translate("MainWindow", "Plot SERR"))
        self.actionTwoStepMode.setCheckable(True)
        self.actionTwoStepMode.setChecked(True)
        self.actionOneStepMode.setCheckable(True)
        self.actionOneStepMode.setChecked(False)

    def connectSignalsAndSlots(self):
        self.actionUpload.triggered.connect(self.loadY)
        self.actionUpload_input.triggered.connect(self.loadX)
        self.actionClearInputs.triggered.connect(self.clearInputs)
        self.maxLagEdit.textChanged.connect(self.optimizationParamtereChange)
        self.maxLevelEdit.textChanged.connect(self.optimizationParamtereChange)
        self.modelTestRatioEdit.textChanged.connect(self.optimizationParamtereChange)
        self.startNextButton.clicked.connect(self.startStep)
        self.undoButton.clicked.connect(self.undo)
        self.actionSave.triggered.connect(self.saveModelAsCSV)
        self.actionOneStepMode.triggered.connect(self.modeChangedToOne)
        self.actionTwoStepMode.triggered.connect(self.modeChangedToTwo)
        self.actionCorrResRes.triggered.connect(self.plotCorrResRes)
        self.actionCorrSigSig.triggered.connect(self.plotCorrSigSig)
        self.actionPlotResiduals.triggered.connect(self.plotResiduals)
        self.actionPlotPrediction.triggered.connect(self.plotPrediction)
        self.actionPlotPredictionResiduals.triggered.connect(self.plotPredictionResiduals)
        self.actionPlotSERR.triggered.connect(self.plotSERR)

    def loadY(self):
        try:
            dlg = QtWidgets.QFileDialog()  #file dialog
            data_filename, _ = dlg.getOpenFileName(self, "Open file", None, "Text files (*.txt *.csv)")
            with open(data_filename, 'r') as opened_file: #read csv as a single column
                _, self.yTitle = ntpath.split(opened_file.name) #remember title in order to show it
                self.tableWidget1.setItem(0, 1, QtWidgets.QTableWidgetItem(self.yTitle))
                read = csv.reader(opened_file)  # open csv
                temp = []
                for row in read:
                    temp.append(float(row[0]))
                self.mainSolver.insert_y(numpy.array(temp))

        except:
            pass

        self.refresh()
        self.statusLabel.setText("Signal (y) loaded successfully.")
        self.statusLabel.setStyleSheet('color: black')

    def loadX(self):
        try:
            dlg = QtWidgets.QFileDialog()
            data_filename, _ = dlg.getOpenFileName(self, "Open file", None, "Text files (*.txt *.csv)")
            with open(data_filename, 'r') as opened_file:
                _, title = ntpath.split(opened_file.name)
                read = csv.reader(opened_file)  # open csv
                temp = []
                for row in read:
                    temp.append(float(row[0]))
                if len(temp) > len(self.mainSolver.resources.y):
                    temp = temp[:len(self.mainSolver.resources.y)]
                    self.mainSolver.insert_x(numpy.array(temp))
                    self.xTitles.append(title)
                    self.showMessage("Warning",
                                     "Provided data was too long, it was adjustet to the length of the signal.")
                elif len(temp) < len(self.mainSolver.resources.y):
                    self.showMessage("Warning", "Provided data is too short.")
                else:
                    self.mainSolver.insert_x(numpy.array(temp))
                    self.xTitles.append(title)
                    self.statusLabel.setText("Input (x) loaded successfully.")
                    self.statusLabel.setStyleSheet('color: black')

        except:
            pass

        self.refresh()


    def optimizationParamtereChange(self):#when optimisation parameters changed, they are checked
        try:
            newMaxLag = int(self.maxLagEdit.text())
            self.statusLabel.setText("New Max Lag accepted.")
            self.statusLabel.setStyleSheet('color: black')
        except:
            newMaxLag = 1
            self.statusLabel.setText("Warning! Strange parameter, Max Lag changed to 1 instead!")
            self.statusLabel.setStyleSheet('color: red')
        try:
            newMaxLev = int(self.maxLevelEdit.text())
            self.statusLabel.setText("New Max Level accepted.")
            self.statusLabel.setStyleSheet('color: black')
        except:
            newMaxLev = 1
            self.statusLabel.setText("Warning! Strange parameter, Max Level changed to 1 instead!")
            self.statusLabel.setStyleSheet('color: red')
        try:
            newRatio = float(self.modelTestRatioEdit.text())
            if newRatio > 0.9:
                self.statusLabel.setText("Warning! Ratio cannot be higher than 0.9. Changed to the max value instead.")
                self.statusLabel.setStyleSheet('color: red')
                newRatio = 0.9
            else:
                if newRatio < 0.1:
                    self.statusLabel.setText(
                        "Warning! Ratio cannot be lower than 0.1. Changed to the max value instead.")
                    self.statusLabel.setStyleSheet('color: red')
                    newRatio = 0.1
                else:
                    self.statusLabel.setText("New Ratio accepted.")
                    self.statusLabel.setStyleSheet('color: black')
        except:
            newRatio = 0.8
            self.statusLabel.setText("Warning! Strange parameter, Ratio changed to 0.8 instead!")
            self.statusLabel.setStyleSheet('color: red')

        self.mainSolver.chagne_max_lag(newMaxLag)
        self.mainSolver.change_max_level(newMaxLev)
        self.mainSolver.modelTestDataRatio = newRatio


        self.refresh()

    def refresh(self): #main plotting function, shows/hides stuff accordingly

        self.tableWidget1.clear() #beginning always consists of writing tables
        self.tableWidget3.clear()
        self.axes.cla()

        self.tableWidget3.setItem(0, 0, QtWidgets.QTableWidgetItem("Term"))
        self.tableWidget3.setItem(0, 1, QtWidgets.QTableWidgetItem("Parameter"))
        self.tableWidget3.setItem(0, 2, QtWidgets.QTableWidgetItem("ERR"))
        self.tableWidget3.setRowCount(self.mainSolver.currentStep + 1)
        for index in range(self.mainSolver.currentStep):
            self.tableWidget3.setItem(1 + index, 0,
                                      QtWidgets.QTableWidgetItem(str(self.mainSolver.model.modelTermsNames[index])))
            self.tableWidget3.setItem(1 + index, 1, QtWidgets.QTableWidgetItem(str(self.mainSolver.model.beta[index])))
            self.tableWidget3.setItem(1 + index, 2, QtWidgets.QTableWidgetItem(str(self.mainSolver.model.ERR[index])))
        setItemsReadOnly(self.tableWidget3)#tabels are only to read

        self.tableWidget1.setRowCount(len(self.xTitles) + 2)
        self.tableWidget1.setItem(0, 0, QtWidgets.QTableWidgetItem("Variable"))
        self.tableWidget1.setItem(0, 1, QtWidgets.QTableWidgetItem("Source File"))
        self.tableWidget1.setItem(1, 0, QtWidgets.QTableWidgetItem("y"))
        self.tableWidget1.setItem(1, 1, QtWidgets.QTableWidgetItem(self.yTitle))
        for num, path in enumerate(self.xTitles):
            self.tableWidget1.setItem(2 + num, 0, QtWidgets.QTableWidgetItem("x" + str(num)))
            self.tableWidget1.setItem(2 + num, 1, QtWidgets.QTableWidgetItem(path))
        setItemsReadOnly(self.tableWidget1)#tabels are only to read

        self.axes.plot(self.mainSolver.resources.y.tolist(), label='Signal') #plot stuff
        self.axes.plot(self.mainSolver.model.simulatedY.tolist(), label='Model')
        plt.legend(loc=1)
        self.canvas.draw()

        if not self.mainSolver.currentStep:  ##Step == 0, most of the things are hidden
            self.actionUpload.setEnabled(True)
            self.actionCorrResRes.setEnabled(False)
            self.actionPlotResiduals.setEnabled(False)
            self.actionPlotPrediction.setEnabled(False)
            self.actionPlotPredictionResiduals.setEnabled(False)
            self.actionPlotSERR.setEnabled(False)

            self.actionSave.setEnabled(False)
            self.menuChooseMode.setEnabled(True)

            self.startNextButton.setText('Start')
            self.prevSERRvalue.setText('0')
            self.curSERRvalue.setText('0')

            self.maxLagEdit.setEnabled(True)
            self.maxLevelEdit.setEnabled(True)
            self.modelTestRatioEdit.setEnabled(True)
            self.undoButton.setEnabled(False)

            if not (self.mainSolver.resources.y.size): #step == 0, but y data is loaded
                self.startNextButton.setEnabled(False)
                self.actionUpload_input.setEnabled(False)
                self.actionClearInputs.setEnabled(False)
                self.actionCorrSigSig.setEnabled(False)
            else:
                self.startNextButton.setEnabled(True)
                self.actionUpload_input.setEnabled(True)
                self.actionClearInputs.setEnabled(True)
                self.actionCorrSigSig.setEnabled(True)

        else: #step != 0, data must have been loaded before
            self.actionCorrSigSig.setEnabled(True)
            self.actionCorrResRes.setEnabled(True)
            self.actionPlotResiduals.setEnabled(True)
            self.actionUpload.setEnabled(False)
            self.actionUpload_input.setEnabled(False)
            self.actionClearInputs.setEnabled(False)
            self.actionSave.setEnabled(True)
            self.actionPlotPrediction.setEnabled(True)
            self.actionPlotPredictionResiduals.setEnabled(True)
            self.actionPlotSERR.setEnabled(True)
            self.menuChooseMode.setEnabled(False)

            self.startNextButton.setText('Next')
            self.prevSERRvalue.setText(str(sum(self.mainSolver.model.ERR)))
            self.curSERRvalue.setText(str(sum(self.mainSolver.model.ERR[:-1])))

            self.maxLagEdit.setEnabled(False)
            self.maxLevelEdit.setEnabled(False)
            self.modelTestRatioEdit.setEnabled(False)
            self.undoButton.setEnabled(True)
            self.startNextButton.setEnabled(True)

    def startStep(self): #next step or start according to current state
        if not self.mainSolver.currentStep:
            if self.mode == 2:
                self.mainSolver.start2()
            else:
                self.mainSolver.start()
        else:
            if self.mode == 2:
                self.mainSolver.step2()
            else:
                self.mainSolver.step()

        self.statusLabel.setText("New model term appended successfully.")
        self.statusLabel.setStyleSheet('color: black')

        self.refresh()

    def undo(self):
        if self.mainSolver.currentStep:
            self.mainSolver.undo()
            self.statusLabel.setText("Last term deleted successfully.")
            self.statusLabel.setStyleSheet('color: black')
        self.refresh()

    def saveModelAsCSV(self):
        try:
            options = QtWidgets.QFileDialog.Options()
            options |= QtWidgets.QFileDialog.DontUseNativeDialog
            fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                                "All Files (*);;Text Files (*.txt *.csv)",
                                                                options=options)

            with open(fileName, 'w') as f:
                writer = csv.writer(f)
                for row in range(self.tableWidget3.rowCount()):
                    rowdata = []
                    for column in range(self.tableWidget3.columnCount()):
                        item = self.tableWidget3.item(row, column)
                        if item is not None:
                            rowdata.append(str(item.text()))
                        else:
                            rowdata.append('')
                    writer.writerow(rowdata)
                for row in range(self.tableWidget1.rowCount()):
                    rowdata = []
                    for column in range(self.tableWidget3.columnCount()):
                        item = self.tableWidget3.item(row, column)
                        if item is not None:
                            rowdata.append(str(item.text()))
                        else:
                            rowdata.append('')
                    writer.writerow(rowdata)
            self.statusLabel.setText("Data saved successfully.")
            self.statusLabel.setStyleSheet('color: black')

        except:
            pass

    def modeChangedToOne(self):
        self.actionTwoStepMode.setChecked(False)
        self.actionOneStepMode.setChecked(True)
        self.mode = 1
        self.statusLabel.setText("Method changed successfully.")
        self.statusLabel.setStyleSheet('color: black')

    def modeChangedToTwo(self):
        self.actionTwoStepMode.setChecked(True)
        self.actionOneStepMode.setChecked(False)
        self.mode = 2
        self.statusLabel.setText("Method changed successfully.")
        self.statusLabel.setStyleSheet('color: black')

    def showMessage(self, title, message):
        messageBox = QtWidgets.QMessageBox()
        messageBox.setIcon(QtWidgets.QMessageBox.Information)
        messageBox.setWindowTitle(title)
        messageBox.setText(message)
        messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        messageBox.exec_()

    def clearInputs(self):
        self.mainSolver.resources.X = []
        self.xTitles = []
        self.refresh()
        self.statusLabel.setText("Inputs cleared successfully.")
        self.statusLabel.setStyleSheet('color: black')

    def plotCorrResRes(self): #plot autocorrelation of residuals
        self.plotSignalInNewWindow("Cross correlation between residuals and themselves",
                                   self.mainSolver.model.corrResRes)

    def plotSERR(self):  # plot autocorrelation of residuals
        self.plotsWindows.append(
            PlotSERR("SERR", self.mainSolver.model.ERR, 0))
        self.plotsWindows[-1].show()

    def plotCorrSigSig(self):
        self.plotSignalInNewWindow("Cross correlation between signal derivative and its square",
                                   self.mainSolver.resources.corrSigSig)

    def plotResiduals(self):
        self.plotsWindows.append(PlotCorrelationWindow("Calculated model residuals", self.mainSolver.model.residuals))
        self.plotsWindows[-1].show()

    def plotPrediction(self):
        simY = self.mainSolver.model.simulate(self.mainSolver.resources.fullX, len(self.mainSolver.resources.simData))
        testY = numpy.concatenate((self.mainSolver.resources.y, self.mainSolver.resources.simData), axis=0)
        self.plotsWindows.append(PlotSignalPredictionWindow("Signal prediction vs test data", testY, simY, len(self.mainSolver.resources.y)))
        self.plotsWindows[-1].show()

    def plotPredictionResiduals(self):
        simY = self.mainSolver.model.simulate(self.mainSolver.resources.fullX, len(self.mainSolver.resources.simData))
        testY = numpy.concatenate((self.mainSolver.resources.y, self.mainSolver.resources.simData), axis=0)
        self.plotsWindows.append(
            PlotResiduals("Model prediction residuals", numpy.abs(numpy.subtract(simY, testY)),
                          len(self.mainSolver.resources.y)))
        self.plotsWindows[-1].show()

    def plotSignalInNewWindow(self, title, sig):
        self.plotsWindows.append(PlotCorrelationWindow(title, sig))
        self.plotsWindows[-1].show()


def setItemsReadOnly(QTableWidget):
    rows = QTableWidget.rowCount()
    columns = QTableWidget.columnCount()
    for i in range(rows):
        for j in range(columns):
            item = QTableWidget.item(i, j)
            item.setFlags(QtCore.Qt.ItemIsEnabled)
