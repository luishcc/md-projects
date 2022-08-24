import os
import numpy as np
from scipy.fft import rfft, rfftfreq

import matplotlib as mpl

dpi = 1600
side = 7
rc_fonts = {
    "font.family": "serif",
    "font.size": 12,
    'figure.figsize': (0.8*side, side),
    "text.usetex": True
    }
mpl.rcParams.update(rc_fonts)

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid.inset_locator import (inset_axes, InsetPosition,
                                                  mark_inset)
from mdpkg.rwfile import read_dat


def func(x):
    b = x*np.sqrt(18)
    a = 1/(2+b)
    return np.sqrt(a)
oh_data = [0.266,0.321,0.451,0.704,0.901,1.137]

def get_snap(dir):
    try:
        with open(dir+'/breaktime.txt', 'r') as fd:
            snap = int(fd.readline())
    except:
        return None
    return snap


# r6 = [0.017699, 0.019868, 0.015957, 0.017699,
#         0.018939, 0.019933, 0.017699, 0.018785, 0.01657]
# xr6 = [226, 301, 376, 452, 527, 603, 904, 1809, 1809]


r6 = [0.017699, 0.018868, 0.016257, 0.017699,
        0.018339, 0.019133, 0.017699, 0.017685]

r6 = [0.017699, 0.018868, 0.017699,
        0.018339, 0.017699, 0.017685]

# r6 = [0.017699, 0.019868, 0.015957, 0.017699,
#         0.018939, 0.019933, 0.017699, 0.017685]

# xr6 = [226, 301, 376, 452, 527, 603, 904, 1809]
#xr6 = [226, 301,  452, 527,  904, 1809]
xr6 = [226, 452, 904, 1809]


r8 = [0.013245, 0.013289, 0.013267]
xr8 = [301, 603, 1206]
xr8 = [301, 603, 1206, None]

r10 = [0.010638, 0.010610]
r10 = [0.010638, 0.010610]
xr10 = [376, 753]
xr10 = [376, 753, None, None]

xrr = [xr6, xr8, xr10]

#xr6 = [l/(2*np.pi*6) for l in xr6]
#xr8 = [l/(2*np.pi*8) for l in xr8]
#xr10 = [l/(2*np.pi*10) for l in xr10]


R = 6
ratio = 48

A = 50
grid = 1


n=0

path_to_data = '/home/luishcc/hdd/free_thread_results/'
path_to_data2 = '/home/luishcc/Desktop/'

data_case_dir = f'R{R}_ratio{ratio}_A{A}-{n+1}'
dir = path_to_data + data_case_dir

snap = get_snap(dir)

file = f'correlation_grid1/{snap}.dat'
datafile = '/'.join([dir,file])


data = read_dat(datafile)
x = data['dz']


num = len(x)
if num % 2 == 0:
    row = int((num / 2) + 1)
else:
    row = int((num + 1) / 2)

xx = rfftfreq(num)

plot_interval = [i for i in range(4,7)]

sum_f = np.zeros((row, len(plot_interval)))
sumsq_f = np.zeros((row, len(plot_interval)))
sum_c = np.zeros((num, len(plot_interval)))
sumsq_c = np.zeros((num, len(plot_interval)))


#############################################


n = 0
while os.path.isfile(datafile):
    print(datafile)
    data = read_dat(datafile)
    for id, val in enumerate(plot_interval):
        arr_real = np.array(data[f'{val}'])
        arr = abs(rfft(arr_real))
        sum_f[:,id] += arr
        sumsq_f[:,id] += arr**2
        sum_c[:,id] += arr_real
        sumsq_c[:,id] += arr_real**2
    n += 1
    data_case_dir = f'R{R}_ratio{ratio}_A{A}-{n+1}'
    dir = path_to_data + data_case_dir
    snap = get_snap(dir)
    file = f'correlation_grid1/{snap}.dat'
    datafile = '/'.join([dir,file])

avg_c = sum_c/n
var_c = sumsq_c/n - avg_c**2

avg_f = sum_f/n
var_f = sumsq_f/n - avg_f**2

#################################################################

# r=5.7
r=4.8
#r=6

r = [4.8]*6
ri = [4.8, 4.8, 4.7, 4.7, 4.6, 4.4]

#ri=r




#################################################

fig, [ax1, ax] = plt.subplots(2,1, gridspec_kw={'height_ratios': [2, 1]})

ax2 = plt.axes([0,0,1,1])
ip = InsetPosition(ax1, [0.5,0.42,0.45,0.4])
ax2.set_axes_locator(ip)
# mark_inset(ax1, ax2, loc1=2, loc2=4, fc="none", ec='0.5')

skip_f = 3
plot_symbols = ['ko-', 'bs-', 'gv-' ]
plot_style = ['-', '--', '-.']
plot_colors =  ['k-', 'b-', 'g-' ]
plot_colors2 =  ['k', 'b', 'g' ]
plot_markers = ['o', 's', 'v']
for i in range(len(plot_interval)):
    ax2.plot([xi/1809 for xi in x], avg_c[:, i], plot_colors[i], label=f'$r={plot_interval[i]}$', linestyle=plot_style[i], linewidth=1.5)
    ax1.plot(xx[skip_f:], avg_f[skip_f:, i],  plot_colors[i], label=f'$r={plot_interval[i]}$' ,  markerfacecolor='none', linestyle=plot_style[i], linewidth=1.5)

ax1.legend(loc='upper right', ncol=3)
#ax2.legend(loc='upper right', ncol=3)


ax1.set_ylim(0,16)
ax1.set_xlim(0.003,0.12)
ax1.set_xlabel(r'$q$')
ax1.set_ylabel(r'$\hat{G}(r,q)$')

# ax2.set_ylim(0.3,0.8)
ax2.set_xlim(0,0.2)
ax2.set_xlabel(r'$\delta z/L$')
ax2.set_ylabel(r'$G(r,\delta z)$')


red = np.array([6,8,10]) * 2*np.pi *0.88
# red = [1,1,1]

ax.set_ylabel(r'$\chi$')

R = [6, 8, 10]
ratio = [6, 12, 24, 48]

A = 50
scale_r = 0.8



for iter1, r in enumerate(R):
    q = []
    q_var = []
    x_plot = []
    for iter2, rat in enumerate(ratio):
        file = path_to_data2 + f'R{r}_ratio{rat}_A{50}-peak.csv'
        print(file)
        try:
            with open(file, 'r') as fd:
                fd.readline()
                line = fd.readline().split(',')
                q.append(float(line[0]) * 2 * np.pi * r * scale_r)
                q_var.append(float(line[1]) * ( 2 * np.pi * r * scale_r)**2)
#                x_plot.append(rat)
                x_plot.append(xrr[iter1][iter2])
        except:
            continue
    print(xrr[iter1], q, q_var)

    ax.errorbar(x_plot, q, yerr = np.sqrt(q_var), fmt=plot_markers[iter1],ecolor = 'black' ,markersize=6.5, color=plot_colors2[iter1], capsize= 2, capthick=1, label=f'$R_0={r}$',
    markerfacecolor='none')

ax.plot([180,1850], [func(oh_data[0])]*2, color='black', linestyle='--', label='Theory')

#ax.plot(x_plot, [i*red[0] for i in r6], 'ko--', markersize=7.5, markerfacecolor='none', label=r'$R_0=6$')


#ax.plot(xr8, [i*red[1] for i in r8], 'bx--', markersize=9.5, markerfacecolor='none',label=r'$R_0=8$')
#ax.plot(xr10, [i*red[2] for i in r10], 'gs--', markersize=8.5, markerfacecolor='none',label=r'$R_0=10$')

ax.set_ylim(0.3,0.76)
#ax.legend(loc=(0.55, 0.05), ncol=3)
ax.legend(loc='lower right', ncol=2)
ax.set_xlabel(r'$L$ $[r_c]$' )

# Some ad hoc tweaks.


# ax2.set_yticks(np.arange(0,2,0.4))
# ax2.set_xticklabels(ax2.get_xticks(), backgroundcolor='w')
# ax2.tick_params(axis='x', which='major', pad=8)


plt.savefig('fig2.pdf', bbox_inches='tight', dpi=dpi )

plt.show()


##############################################
exit()

scale_x = 1
scale_y = 1
ticks_x = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x / scale_x))
ticks_y = ticker.FuncFormatter(lambda y, pos: '{0:g}'.format(y / scale_y))
ax3.xaxis.set_minor_locator(AutoMinorLocator())
ax3.yaxis.set_minor_locator(AutoMinorLocator())
ax3.xaxis.set_major_formatter(ticks_x)
ax3.yaxis.set_major_formatter(ticks_y)
ax3.yaxis.set_ticks_position('both')
ax3.xaxis.set_ticks_position('both')
ax3.tick_params(which='minor', direction='in')
