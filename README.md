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
