# Maximum Cut

  Final project for IE671: Nonlinear Optimization by Demetrios Papazaharias, Carter Mann, and Luca Wrabetz

## Compiling Information

  We have provided a ```makefile``` in order to efficiently run each instance of MaxCut using differnet methods. 
  
  | Command              | Result                                                                    |
|----------------------|---------------------------------------------------------------------------|
| ```make LP```        | Compute the LP Bound for all instances                                    |
| ```make IP```        | Solve the IP Bound for all instances                                      |
| ```make LD```        | Compute eigenvalue relaxation and Lagrangian Dual bound for all instances |
| ```make ellipsoid``` | Compute Semi-Definite Program relaxation bound for all instances          |
| ```make heuristic``` | Solve simulated annealing heuristic for all instances                     |

 If you prefer to run a specific instance for a method individually. Change directory to ```src``` and 
