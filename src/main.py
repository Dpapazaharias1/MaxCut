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
        if os.path.exists('./results/IPSol.csv'):
            with open('./results/IPSol.csv', 'a') as csvfile:
                writer = csv.writer(csvfile, delimiter = ',')
                writer.writerow([nodes, density, seed, MC.model.objval, MC.model.objBound, MC.model.MIPGap, MC.model.Runtime])
        else:
            with open('./results/IPSol.csv', 'a') as csvfile:
                writer = csv.writer(csvfile, delimiter = ',')
                writer.writerow(['n', 'd', 's', 'best', 'bound', 'gap', 'time(s)'])
                writer.writerow([nodes, density, seed, MC.model.objval, MC.model.objBound, MC.model.MIPGap, MC.model.Runtime])

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
        EV.getEigenvalues()
        bigM = 2*nodes
        seq = 2
        if os.path.exists('./results/LDBound.csv'):
            with open('./results/LDBound.csv', 'a') as csvfile:
                writer = csv.writer(csvfile, delimiter = ',')
                writer.writerow([nodes, density, seed, EV.evMax, EV.getEigenvalueBound(), bigM, EV.stepFunction(seq,bigM), EV.Runtime])
        else:
            with open('./results/LDBound.csv', 'a') as csvfile:
                writer = csv.writer(csvfile, delimiter = ',')
                writer.writerow(['n', 'd', 's', 'maxEigenval', 'EigenvalueBound', 'bigM', 'LDBound','time(s)'])
                writer.writerow([nodes, density, seed, EV.evMax, EV.getEigenvalueBound(), bigM, EV.stepFunction(seq,bigM), EV.Runtime])


    elif sys.argv[1] == "ellipsoid":
        print('Solving Ellipsoid:')
        from MaxCut_Ellipsoid import Ellipsoid
        MCE = Ellipsoid()
        MCE.initialize(inputfile)
        MCE.solve()
        if os.path.exists('./results/Ellipsoid.csv'):
            with open('./results/Ellipsoid.csv', 'a') as csvfile:
                writer = csv.writer(csvfile, delimiter = ',')
                writer.writerow([nodes, density, seed, MCE.objCurrent, MCE.Runtime])
        else:
            with open('./results/Ellipsoid.csv', 'a') as csvfile:
                writer = csv.writer(csvfile, delimiter = ',')
                writer.writerow(['n', 'd', 's', 'bound', 'time(s)'])
                writer.writerow([nodes, density, seed, MCE.objCurrent, MCE.Runtime])
    
    elif sys.argv[1] == "heuristic":
        from MaxCut_Heuristic import MaxCut_Heuristic
        MCH = MaxCut_Heuristic()
        MCH.initialize(inputfile)
        MCH.simulatedAnnealing(coolRate=0.99, tempLength = 1000, cMaxAccept=0.1)
        if os.path.exists('./results/HeuristicSol.csv'):
            with open('./results/HeuristicSol.csv', 'a') as csvfile:
                writer = csv.writer(csvfile, delimiter = ',')
                writer.writerow([nodes, density, seed, MCH.stopTemp, MCH.tempLength, MCH.coolRate, MCH.cMaxAccept, MCH.bestWeight, MCH.bestTime, MCH.Runtime])
        else:
            with open('./results/HeuristicSol.csv', 'a') as csvfile:
                writer = csv.writer(csvfile, delimiter = ',')
                writer.writerow(['n', 'd', 's','stopTemp', 'tempLength', 'coolRate', 'cMax', 'solution', 'Soltime(s)','Runtime(s)'])
                writer.writerow([nodes, density, seed, MCH.stopTemp, MCH.tempLength, MCH.coolRate, MCH.cMaxAccept, MCH.bestWeight, MCH.bestTime, MCH.Runtime])

    else:
        print("No solution method selected")
