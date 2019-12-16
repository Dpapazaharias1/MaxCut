from Graph import Graph 
import numpy as np
import math
import time


class Ellipsoid:
    
    G = Graph()
    n = 0
    m = 0
    y = []
    w = []
    g = []
    mapv = []
    var = 0 # Number of variables Y_ij, not including diagonal and Y_ji
    H = 0
    R = 0
    Q = [] # List of eigenvectors for PSD constraints
    change = 100
    epsilon = 0.001
    objCurrent = 0
    Runtime = 0

    def initialize(self, inputfile):
        self.G.read(inputfile)
        self.n = self.G.n
        self.m = self.G.m
        counter = 0
        for i in range(self.n):
            for j in range(i+1, self.n):
                    self.y.append(0)
                    self.w.append(self.G.adjMatrix[i][j])
                    self.g.append(0.5*self.G.adjMatrix[i][j])
                    self.mapv.append((i,j))
                    counter += 1
        
        self.y = np.array([self.y]).T
        self.g = np.array([self.g]).T
        self.var = len(self.y)
        self.R = 2*self.n
        self.H = (self.R**2) * np.eye(self.var)

    def __computeObj(self):
        zcurr = 0
        for i in range(self.var):
            zcurr += self.w[i] * (1-self.y[i])
        zcurr = 0.5*zcurr
        return zcurr[0]

    def __listToMatrix(self):
        yBar = np.eye(self.n)
        counter = 0
        for i in range(self.n):
            for j in range(i+1, self.n):
                yBar[i][j] = self.y[counter]
                yBar[j][i] = self.y[counter]
                counter += 1
        return yBar

    def __checkFeasible(self):
        yBar = self.__listToMatrix()
        eigValues, eigVectors = np.linalg.eig(yBar)
        minEig = np.amin(eigValues)
        minIndex = np.where(eigValues == minEig)[0][0]
        if minEig < 0:
            return eigVectors[:, minIndex]
        else:
            return np.array([])
    
    def __getConstrGradient(self, q):
        gBar = np.zeros((self.var,1))
        counter = 0
        for i in range(self.n):
            for j in range(i+1, self.n):
                gBar[counter] = -q[i] * q[j]
                counter += 1
        return gBar

    def __update(self, y, g):
        Hg = self.H.dot(g)
        gTH = g.T.dot(self.H)
        HggTH = Hg.dot(gTH)
        Hdenom = g.T.dot(Hg)
        ySubtract = (1.0/(self.var + 1)) * (1.0/math.sqrt(Hdenom)) * Hg
        self.y = y - ySubtract
        hSubtract = (2.0/(self.var+1)) * (1.0/float(Hdenom)) * HggTH
        newH = self.H - hSubtract
        self.H = ((self.var**2)/((self.var**2) - 1))*newH

    def solve(self):
        start = time.time()
        counter = 0
        while self.change > self.epsilon:
            yCurrent = np.copy(self.y)
            qNew = self.__checkFeasible()
            if qNew.size > 0:
                self.Q.append(qNew)
                gBar = self.__getConstrGradient(qNew)
                self.__update(yCurrent, gBar)
            else:
                self.__update(yCurrent, self.g)
                self.objCurrent = self.__computeObj()
            self.change = np.linalg.norm(yCurrent-self.y)
            counter += 1
        self.Runtime = time.time() - start

if __name__ == "__main__":
    import os
    import sys
    n = 10
    d = 0.2
    s = 1
    if len(sys.argv) == 4:
        n = sys.argv[1]
        d = sys.argv[2]
        s = sys.argv[3]
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    instance = "../dat/Graph_instance_n_{}_d_{}_s_{}.dat".format(n,d,s)
    #-----------------  
    SDP = Ellipsoid()
    SDP.initialize(instance)
    start = time.time()
    SDP.solve()
    print('Runtime: {}'.format(SDP.Runtime))
    print(SDP.objCurrent)