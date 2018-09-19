import numpy as np
import matplotlib as mpl
#mpl.use('Agg')
import matplotlib.pyplot as plt
import mpl_toolkits.axisartist as axisartist
from scipy import signal

# cm inch transfer for matplotlib
def cm2inch(*tupl):
    inch = 2.54
    return tuple(i/inch for i in tupl)

# figure and axes parameters
# total width is fixed, for one column plot

## for manuscript
#plot_width    = 9.0
#margin_left   = 1.5
#margin_right  = 0.1
#margin_bottom = 1.2
#margin_top    = 0.2
#space_width   = 1.0
#space_height  = 0.5
#ftsize        = 9

# for slides
plot_width    = 10.0
margin_left   = 2.5
margin_right  = 0.1
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
subplot_height = subplot_width * 0.8

plot_height = (num_rows*subplot_height
              +margin_bottom
              +margin_top
              +(num_rows-1)*space_height)

D = 4.4/1000
U = 8.76
F_sample = 5000

filename = 'POD_coef.csv'
data = np.genfromtxt( filename, names=True, delimiter=',' )

num_mode = len(data.dtype) - 2
num_snapshots = data.size

for i in range(num_mode):
    fig, ax = plt.subplots(num_rows,num_cols,
                           figsize=cm2inch(plot_width,plot_height))

    f, d = signal.welch(data['V{:d}'.format(i)]*data['sigma'][i],
                        fs=F_sample,
                        nperseg=512
                       )

    ax.plot( f*D/U, d, 'k-', lw=1 )

    ax.set_yscale('log')
    ax.set_ylim(1.e-3, 4.e5)
    yticks = np.logspace(-3,5,num=9)
    ax.set_yticks(yticks)
    #ax.set_yticklabels(yticks, ha='left', va='center')

    ax.set_xlim(0,2500*D/U)

    ax.set_xlabel('St')
    ax.set_ylabel('PSD')

    fig.subplots_adjust(
            left = margin_left/plot_width,
            bottom = margin_bottom/plot_height,
            right = 1.0-margin_right/plot_width,
            top = 1.0-margin_top/plot_height,
            wspace = space_width/subplot_width,
            hspace = space_height/subplot_height
            )

    fig.savefig('fig_POD_PSD_mode{:d}.eps'.format(i))
    fig.savefig('fig_POD_PSD_mode{:d}.png'.format(i))

    plt.close()
