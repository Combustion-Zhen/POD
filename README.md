# POD
implementation of the proper orthogonal decomposition

input:

in commend line:
N   the number of snapshots
M   the number of modes

files:
snapshots
averaged field

data files should be in csv form

snapshots file named as [file\_prefix].[file\_number].[file\_suffix],
where [file\_prefix] and [file\_suffix] are specified in the script, [file\_number] is a int in range(N)

averaged file name is in the line of data\_ave = np.genfromtxt...

data to be employed for POD is specified in var\_names

output:
    POD_coef.csv    containing eigenvalues and first M mode eigenvectors
    POD_mode.csv

citation:
```
@inproceedings{Lu2018
author = {{Lu}, Zhen and {Elbaz}, Ayman M. and {Hernandez Perez}, Francisco E. and {Roberts}, William L. and {Im}, Hong G.},
        title = "{Large Eddy Simulations of the Vortex-Flame Interaction in a Turbulent Swirl Burner}",
    booktitle = {APS Division of Fluid Dynamics Meeting},
         year = "2018",
        month = "November",
          eid = {Q2.005}
}
```
