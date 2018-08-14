import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

# cm inch transfer for matplotlib
def cm2inch(*tupl):
    inch = 2.54
    return tuple(i/inch for i in tupl)

filename = 'POD_coef.csv'
data = np.genfromtxt(filename, delimiter=',', names=True)
num_snapshots = data.size

# figure and axes parameters
# total width is fixed, for one column plot
plot_width    = 9.0
margin_left   = 1.5
margin_right  = 0.1
margin_bottom = 1.2
margin_top    = 0.2
space_width   = 3.5
space_height  = 0.5
ftsize        = 9

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


# plot against tmix
fig, ax = plt.subplots(num_rows,num_cols,
figsize=cm2inch(plot_width,plot_height))

ax.scatter(data['V0']*np.sqrt(num_snapshots),
           data['V1']*np.sqrt(num_snapshots),
           s=4, c='k'
          )

circle = plt.Circle((0,0), np.sqrt(2), color='r', fill=False)
ax.add_artist(circle)

ax.set_xlim(-2,2)
ax.set_xticks(np.linspace(-2,2,num=5))
ax.set_ylim(-2,2)
ax.set_yticks(np.linspace(-2,2,num=5))

ax.set_xlabel(r'$a_1/\sqrt{\lambda_1}$')
ax.set_ylabel(r'$a_2/\sqrt{\lambda_2}$')

fig.subplots_adjust(
        left = margin_left/plot_width,
        bottom = margin_bottom/plot_height,
        right = 1.0-margin_right/plot_width,
        top = 1.0-margin_top/plot_height,
        wspace = space_width/subplot_width,
        hspace = space_height/subplot_height
        )

fig.savefig('fig_POD_modal_amplitude.eps')
fig.savefig('fig_POD_modal_amplitude.pdf')
