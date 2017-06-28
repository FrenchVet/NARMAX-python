import numpy
import itertools
from scipy import signal

#it's a class that contains all teh required data for the modelling
#it is able to calculate other useful stuff, but in general it's a base for modelling

class Data:
    y = numpy.array([]) #signal
    corrSigSig = numpy.array([]) #cross correlation of the signal derivative and its derivative squared
    simData = numpy.array([]) #part fo data left for testing
    X = [] #an array of signals which are considered for modelling as inputs
    fullX = [] #same signals as above, but longer for  testing
    sigma = 0 #sigma of the signal (standard d
    maxLevel = 2 #maximal level of he nonlinearity. Due to simple processing it cannot be higher than 9
    maxLag = 7 #maximal lag of the regressors. Due to simple processing it cannot be higher than 9
    regressors = []
    names = []

    deletedRegressors = [] #variables used as a backup if user would like to undo
    deletedNames = []
    deletedIndexes = []

    def combine_all(self): #generation of the regressor matrix along with the similar matrix with regressor names
        arrays = []  #base regressor vectors and names, which later are combined
        baseNames = []
        for lag in range(1, self.maxLag+1): #for every possible lag of y, starting from 1
            rolled = numpy.roll(self.y, lag).tolist() #move signal accordingly
            rolled[:lag] = [0]*lag #empty the first samples
            arrays.append(rolled)
            baseNames.extend(['y-'+str(lag)])
        for inputNumber, inputVar in enumerate(self.X): #same for external input, but it can has 0 lag
            for lag in range(0, self.maxLag+1):
                rolled = numpy.roll(inputVar, lag).tolist()
                rolled[:lag] = [0] * lag
                arrays.append(rolled)
                baseNames.extend(['x' + str(inputNumber) + '-' + str(lag)])
        temp = [1]*len(self.y) #generate regressor for the constant term
        self.regressors = [temp] #append constant term at the beginning, because it is not supposed to be mixed
        self.names = ['const']

        for i in range(1, self.maxLevel + 1): #mixing depending on the level
            els = [list(x) for x in itertools.combinations_with_replacement(arrays, i)] #combine regressors with
                                                                                        # replacements for current level
            if i > 1: #when there are multiple regressors to multiply
                out = []
                for regresor in els: #multiply differen regresser independently from their quantity. Regressor has muliple arrays
                                    #zip combines corresponding elements which are later multiplied
                    out.append([numpy.prod(numpy.array(x)) for x in zip(*regresor)])
                self.regressors.extend(out)
            else:#regressors are single, so there is no need to multiply
                out = []
                for regresor in els:
                    out.append(regresor[0])
                self.regressors.extend(out)
            els = [list(x) for x in itertools.combinations_with_replacement(baseNames, i)] #names are just shu
            # ffled and
                                                                                            #appended
            self.names.extend(els)

        self.regressors = numpy.array(self.regressors) #regressors shoudl be numpy elements

    def divide_data_set(self, percentage): #divide data for future testing
        if not len(self.simData): #when there is data
            where = round(len(self.y)*percentage) #find an index of the split
            self.simData = self.y[where:]
            self.y = self.y[0:where]
            self.sigma = self.y @ self.y #calculate standard deviation afterwards
            for indeks in range(len(self.X)): #split the external data
                self.fullX.append(self.X[indeks]) #data for testing should be original size
                self.X[indeks] = self.X[indeks][0:where]  #data for modeling should be shorter

    def concatenateDataSet(self): #as above, but other direction
        if len(self.simData):
            self.y = numpy.concatenate((self.y, self.simData), axis=0)
            self.simData = numpy.array([])
            self.sigma = self.y @ self.y
            for indeks in range(len(self.X)):
                self.X[indeks] = self.fullX[indeks]
            self.fullX = []

    def calculateCorrSigSig(self):      #calculate derivative of the signal, its derivative square and cross corelation
                                        # between them
        if len(self.y):  #if tehre is sginal
            derY = numpy.diff(self.y)
            derYsq = numpy.power(derY, 2)
            self.corrSigSig = signal.correlate(derY, derYsq, mode='same')# / len(self.y)
        else:
            self.corrSigSig = numpy.array([])
