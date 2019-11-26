class Graph:
    n = 0
    m = 0
    edges = []
    adjLists = []
    adjWeight = []
    adjMatrix = []
    totWeight = 0

    def read(self, inputfile):
        f = open(inputfile, 'r')
        line = f.readline()
        fields = str.split(line)
        self.n = int(fields[0])
        self.m = int(fields[1])

        for i in range(self.n):
            self.adjLists.append([])
            self.adjWeight.append([])
            self.adjMatrix.append([0 for i in range(self.n)])

        for line in f:
            fields = line.split('\t')
            i = int(fields[0])
            j = int(fields[1])
            self.adjLists[i].append(j)
            self.adjLists[j].append(i)
            w_e = 1
            if len(fields) > 2:
                w_e = float(fields[2])
            self.edges.append((i,j,w_e))
            self.totWeight += abs(w_e)
            self.adjWeight[i].append(w_e)
            self.adjWeight[j].append(w_e)
            self.adjMatrix[i][j] = w_e
            self.adjMatrix[j][i] = w_e
        f.close
