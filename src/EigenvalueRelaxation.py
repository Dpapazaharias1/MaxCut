import numpy as np
from Graph import *

class EigenvalueRelaxation():
    G = Graph()
    n = 0
    m = 0
    L = 0 # Laplacian
    D = 0 # Weighted "Degree" Matrix
    A = 0 # Weighted "Indicdence" Matrix
    eigenvalues = []
    evMax = 0
    normEigenvectors =[]
    uVector = []
    bigM = 50
    roe = 0.98

    def initialize(self, inputfile):
        self.G.read(inputfile)
        self.n = self.G.n
        self.m = self.G.m
        self.A = self.G.adjMatrix
        self.D = [[0 for i in range(self.n)] for j in range(self.n)]
        for i in range(self.n):
            self.D[i][i] = sum(self.G.adjWeight[i])
        # Convert A and D to numpy matrices
        self.A = np.matrix(self.A)
        self.D = np.matrix(self.D)
        # Construct Laplacian
        self.L = np.subtract(self.D, self.A)

    def getEigenvalues(self):
        self.eigenvalues, self.normEigenvectors = np.linalg.eig(self.L)
        self.evMax = max(self.eigenvalues)

    def getEigenvalueBound(self):
        return self.n * self.evMax / 4.0

    def getlagrangianDual(self):
        uSum = np.sum(self.uVector)
        diagU = np.identity(self.n) * np.diag(self.uVector)
        LUMatrix = self.L+ diagU
        eigenvalues, normEigenvectors = np.linalg.eig(LUMatrix)
        evMax = max(eigenvalues)
        zEV = (-0.25)*uSum + ((self.n/4)*evMax)
        return zEV, LUMatrix

    def stepFunction(self):
    	self.uVector = [0 for i in range(self.n)]
    	self.uVector = np.array(self.uVector)
    	gVector = [-0.25 for i in range(self.n)]
    	gVector = np.array(gVector)
    	#Main Loop
    	for k in range(0,100):
    		lagDual, LUMatrix = self.getlagrangianDual()
    		diagLU = np.diag(LUMatrix)
    		j = np.argmax(diagLU)
    		gVector[j] = (self.n - 1)/4
    		self.uVector = self.uVector - (self.bigM*(self.roe**k))*(np.divide(gVector,np.linalg.norm(gVector,2)))

    	return lagDual




if __name__ == "__main__":
    import os
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    instance = "../dat/Graph_instance_n_50_d_0.8_s_1.dat"
    EV = EigenvalueRelaxation()
    EV.initialize(instance)
    EV.getEigenvalues()
    print("Maximum eigenvalue: {}".format(EV.evMax))
    print("Eigenvalue bound: {}".format(EV.getEigenvalueBound()))
    #----- Subgradient
    print("LD Bound: {}".format(EV.stepFunction()))
