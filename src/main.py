if __name__ == "__main__":
    import os
    import sys
    import csv
    print('Number of arguments: {}'.format(len(sys.argv)))
    print('Argument(s) passed: {}'.format(str(sys.argv)))
    inputfile = sys.argv[-1]
    inputsplit = inputfile.split('_')
    seed = int(inputsplit[-1].split('.')[0])
    nodes = int(inputsplit[3])
    density = float(inputsplit[5])
    if sys.argv[1] == "IP":
        from MaxCut_IP import MaxCut
        print("Solving Max Cut IP:")
        MC = MaxCut()
        MC.initialize(inputfile)
        MC.solve()
    elif sys.argv[1] == "LP":
        from MaxCut_IP import MaxCut
        print("Solving Max Cut LP Relaxation:")
        MC = MaxCut()
        MC.initialize(inputfile)
        MC.solveLP()
        if os.path.exists('./results/LPBound.csv'):
            with open('./results/LPBound.csv', 'a') as csvfile:
                writer = csv.writer(csvfile, delimiter = ',')
                writer.writerow([nodes, density, seed, MC.model.objval, MC.model.Runtime])
        else:
            with open('./results/LPBound.csv', 'a') as csvfile:
                writer = csv.writer(csvfile, delimiter = ',')
                writer.writerow(['n', 'd', 's', 'bound', 'time(s)'])
                writer.writerow([nodes, density, seed, MC.model.objval, MC.model.Runtime])

    elif sys.argv[1] == "LD":
        from EigenvalueRelaxation import EigenvalueRelaxation
        print('Solving Eigenvalue Relaxation:')
        EV = EigenvalueRelaxation()
        EV.initialize(inputfile)

    elif sys.argv[1] == "SDP":
        #from ellipsoid
        print('Solving Semi-Definite Relaxation:')

    elif sys.argv[1] == "heuristic":
        from MaxCut_Heuristic import MaxCut_Heuristic
        MCH = MaxCut_Heuristic()
        MCH.initialize(inputfile)
        MCH.simulatedAnnealing()

    else:
        print("No solution method selected")
