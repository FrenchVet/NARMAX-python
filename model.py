import numpy
from scipy import signal


#this clas contains all model parameters


class Model:
    beta = [] #parameters of the model terms
    A = [] #matrix for the calculation of teh parameters
    G = [] #parameters for the orthogonalised terms
    Q = [] #orthogonalised terms
    P = [] #actual model terms
    ERR = [] #error reduction ratio, how a certain orthogonalised term reduced the error of the modeling
    simulatedY = numpy.array([])
    residuals = numpy.array([])
    corrResRes = numpy.array([]) #auto correlation between modelling residuals
    modelTermsNames = []

    def calculateStatistics(self, y): #basically residuals and auto correlation of residuals
        if self.P:
            self.residuals = numpy.subtract(y, self.simulatedY)
            self.corrResRes = signal.correlate(self.residuals, self.residuals, mode='same') #/ len(y)
            mean = numpy.mean(self.residuals)
            coefficient = sum(numpy.power(numpy.subtract(self.residuals, mean), 2))
            self.corrResRes = numpy.divide(self.corrResRes, coefficient)

        else:
            self.residuals = numpy.array([])
            self.corrResRes = numpy.array([])

    def simulate(self, X, length): #generate signal from external inputs for a certain amoutn of samples
        simulation = self.simulatedY.tolist() #start with the signal already computed (it's in the solver)
        signalLength = len(simulation) #for indexing purpose
        for k in range(length):
            sample = 0 #new sample that will be added
            for number, terms in enumerate(self.modelTermsNames):
                if terms[0][0] == 'c': #if a term is a constant, it is just addded to the sample value
                    sample = sample + self.beta[number]
                else:
                    termSample = self.beta[number] #another variable for multiplying different regressors in a term
                                                    #start with the poarameter that is next to the term
                    for name in terms:
                        if name[0] == 'y':  #decipher the regressor name from resources
                            lag = int(name[-1])
                            termSample = termSample*simulation[-lag] #get appropriate value and multiply it to the value
                        else:
                            lag = int(name[-1]) #as above, but external input is already present, so it has the demanded
                            #  length, so its index should start with the base length of the signal, plus steps that
                            #were already done, minus lag concluded from the term
                            termSample = termSample * X[int(name[1])][signalLength+k-lag]
                    sample = sample + termSample #sum all inputs for the sample

            simulation.append(sample)
        simulation = numpy.array(simulation)
        return simulation


