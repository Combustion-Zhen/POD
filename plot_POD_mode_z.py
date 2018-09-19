import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as patches

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
plot_width    = 9.0
margin_left   = 2.2
margin_right  = 0.4
margin_bottom = 1.8
margin_top    = 0.2
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
subplot_height = subplot_width * 1.0

plot_height = (num_rows*subplot_height
              +margin_bottom
              +margin_top
              +(num_rows-1)*space_height)

###############################################################################

mode = 1
# resolution set in paraview
resolution = 1000

for z in np.arange(-35.,60.,10.):
    filename = 'cut_z{0:g}_Mode.{1:d}.csv'.format(z,mode)

    data = np.genfromtxt( filename, names = True, delimiter=',' )

    for i in range(3):
        fig, ax = plt.subplots(num_rows,num_cols,
                               figsize=cm2inch(plot_width,plot_height))

        if z < 40 and z > 0:
            r = (13.6+14.4*z/40)/1000
        elif z >= 40:
            r = 0.04
        else:
            r = 0.0136

        patch = patches.Circle((0,0), radius=r, facecolor='none')
        
        ax.add_patch(patch)

        ax.imshow(data['U{:d}'.format(i)].reshape((resolution, resolution)),
                   extent=[data['Points0'].min(),
                           data['Points0'].max(),
                           data['Points1'].min(), 
                           data['Points1'].max()],
                   cmap='seismic',
                   origin='lower',
                   aspect='auto',
                   clip_path=patch,
                   clip_on=True,
                  )

        if r < 0:
            circle = plt.Circle((0,0), 0.0022, color='w')
            ax.add_artist(circle)

        ax.set_xticks(np.linspace(-0.04,0.04,num=5))
        ax.set_yticks(np.linspace(-0.04,0.04,num=5))

        ax.set_xticklabels(np.linspace(-40,40,num=5,dtype=int))
        ax.set_yticklabels(np.linspace(-40,40,num=5,dtype=int))

        ax.set_xlabel('$x\;(\mathrm{mm})$')
        ax.set_ylabel('$y\;(\mathrm{mm})$')

        fig.subplots_adjust(
                left = margin_left/plot_width,
                bottom = margin_bottom/plot_height,
                right = 1.0-margin_right/plot_width,
                top = 1.0-margin_top/plot_height,
                wspace = space_width/subplot_width,
                hspace = space_height/subplot_height
                )

        fig.savefig('fig_POD_mode{0:d}_z{1:d}_U{2:d}.eps'.format(mode,int(z),i))
        fig.savefig('fig_POD_mode{0:d}_z{1:d}_U{2:d}.png'.format(mode,int(z),i))

        plt.close()
