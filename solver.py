import numpy
from model import Model
from modellingResources import Data
import time

class Solver:
    model = Model()
    resources = Data()
    currentStep = 0
    modelTestDataRatio = 0.8

    def insert_y(self, newy):
        self.resources.y = numpy.array(newy)
        self.resources.sigma = newy @ newy
        self.resources.calculateCorrSigSig()

    def insert_x(self, newx): #it should be assured, that external input is inserted AFTER the signal (y), in order to
                            #assure proper data length
        if len(newx) > len(self.resources.y):
            newx = newx[:len(self.resources.y)]
            self.resources.X.append(numpy.array(newx))
        elif len(newx) < len(self.resources.y):
            print("Provided data is too short")
        else:
            self.resources.X.append(numpy.array(newx))

    def chagne_max_lag(self, newmaxlag): #it should be assured that these value is provided with integers
        self.resources.maxLag = newmaxlag

    def change_max_level(self, newmaxlevel):#it should be assured that these value is provided with integers
        self.resources.maxLevel = newmaxlevel

    def start(self): #start of the one-step-ahead prediction method
        start = time.clock()
        if len(self.resources.y): #when there is data
            self.resources.divide_data_set(self.modelTestDataRatio) #divide data into the test and moddeling set
            self.resources.combine_all()  #generate a regressor matrix
            max = 0 #initialise
            whichRegresorToEliminate = 0
            tempG = 0
            tempQ = 0
            tempP = 0
            tempERR = 0
            tempName = ''
            for i, regresor in enumerate(self.resources.regressors):
                regresor = numpy.array(regresor) #assure that regressor is a numpy type and cosider it as an orthogonal
                                                #model element
                g = (numpy.transpose(self.resources.y) @ regresor) / (numpy.transpose(regresor) @ regresor) #calculate
                                        #corresponding parameter to the term
                ERR = g ** 2 * ((numpy.transpose(regresor) @ regresor) / self.resources.sigma) #error reduction ratio
                if ERR > max:#if it's the highest err, consider the term chosen
                    max = ERR
                    tempG = g
                    tempQ = regresor
                    tempP = regresor
                    tempERR = ERR
                    tempName = self.resources.names[i]
                    whichRegresorToEliminate = i
            self.model.G.append(tempG) #after looping through all the regressors, the best one is chosen and appended
            self.model.Q.append(tempQ)
            self.model.P.append(tempP)
            self.model.ERR.append(tempERR)
            self.model.modelTermsNames.append(tempName)

            self.resources.deletedIndexes.append(whichRegresorToEliminate) #save for an undo case
            self.resources.deletedNames.append(tempName)
            self.resources.deletedRegressors.append(self.resources.regressors[whichRegresorToEliminate])

           #delete chosen regressor
            self.resources.regressors = numpy.delete(self.resources.regressors, whichRegresorToEliminate, 0)
            del self.resources.names[whichRegresorToEliminate]

            self.currentStep = self.currentStep + 1
            self.finish() #method which calculates model from the chosen terms
            end = time.clock()
            print(end - start)

        else:
            print('There is no input to the model')

    def step(self): #user needs to assure that function "start" was invoked before
        start = time.clock()
        max = 0
        whichRegresorToEliminate = 0
        tempG = 0
        tempQ = 0
        tempP = 0
        tempERR = 0
        tempName = ''
        for i, regresor in enumerate(self.resources.regressors): #as above
            q = regresor #accept the base of the next orthogonal contribution as the regressor
            for qr in self.model.Q: #calculate the orthogonalised base from the previous terms
                q = q - (((numpy.transpose(regresor) @ qr) / (numpy.transpose(qr) @ qr)) * qr)
            g = (numpy.transpose(self.resources.y) @ q) / (numpy.transpose(q) @ q)
            ERR = g ** 2 * ((numpy.transpose(q) @ q) / self.resources.sigma)
            if ERR > max:
                max = ERR
                tempG = g
                tempQ = q
                tempP = regresor
                tempERR = ERR
                tempName = self.resources.names[i]
                whichRegresorToEliminate = i

        self.model.G.append(tempG)
        self.model.Q.append(tempQ)
        self.model.P.append(tempP)
        self.model.ERR.append(tempERR)

        self.resources.deletedIndexes.append(whichRegresorToEliminate)
        self.resources.deletedNames.append(tempName)
        self.resources.deletedRegressors.append(self.resources.regressors[whichRegresorToEliminate])

        self.model.modelTermsNames.append(tempName)
        self.resources.regressors = numpy.delete(self.resources.regressors, whichRegresorToEliminate, 0)
        del self.resources.names[whichRegresorToEliminate]
        self.currentStep = self.currentStep + 1
        self.finish()
        end = time.clock()
        print(end - start)

    def start2(self): #as above, jutro method is little different inside
        if len(self.resources.y):
            start = time.clock()
            self.resources.divide_data_set(self.modelTestDataRatio)
            self.resources.combine_all()
            max = 0
            whichRegresorToEliminate = 0
            tempG = 0
            tempQ = 0
            tempP = 0
            tempERR = 0
            tempName = ''
            for i, regresor in enumerate(self.resources.regressors):
                regresor = numpy.array(regresor)
                g = (numpy.transpose(self.resources.y) @ regresor) / (numpy.transpose(regresor) @ regresor)
                ERR = g ** 2 * ((numpy.transpose(regresor) @ regresor) / self.resources.sigma)

                for regresor2 in self.resources.regressors: #after regressor is calculated it is also considered as a base for the next choice
                    q = regresor2 - (((numpy.transpose(regresor2) @ regresor) / (numpy.transpose(regresor) @ regresor)) * regresor)
                    if not sum(q): #if it is the same regressor it is abandonned
                        continue
                    g2 = (numpy.transpose(self.resources.y) @ q) / (numpy.transpose(q) @ q)
                    ERR2 = ERR + g2 ** 2 * ((numpy.transpose(q) @ q) / self.resources.sigma)#ERR@ is calculated as a
                    #sum of error reduction ratios of the first choice, and the choice that would come afterwards

                    if ERR2 > max:
                        max = ERR2
                        tempG = g
                        tempQ = regresor
                        tempP = regresor
                        tempERR = ERR
                        tempName = self.resources.names[i]
                        whichRegresorToEliminate = i

            self.model.G.append(tempG)
            self.model.Q.append(tempQ)
            self.model.P.append(tempP)
            self.model.ERR.append(tempERR)

            self.resources.deletedIndexes.append(whichRegresorToEliminate)
            self.resources.deletedNames.append(tempName)
            self.resources.deletedRegressors.append(self.resources.regressors[whichRegresorToEliminate])

            self.model.modelTermsNames.append(tempName)
            self.resources.regressors = numpy.delete(self.resources.regressors, whichRegresorToEliminate, 0)
            del self.resources.names[whichRegresorToEliminate]
            self.currentStep = self.currentStep + 1
            self.finish()
            end = time.clock()
            print(end-start)
        else:
            print('There is no input to the model')

    def step2(self): #user needs to assure that function "start2" was invoked before
        start = time.clock()
        max = 0
        whichRegresorToEliminate = 0
        tempG = 0
        tempQ = 0
        tempP = 0
        tempERR = 0
        tempName = ''
        for i, regresor in enumerate(self.resources.regressors):
            q = regresor
            for qr in self.model.Q:
                qr = numpy.array(qr)
                q = q - (((numpy.transpose(regresor) @ qr) / (numpy.transpose(qr) @ qr)) * qr)
            g = (numpy.transpose(self.resources.y) @ q) / (numpy.transpose(q) @ q)
            ERR = g ** 2 * ((numpy.transpose(q) @ q) / self.resources.sigma)

            for regresor2 in self.resources.regressors:
                q2 = regresor2 #as in the function "step" but with the two-step methodology
                for qr in self.model.Q:
                    q2 = q2 - (((numpy.transpose(regresor2) @ qr) / (numpy.transpose(qr) @ qr)) * qr)
                q2 = q2 - (((numpy.transpose(regresor2) @ q) / (numpy.transpose(q) @ q)) * q)
                if not sum(q2):
                    continue
                g2 = (numpy.transpose(self.resources.y) @ q2) / (numpy.transpose(q2) @ q2)
                ERR2 = ERR + g2 ** 2 * ((numpy.transpose(q2) @ q2) / self.resources.sigma)

            if ERR2 > max:
                max = ERR
                tempG = g
                tempQ = q
                tempP = regresor
                tempERR = ERR
                tempName = self.resources.names[i]
                whichRegresorToEliminate = i

        self.model.G.append(tempG)
        self.model.Q.append(tempQ)
        self.model.P.append(tempP)
        self.model.ERR.append(tempERR)

        self.resources.deletedIndexes.append(whichRegresorToEliminate)
        self.resources.deletedNames.append(tempName)
        self.resources.deletedRegressors.append(self.resources.regressors[whichRegresorToEliminate])

        self.model.modelTermsNames.append(tempName)
        self.resources.regressors = numpy.delete(self.resources.regressors, whichRegresorToEliminate, 0)
        del self.resources.names[whichRegresorToEliminate]
        self.currentStep = self.currentStep + 1
        self.finish()
        end = time.clock()
        print(end-start)
    def finish(self):
        self.model.A = numpy.zeros([len(self.model.Q), len(self.model.Q)]) #matrix used for transition between
                                            #orthogonalised bases and regressors. It has zeros belowe the main diagonal
        for r, qTerm in enumerate(self.model.Q):
            self.model.A[r, r] = 1 #ones at the main diagonal
            for c, pTerm in enumerate(self.model.P[(r + 1):]):#apropriate terms above the main diagonal
                c = c + r + 1
                self.model.A[r, c] = ((numpy.transpose(qTerm) @ pTerm) / (numpy.transpose(qTerm) @ qTerm))
        self.model.beta = numpy.linalg.solve(self.model.A, numpy.array(self.model.G)) #model terms parameters are
                                                        #calculated from the A matrix and orthogonalised parameters
        self.model.simulatedY = numpy.array([])
        for k in range(len(self.model.P)):
            if not k: #first element is treated as a base
                self.model.simulatedY = numpy.multiply(self.model.beta[k], self.model.P[k])
            else: #next, bases and regressors are multiplied by each other and added to the signal
                self.model.simulatedY = numpy.add(self.model.simulatedY, numpy.multiply(self.model.beta[k], self.model.P[k]))
        self.model.calculateStatistics(self.resources.y) #statisticas are mainly residuals of the mdoel and its corr

    def reset(self): #never used function, but maybe it could be useful someday
        self.model = Model()
        self.resources = Data()
        self.currentStep = 0
        self.modelTestDataRatio = 0.8

    def undo(self): #come back a ster
        if self.currentStep: #are there any steps that can be undone? (philosophical question)
            self.model.G.pop()#pop elements that are usually added as a result of a modelling step
            self.model.P.pop()
            self.model.Q.pop()
            self.model.ERR.pop()
            self.model.modelTermsNames.pop()
            self.finish() #calculate model accordingly to the current values

            restoredIndex = self.resources.deletedIndexes.pop() #obtain elemenets that where deleted after a modelling
                                                                # step
            resoteredName = self.resources.deletedNames.pop()
            resotredRegresor = self.resources.deletedRegressors.pop()

            self.resources.names.insert(restoredIndex, resoteredName) #put them back on their place
            tempRegs = self.resources.regressors.tolist()
            tempRegs.insert(restoredIndex, resotredRegresor)
            self.resources.regressors = numpy.array(tempRegs)

            self.currentStep = self.currentStep - 1 #reduce step

            if not self.currentStep: #if user came back to the step 0
                self.resources.concatenateDataSet() #concatenate modellingand test data
