# combine the POD mode file with coordinate file xyz for paraview processing
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('M', type=int, help='the number of modes to be presented')
args = parser.parse_args()

mode_number = args.M

file_mesh_prefix = 'clip_xyz'
file_data_prefix = 'POD_mode'
file_suffix = 'csv'

# read mesh
file_name = '.'.join([file_mesh_prefix, file_suffix])
data_mesh = np.genfromtxt(file_name, names=True, delimiter=',')

data_mesh_names = data_mesh.dtype.names
data_mesh = data_mesh.view(data_mesh.dtype[0]).reshape(data_mesh.shape+(-1,))

# read and process mode
for i in range(mode_number):
    file_name = '.'.join([file_data_prefix, '{:d}'.format(i), file_suffix])
    data = np.genfromtxt(file_name, names=True, delimiter=',')

    names = ','.join(data.dtype.names + data_mesh_names)

    data = data.view(data.dtype[0]).reshape(data.shape+(-1,))

    data_all = np.concatenate((data,data_mesh),axis=1)

    np.savetxt(file_name,
               data_all, 
               fmt='%12.6e',
               delimiter=',', 
               header=names, 
               comments=''
              )
