from scipy.fft import rfft, rfftfreq
import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np
# from mdpkg.rwfile import read_dat
import matplotlib as mpl


dpi = 1600
side = 7
rc_fonts = {
    "font.family": "serif",
    "font.size": 12,
    'figure.figsize': (1.6*side, .8*side),
    "text.usetex": True
    }
mpl.rcParams.update(rc_fonts)

# path_to_data = '/home/luishcc/hdd/free_thread_old/'
path_to_data = '/home/luishcc/hdd/surfactant/'
# path_to_data = '/home/luishcc/hdd/free_thread_new/'
# path_to_data = '/home/luishcc/hdd/'


def get_snap(dir, exact=True):
    try:
        with open(dir+'/breaktime.txt', 'r') as fd:
            snap = int(fd.readline())
    except:
        return None
    return snap

R = 8
ratio = 24
A = 50

surf_con = 2.3

grid = 1

ini = 1
end = 30


# data_case_dir = f'R{R}_ratio{ratio}_A{A}/1'
data_case_dir = f'R{R}-{surf_con}/1'
dir = path_to_data + data_case_dir

snap = get_snap(dir)

file = f'breaktime_correlation_grid{grid}.dat'
datafile = '/'.join([dir,file])

data = pd.read_csv(datafile,  sep=' ', header=0, names=['dz', 'correlation', 'nan'])
x = data['dz'].tolist()

num = len(x)
if num % 2 == 0:
    row = int((num / 2) + 1)
else:
    row = int((num + 1) / 2)

xx = rfftfreq(num)

sum_real = np.zeros(len(x))
sumsq_real = np.zeros(len(x))
sum = np.zeros(row)
sumsq = np.zeros(row)

###############


n = 1
while os.path.isfile(datafile):
    print(snap)
    print(datafile)
    data = pd.read_csv(datafile, sep=' ', header=0, names=['dz', 'correlation', 'nan'])
    # data = pd.read_dat(datafile)

    arr_real = np.array(data['correlation'].tolist())
    arr = abs(rfft(arr_real))

    sum += arr
    sumsq += arr**2

    sum_real += arr_real
    sumsq_real += arr_real**2

    n += 1


    # data_case_dir = f'R{R}_ratio{ratio}_A{A}/{n}'
    data_case_dir = f'R{R}-{surf_con}/{n}'
    dir = path_to_data + data_case_dir
    datafile = '/'.join([dir,file])
    snap = get_snap(dir)

avg = sum/(n-1)
var = sumsq/(n-1) - avg**2

avg_real = sum_real/(n-1)
var_real = sumsq_real/(n-1) - avg_real**2


from mpl_toolkits.axes_grid1.inset_locator import (inset_axes, InsetPosition,
                                                  mark_inset)

fig, axs = plt.subplots(1,2, sharey=False)

# fig.subplots_adjust(wspace=.3)
ax = axs[0]
ax2 = axs[1]

ax.errorbar(x, avg_real, yerr = np.sqrt(var_real),
 linewidth=.3, fmt=' ',ecolor = 'black',markersize=1, color='black',
 markerfacecolor='none', capsize=.3, capthick=.3)
ax.plot(x,avg_real, 'b-', linewidth=2.5, label=r'Oh $=0.199$')

# ax.set_xlim(0,0.08)

ax2.set_ylabel(r'$\hat{G}(r,q)$')
ax.set_ylabel(r'${G}(r,\delta_z)$')
ax.set_xlabel(r'$\delta_z$')


ax2.plot(xx[ini:end],avg[ini:end], 'b-', linewidth=1.5, label=r'Oh $=1.137$')
ax2.errorbar(xx[ini:end], avg[ini:end], yerr = np.sqrt(var[ini:end])/2,
linewidth=1., fmt='s',ecolor ='blue',markersize=5, color='blue', markerfacecolor='none', capsize=2, capthick=0.4)
ax2.set_xlabel(r'$q$')

ax2.set_xlim(0,0.08)

# ax.legend(frameon=False)
# ax2.legend(frameon=False)


plt.show()

#
# with open(f'R{R}_ratio{ratio}_A{A}-peak.csv', 'w') as fd:
#     fd.write('peak_avg,variance\n')
#     fd.write(f'{popt[0]},{popt[1]}')
