"""

Zhen Lu 2018/08/13

An implementation of the POD with the snapshot method

"""
import numpy as np
from scipy import linalg
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('N', type=int, help='the number of snapshots')
parser.add_argument('M', type=int, help='the number of modes to be presented')
args = parser.parse_args()

file_number = args.N
mode_number = args.M

file_prefix = 'clip_POD0'
file_suffix = 'csv'

filename = 'POD.dat'

var_names = ['U0', 'U1', 'U2']
var_str = ''.join(var_names)

# load the average data first
data_ave = np.genfromtxt('clip_ave.csv',
                         names=True,
                         delimiter=','
                        )

# get data size
data = np.empty((data_ave.size,len(var_names)))
data_len = data_ave.size*len(var_names)
data_bytesize = data_ave.dtype[0].itemsize

# memmap
fp = np.memmap(filename, 
               dtype=data_ave.dtype[0], 
               mode='w+', 
               shape=(data_len,file_number), 
               order='F')

# read and calculate perturbation, store in fp
for i in range(file_number):
    file_name = '.'.join([file_prefix,'{:d}'.format(i),file_suffix])
    data_ins = np.genfromtxt(file_name, names=True, delimiter=',')

    for j, var in enumerate(var_names):
        data[:,j] = data_ins[var] - data_ave[var]
        
    fp[:,i] = data.flatten()

del fp

# compose the covariance matrix
matrix_cov = np.empty((file_number, file_number))

for i in range(file_number):
    data_i = np.memmap(filename,
                       dtype=data_ave.dtype[0],
                       mode='r+',
                       shape=(data_len,1),
                       order='F',
                       offset=i*data_len*data_bytesize
                      )
    
    matrix_cov[i,i] = np.sum( np.square(data_i) )
    
    for j in range(i+1,file_number):
        data_j = np.memmap(filename,
                           dtype=data_ave.dtype[0],
                           mode='r+',
                           shape=(data_len,1),
                           order='F',
                           offset=j*data_len*data_bytesize
                          )
        
        matrix_cov[i,j] = np.sum( np.multiply( data_i, data_j ) )
        matrix_cov[j,i] = matrix_cov[i,j]

# eigen decomposition
e, v = linalg.eig(matrix_cov)

# sort eigenvalues and eigenvectors
idx = np.argsort( e )[::-1]

# the matrix is symmetric, all eigenvalues are non-negative real
eig = np.real(e)[idx]
sigma = np.sqrt(eig)

v = v[:,idx]

# save modes
modes = np.zeros([data_len, mode_number], order='F')

for i in range(file_number):
    data = np.memmap(filename,
                     dtype=data_ave.dtype[0],
                     mode='r+',
                     shape=(data_len,1),
                     order='F',
                     offset=i*data_len*data_bytesize
                    ).flatten()

    for j in range(mode_number):
        modes[:,j] += data*v[i,j]
        
for j in range(mode_number):
    modes[:,j] /= sigma[j]

# save the modes
for j in range(mode_number):
    file_name = '.'.join(['POD_mode_{}'.format(var_str),
                          '{:d}'.format(j),
                          file_suffix])
    np.savetxt(file_name,
               modes[:,j].reshape(data_ave.size,len(var_names)),
               fmt='%12.6e',
               delimiter=',',
               header=','.join(var_names),
               comments=''
              )

# coefficients, eigenvalues, sigma, and the Vij of the first X modes
data = np.concatenate((eig.reshape((-1,1)), sigma.reshape((-1,1)), v[:,:mode_number]),axis=1)

var_names = [ 'V{:d}'.format(i) for i in range(mode_number) ]
var_names.insert(0, 'sigma')
var_names.insert(0, 'eigval')

np.savetxt('POD_coef_{}.csv'.format(var_str),
           data,
           fmt = '%12.6e',
           delimiter = ',',
           header = ','.join(var_names),
           comments = ''
          )

