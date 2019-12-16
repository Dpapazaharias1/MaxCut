import numpy as np
import time
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
    bigM = 18
    roe = 0.98
    time = 0
    Runtime = 0

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

    def getSequence(self, val, k):
    	if(val == 1):
    		return self.bigM/(k+1)
    	if(val == 2):
    		return self.bigM*(self.roe**k)

    def getlagrangianDual(self):
        uSum = np.sum(self.uVector)
        diagU = np.identity(self.n) * self.uVector
        LUMatrix = self.L+ diagU
        eigenvalues, normEigenvectors = np.linalg.eig(LUMatrix)
        evMax = max(eigenvalues)
        zEV = (-0.25)*uSum + ((self.n/4)*evMax)
        return zEV, LUMatrix

    def stepFunction(self, seq, bigM, roe = 0.99):
        self.time = time.time()
        self.bigM, self.roe = bigM , roe
        self.uVector = np.array([0 for i in range(self.n)])
        gVector = np.array([-0.25 for i in range(self.n)])
        k = 1
    	#Main Loop
        while True:
            lagDual, LUMatrix = self.getlagrangianDual()
            j = np.argmax(np.diag(LUMatrix))
            gVector[j] = (self.n -1)/4
            seqVal = self.getSequence(seq,k)
            newVector = self.uVector - (seqVal)*(np.divide(gVector,np.linalg.norm(gVector,2)))
            gap = np.linalg.norm((newVector - self.uVector),2)
            #print(gap)
            self.uVector = newVector
            k = k + 1
            if(gap < 0.01):
                break
        self.Runtime = time.time() - self.time
        return lagDual



if __name__ == "__main__":
    import os
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    instance = "../dat/Graph_instance_n_20_d_0.2_s_1.dat"
    EV = EigenvalueRelaxation()
    EV.initialize(instance)
    EV.getEigenvalues()
    print("Maximum eigenvalue: {}".format(EV.evMax))
    print("Eigenvalue bound: {}".format(EV.getEigenvalueBound()))
    #----- Subgradient
    #stepFunction arguments(seq, stop, bigM, roe) --> seq = sequence number 1 or 2 from assignment. stop = stopping criteria for sequence loop
    # (optional)bigM = bigM value for sequence. (optional)roe = roe value for sequence 2
    print("LD Bound: {}".format(EV.stepFunction(2)))
