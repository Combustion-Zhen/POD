import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch

# cm inch transfer for matplotlib
def cm2inch(*tupl):
    inch = 2.54
    return tuple(i/inch for i in tupl)

# figure and axes parameters
# total width is fixed, for one column plot

## manuscript
#plot_width    = 9.0
#margin_left   = 1.5
#margin_right  = 0.1
#margin_bottom = 1.2
#margin_top    = 0.2
#space_width   = 1.0
#space_height  = 0.5
#ftsize        = 9

# slides
plot_width    = 8.0
margin_left   = 2.2
margin_right  = 0.4
margin_bottom = 1.8
margin_top    = 0.1
space_width   = 1.0
space_height  = 0.5
ftsize        = 20

font = {'family':'serif',
        'weight':'normal',
        'size':ftsize}

# use TEX for interpreter
plt.rc('text',usetex=True)
plt.rc('text.latex', preamble=[r'\usepackage{amsmath}',r'\usepackage{bm}'])
# use serif font
plt.rc('font',**font)

num_cols = 1
num_rows = 1

subplot_width = (plot_width
                -margin_left
                -margin_right
                -(num_cols-1)*space_width)/num_cols
subplot_height = subplot_width * 1.1/0.8

plot_height = (num_rows*subplot_height
              +margin_bottom
              +margin_top
              +(num_rows-1)*space_height)

###############################################################################

mode = 0
filename = 'cut_y0_Mode.{:d}.csv'.format(mode)
# resolution set in paraview
resolution = 1000

data = np.genfromtxt( filename, names = True, delimiter=',' )

U_mag = np.sqrt( np.square(data['U0']) 
                +np.square(data['U1'])
                +np.square(data['U2'])
               )

U_mag = U_mag.reshape((resolution, resolution))

for i in range(3):
    fig, ax = plt.subplots(num_rows,num_cols,
                           figsize=cm2inch(plot_width,plot_height))

    path = Path([[0.0136, 0], 
                 [0.028, 0.04],
                 [0.045, 0.04], 
                 [0.045, 0.08],
                 [-0.045, 0.08],
                 [-0.045, 0.04],
                 [-0.028, 0.04],
                 [-0.0136, 0],
                 [-0.0136, -0.04],
                 [-0.0022, -0.04],
                 [-0.0022, 0],
                 [0.0022, 0],
                 [0.0022, -0.04],
                 [0.0136, -0.04],
                 [0.0136, 0]
                ])

    patch = PathPatch(path, facecolor='none', edgecolor='none')
    
    ax.add_patch(patch)

    ax.imshow(data['U{:d}'.format(i)].reshape((resolution, resolution)),
               extent=[data['Points0'].min(),
                       data['Points0'].max(),
                       data['Points2'].min(), 
                       data['Points2'].max()],
               cmap='seismic',
               origin='lower',
               aspect='auto',
               clip_path=patch,
               clip_on=True,
              )

    ax.set_xticks([-0.04, -0.02, 0., 0.02, 0.04])
    ax.set_yticks(np.linspace(-0.04,0.06,num=6))

    ax.set_xticklabels(np.linspace(-40,40,num=5,dtype=int))
    ax.set_yticklabels(np.linspace(-40,60,num=6,dtype=int))

    ax.set_xlabel('$r\;(\mathrm{mm})$')
    ax.set_ylabel('$z\;(\mathrm{mm})$')

    fig.subplots_adjust(
            left = margin_left/plot_width,
            bottom = margin_bottom/plot_height,
            right = 1.0-margin_right/plot_width,
            top = 1.0-margin_top/plot_height,
            wspace = space_width/subplot_width,
            hspace = space_height/subplot_height
            )

    fig.savefig('fig_POD_mode{0:d}_y0_U{1:d}.eps'.format(mode,i))
    fig.savefig('fig_POD_mode{0:d}_y0_U{1:d}.png'.format(mode,i))

    plt.close()
