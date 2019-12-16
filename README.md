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

 If you prefer to run a specific instance for a method use the following command

```console
foo@bar:~$ python ./src/<filename>.py n d s
```
Where `n`, `d`, and `s` correspond to the size of the instance, density and seed, respectively. The choices for ```<filename>``` are:



| Filename                           | Result                                            |
|------------------------------------|---------------------------------------------------|
| ```MaxCut_IP.py```                 | Solve the IP                                      |
| ```MaxCut_Ellipsoid.py```          | Compute Semi-Definite Program relaxation bound    |
| ```EigenvalueRelaxation.py``` | Compute eigenvalue relaxation and Lagrangian Dual |
| ```MaxCut_Heuristic.py```     | Compute the lower bound for Max Cut               |
