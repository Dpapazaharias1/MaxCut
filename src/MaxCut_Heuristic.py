import random
import math
from Graph import *

class MaxCut_Heuristic:
    G = Graph()
    n = 0
    m = 0
    edges = []
    currentWeight = 0
    bestWeight = 0
    S = []
    Sbar = []
    A = []
    bestSolution = []

    def initialize(self, inputfile):
        self.G.read(inputfile)
        self.n = self.G.n
        self.m = self.G.m
        self.edges = sorted(self.G.edges, key = lambda x: x[2], reverse=True)

    def greedySolution(self):
        self.A = [0 for i in range(self.n)] # Assignment list
        for i, j, w_e in self.edges:
            if self.A[i] == 0 and self.A[j] == 0: # If i,j are unassigned
                self.A[i] = -1
                self.A[j] = 1
                self.currentWeight += w_e
            elif (self.A[i] == 1 and self.A[j] == -1) or (self.A[i] == -1 and self.A[j] == 1): # i,j are in opposite sets
                self.currentWeight += w_e
            elif self.A[i] == 1 and self.A[j] == 0: # i belongs to S, j unassigned
                self.A[j] = -1
                self.currentWeight += w_e
            elif self.A[i] == -1 and self.A[j] == 0: # i belngs to Sbar, j unassigned
                self.A[j] = 1
                self.currentWeight += w_e 
            elif self.A[j] == 1 and self.A[i] == 0: # j belongs to S, i unassigned
                self.A[i] = -1
                self.currentWeight += w_e 
            elif self.A[j] == -1 and self.A[i] == 0: # j belongs to Sbar, i unassigned
                self.A[i] = 1
        self.bestWeight = self.currentWeight
        self.bestSolution = self.A[:]
    

    def __swap(self, i): # Computes change in objective from switching which part of the cut i belongs
        c = 0
        for u in self.G.adjLists[i]:
            if self.A[i] == self.A[u]:
                c += self.G.adjMatrix[i][u]
            elif self.A[i] == -self.A[u]:
                c -= self.G.adjMatrix[i][u]
        return c

    def __calcChange(self, i, j): # Compute cost of swapping two nodes in different cut sets
        c_i = self.__swap(i) # Compute cost of swapping i
        c_j = self.__swap(j) # Compute cost of swapping j
        c = c_i + c_j + 2*self.G.adjMatrix[i][j] # i,j will still belong to separate components
        return c

    def __findCMax(self):
        # Get worst possible swap
        maxC = 0
        for i in range(self.n):
            for j in range(self.n):
                if self.A[i] == -self.A[j]:
                    cost = self.__calcChange(i,j)
                    if cost < maxC:
                        maxC = cost
        return maxC

    def __update(self, i, j, costChange):
        self.currentWeight += costChange
        self.A[i] = -self.A[i]
        self.A[j] = -self.A[j]

    def simulatedAnnealing(self, stopTemp=1, tempLength=1000, coolRate=0.99, cMaxAccept=-10):
        # If A is empty, run greedy solution to get initial sol
        if not self.A:
            self.greedySolution()
        
        print("Initial Objective: {}".format(self.currentWeight))
        print("Initial Solution: {}".format(self.A))
        
        cMax = self.__findCMax()
        initialTemp = -cMax/math.log(-cMaxAccept)
        currentTemp = initialTemp
        V = [v for v in range(self.n) if self.A[v] != 0]
        
        while currentTemp > stopTemp:
            for t in range(tempLength):
                i = random.choice(V)
                j = random.choice([v for v in V if self.A[v] == -self.A[i]])
                costChange = self.__calcChange(i, j)
                if costChange > 0:
                    self.__update(i, j, costChange)
                else:
                    q = random.random()
                    if q < math.exp(costChange/currentTemp):
                        self.__update(i, j, costChange)
                    else:
                        pass # do nothing
                if self.bestWeight < self.currentWeight:
                    print("New incumbent: Swap ({},{}): DeltaC = {}, Best Sol = {}".format(i,j,costChange, self.currentWeight))
                    print("Current Solution: {}".format(self.A))
                    self.bestWeight = self.currentWeight
                    self.bestSolution = self.A[:]
            currentTemp = currentTemp * coolRate


if __name__ == "__main__":
    import os
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    instance = "../dat/Graph_instance_n_10_d_0.2_s_1.dat"
    H = MaxCut_Heuristic()
    H.initialize(instance)
    H.simulatedAnnealing()
    print("Best Objective: {}".format(H.bestWeight))
    print("Best Solution: {}".format(H.bestSolution))
            