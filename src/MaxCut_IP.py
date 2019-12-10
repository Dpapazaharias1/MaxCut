from gurobipy import *
from Graph import *

class MaxCut:
    G = Graph()
    n = 0
    m = 0
    model = 0
    y = {}
    x = {}
    
    def __initializeModel(self):
        self.model = Model("MaxCut")
        #---- Variables
        # TODO: Can we relax the binary variables for y's.
        for i in range(self.n):
            self.x[i] = self.model.addVar(vtype=GRB.BINARY, obj = 0, lb = 0, ub = 1, name='vertex_{}'.format(i))
            for j in self.G.adjLists[i]:
                if i < j:
                    self.y[i, j] = self.model.addVar(vtype=GRB.BINARY, obj = self.G.adjMatrix[i][j], lb = 0, ub = 1,  name='edge_{}_{}'.format(i,j))
        #---- Model Parameters
        self.model.modelSense = GRB.MAXIMIZE
        self.model.update()
        #---- Constraints
        # TODO: Check if constraints (4) and (5) are redundant.
        for i in range(self.n):
            for j in self.G.adjLists[i]:
                if i < j:
                    self.model.addConstr(self.y[i,j] <= 2 - self.x[i] - self.x[j])
                    self.model.addConstr(self.y[i,j] <= self.x[i] + self.x[j])
                    self.model.addConstr(self.y[i,j] >= self.x[i] - self.x[j]) # Possibly redundant
                    self.model.addConstr(self.y[i,j] >= self.x[j] - self.x[i]) # Possibly redundant


    def initialize(self, inputfile):
        self.G.read(inputfile)
        self.n = self.G.n
        self.m = self.G.m
        self.__initializeModel()

    def solveLP(self):
        for i in range(self.n):
            self.x[i].vtype = GRB.CONTINUOUS
            for j in self.G.adjLists[i]:
                if i < j:
                    self.y[i,j].vtype = GRB.CONTINUOUS
        self.model.optimize()
        
    def solve(self):
        for i in range(self.n):
            self.x[i].vtype = GRB.BINARY
            for j in self.G.adjLists[i]:
                if i < j:
                    self.y[i,j].vtype = GRB.BINARY
        self.model.optimize()

if __name__ == "__main__":
    import os
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    instance = "../dat/Graph_instance_n_10_d_0.2_s_1.dat"
    MC = MaxCut()
    MC.initialize(instance)
    MC.solve()
