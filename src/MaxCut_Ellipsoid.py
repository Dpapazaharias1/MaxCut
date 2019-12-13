from Graph import Graph 
import numpy as np 
import numpy.linalg as lin 
import math 

### FUNCTIONS ###

def checkFeasible(y):
    # solve minimum v'Yv, using ybar matrix 
    # import pdb; pdb.set_trace()
    ybar = dictToMatrix(y)
    ybar_eigvalues, ybar_eigvectors = lin.eig(ybar)
    min_value = np.amin(ybar_eigvalues)
    min_index = np.where(ybar_eigvalues == np.amin(ybar_eigvalues))
    if min_value >= 0:
        return None
    else:
        return ybar_eigvectors[min_index[0][0]]

def computeConstrGradient(y, q, var):
    # compute gbar for next step
    gbar = np.zeros(var)
    counter = 0 
    for key in y:
        ij_string = key.split(',')
        i = int(ij_string[0])
        j = int(ij_string[1])
        gbar[counter] = q[i] + q[j]
        counter += 1
    return gbar

def computeY(y, H, g):
    # compute next Y
    Hg = H.dot(g) # numerator of big fraction
    Hdenom = math.sqrt(g.T.dot(Hg)) # denominator
    subtract = (1/G.n+1)*(1/Hdenom)*Hg # entire subtracion term
    yvec = dictToVector(y, mapv) # flip to vector
    yvec = yvec - subtract # subtract
    return vectorToDict(yvec, mapv) # return new variables (dictionary)

def computeH(y, H, g):
    # compute next H
    HggtH = ((H.dot(g)).dot(g.T))*H # numerator of big fraction
    Hdenom = g.T.dot(H.dot(g)) # denominator of big fraction
    subtract = (2/(G.n+1))*(1/Hdenom)*HggtH
    H = H - subtract
    return ((G.n**2)/((G.n**2)-1))*H

def computeObj(w, y):
    # compute current objective value
    zcurr = 0
    for key in y:
        zcurr += w[key]*(1-y[key])
    zcurr = -0.5*zcurr
    return zcurr

def dictToVector(y, mapv):
    # convert dictionary y to vector y for matrix ops
    yvec = np.zeros(var)
    for key in y:
        yvec[mapv[key]] = y[key]
    return yvec

def vectorToDict(yvec, mapv):
    # convert y vector to a dictionary of decision variables
    y = {}
    for key in mapv:
        y[key] = yvec[mapv[key]]
    return y 

def dictToMatrix(y):
    # take dict y and turn it into ybar matrix
    # ones on the diagonal (variable ii, not used), yij in spot yij
    # matrix needed for eigenvector operations to check feasibility
    ybar = np.eye(G.n)
    for key in y:
        ij_string = key.split(',')
        i = int(ij_string[0])
        j = int(ij_string[1])
        ybar[i][j] = y[key]
    return ybar

# read instance
G = Graph()
G.read('Graphtest.txt')

# initialize variables and parameters
y = {} # decision variable y dictionary
w = {} # weights dictionary
mapv = {} # dictionary to map variable key names "i,j" to index in vectors
counter = 0
for i in range(G.n):
    for j in range(G.n):
        if i < j:
            y["{},{}".format(i, j)] = 0
            w["{},{}".format(i, j)] = G.adjMatrix[i][j] 
            mapv["{},{}".format(i, j)] = counter
            counter += 1
        else:
            pass
var = len(y) # number of variables in y, without double counting or counting "ii"s
g = np.zeros(var) # initialize constant objective function gradient
counter = 0
for key in w:
    g[counter] = -w[key]
    counter += 1
H = np.eye(var) # starting ellipsoid, circle of radius r
Q = [] # keep track of eigenvectors used
r = math.sqrt(G.m)
H = r*H
epsilon = 0.00000001
change = 100
zcurr = computeObj(w, y)

#####################################################################################
##################################### MAIN LOOP #####################################
#####################################################################################

counter = 0
print("Initial y: {}".format(y))
while change > epsilon:
    qvector = checkFeasible(y)
    if qvector == None: 
        y = computeY(y, H, g)
        H = computeH(y, H, g)
    else: 
        gbar = computeConstrGradient(y, qvector, var)
        Q.append(qvector)
        y = computeY(y, H, gbar)
        H = computeH(y, H, gbar)
    # print("Iteration {}: {}".format(counter, y))
    z_old = zcurr
    zcurr = computeObj(w, y)
    change = abs(z_old - zcurr)
    counter += 1

print("Iterations: {}".format(counter))
print("Solution: {}".format(y))
print("Objective: {}".format(zcurr))
print("Eigenvectors added: {}".format(Q))
print(w)

#####################################################################################
#####################################################################################
#####################################################################################




