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
    normEigenvectors =[]

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


if __name__ == "__main__":
    import os
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    instance = "../dat/Graph_instance_n_10_d_0.2_s_1.dat"
    EV = EigenvalueRelaxation()
    EV.initialize(instance)
    EV.getEigenvalues()
    print("Maximum eigenvalue: {}".format(max(EV.eigenvalues)))
    
