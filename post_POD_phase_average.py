import numpy as np

num_bins = 8

file_prefix = 'clip_POD0'
file_suffix = 'csv'

filename = 'clip_ave.csv'
data = np.genfromtxt(filename, delimiter=',', skip_header=1)

data_ave = np.zeros( (num_bins,) + data.shape )
data_count = np.zeros( num_bins )

with open(filename, 'r') as f:
    names = f.readline().rstrip('\n')

filename = 'POD_coef.csv'
data = np.genfromtxt(filename, delimiter=',', names=True)
num_snapshots = data.size

r = np.sqrt(np.square(data['V0'])+np.square(data['V1']))
v = (data['V0']+data['V1']*1j)/r
theta = np.real(np.log(v)/1j)

bin_l = (-1+1./num_bins)*np.pi
bin_u = (1-1./num_bins)*np.pi

bins = np.linspace( bin_l, bin_u, num_bins )

for i, v in enumerate(theta):
    if np.logical_or( v < bin_l, v>=bin_u ):
        idx = 0
    else:
        idx = np.digitize(v, bins)

    filename = '.'.join([file_prefix,'{:d}'.format(i),file_suffix])
    data = np.genfromtxt(filename, delimiter=',', skip_header=1)

    data_ave[idx,:,:] += data
    data_count[idx] += 1.

for idx in range(num_bins):
    data_ave[idx,:,:] /= data_count[idx]

    filename = '.'.join(['POD_phase','{:d}'.format(idx),file_suffix])

    np.savetxt(filename,
               data_ave[idx,:,:], 
               fmt='%12.6e', 
               delimiter=',', 
               header=names, 
               comments='' 
              )
