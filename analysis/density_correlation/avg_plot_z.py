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
    'figure.figsize': (1.*side, 1.*side),
    "text.usetex": True
    }
mpl.rcParams.update(rc_fonts)

path_to_data = '/home/luishcc/hdd/free_thread_old/'
# path_to_data = '/home/luishcc/hdd/free_thread_new/'
# path_to_data = '/home/luishcc/hdd/'


def get_snap(dir, exact=True):
    try:
        with open(dir+'/breaktime.txt', 'r') as fd:
            snap = int(fd.readline())
    except:
        return None
    return snap

R = 6
ratio = 48
A = 40

grid = 1

ini = 1
end = 30


data_case_dir = f'R{R}_ratio{ratio}_A{A}/1'
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
    n += 1
    data_case_dir = f'R{R}_ratio{ratio}_A{A}/{n}'
    dir = path_to_data + data_case_dir
    datafile = '/'.join([dir,file])
    snap = get_snap(dir)


avg = sum/(n-1)
var = sumsq/(n-1) - avg**2


from mpl_toolkits.axes_grid1.inset_locator import (inset_axes, InsetPosition,
                                                  mark_inset)

fig, axs = plt.subplots(1,1, sharey=True)

# fig.subplots_adjust(wspace=.3)
# ax = axs[0]
# ax2 = axs[1]

ax=axs
ax2=axs

ax.plot(xx[1:],avg[1:], 'k-', linewidth=1.5, label=r'Oh $=0.199$')
ax.errorbar(xx[1:], avg[1:], yerr = np.sqrt(var[1:])/2,
 linewidth=1., fmt='o',ecolor = 'black',markersize=5, color='black',
 markerfacecolor='none', capsize=2, capthick=0.4)

ax.set_xlim(0,0.08)

ax.set_ylabel(r'$\hat{G}(r,q)$')
ax.set_xlabel(r'$q$')

R = 6
ratio = 48
A = 90

grid = 1



data_case_dir = f'R{R}_ratio{ratio}_A{A}/1'
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
    n += 1
    data_case_dir = f'R{R}_ratio{ratio}_A{A}/{n}'
    dir = path_to_data + data_case_dir
    datafile = '/'.join([dir,file])
    snap = get_snap(dir)


avg = sum/(n-1)
var = sumsq/(n-1) - avg**2


ax2.plot(xx[1:],avg[1:], 'b--', linewidth=1.5, label=r'Oh $=1.137$')
ax2.errorbar(xx[1:], avg[1:], yerr = np.sqrt(var[1:])/2,
linewidth=1., fmt='s',ecolor ='blue',markersize=5, color='blue', markerfacecolor='none', capsize=2, capthick=0.4)
ax2.set_xlabel(r'$q$')

ax2.set_xlim(0,0.08)

ax.legend(frameon=False)
ax2.legend(frameon=False)


plt.show()

#
# with open(f'R{R}_ratio{ratio}_A{A}-peak.csv', 'w') as fd:
#     fd.write('peak_avg,variance\n')
#     fd.write(f'{popt[0]},{popt[1]}')
