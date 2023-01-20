import pandas as pd
import matplotlib as mpl

dpi = 1600
side = 7
rc_fonts = {
    "font.family": "serif",
    "font.size": 12,
    'figure.figsize': (0.8*side, 0.6*side),
    "text.usetex": True
    }
mpl.rcParams.update(rc_fonts)

import matplotlib.pyplot as plt
import os
import numpy as np


R = 6
ratio = 48
A = -70


if R == 2:
    separation = 1.7
elif R == 4:
    separation = 2.5
elif R == 6:
    separation = 4
elif R == 8:
    separation = 5.5
elif R == 10:
    separation = 7


case = f'R{R}_ratio{ratio}_A{abs(A)}'
# path = f'/home/luishcc/md-projects/analysis/cluster/R{R}_ratio{ratio}_A{abs(A)}/'
path = f'/home/luishcc/md-projects/analysis/cluster/break-avg/R{R}_ratio{ratio}_A{abs(A)}'

# dir_out = '/'.join([path, 'fig'])
#
# if not os.path.isdir(dir_out):
#     os.mkdir(dir_out)

num_cluster = {}
num_main = {}
num_satellite = {}
num_drops = {}

num_cluster2 = {}
num_main2 = {}
num_satellite2 = {}
num_drops2 = {}

for file in os.scandir(path):

    try:
        df = pd.read_csv(file.path)
    except:
        continue
    name = int(file.name.split('.')[0])

    print(df.shape)


    df.drop(df[df['size'] <= 1].index, inplace=True)
    # df.drop(df[df['radius'] > 5].index, inplace=True)
    # df.drop(df[df['size'] > 1000].index, inplace=True)
    df.drop(df[df['anisotropy'] > 0.2].index, inplace=True)
    # df.drop(df[df['asphericity'] > 3].index, inplace=True)
    df['radius'] = df['radius'].multiply(np.sqrt(5/3))


    satellite = df[df['radius'] < separation]
    main = df[df['radius'] > separation]
    #
    # satellite = satellite.multiply(1/(30*1810))
    # main = main.multiply(1/(30*1810))

    print(df.shape)
    # num_cluster[name] = df.shape[0] / (30 * 1810)
    # num_drops[name] = df.shape[0]  / (30 * 1810)
    # num_main[name] = main.shape[0] / (30 * 1810)
    # num_satellite[name] = satellite.shape[0] / (30 * 1810)

    num_cluster[name] = df.shape[0] / (30 * 2*np.pi*R*0.8)
    num_drops[name] = df.shape[0]  / (30 * 2*np.pi*R*0.8)
    num_main[name] = main.shape[0] / (30 * 2*np.pi*R*0.8)
    num_satellite[name] = satellite.shape[0] / (30 * 2*np.pi*R*0.8)

    num_cluster2[name] = df.shape[0]
    num_drops2[name] = df.shape[0]
    num_main2[name] = main.shape[0]
    num_satellite2[name] = satellite.shape[0]
    print()


list1 = sorted(num_cluster.items())
list2 = sorted(num_drops.items())
list3 = sorted(num_satellite.items())
list4 = sorted(num_main.items())

x1, y1 = zip(*list1)
x2, y2 = zip(*list2)
x3, y3 = zip(*list3)
x4, y4 = zip(*list4)

x = np.linspace(int(x1[0]), int(x1[-1]), len(y2))

max_snap1 = max(num_cluster, key=num_cluster.get)
max_snap2 = max(num_drops, key=num_drops.get)
max_snap3 = max(num_satellite, key=num_satellite.get)
max_snap4 = max(num_main, key=num_main.get)

plt.figure(1)
# plt.suptitle(f'R={R}; ratio={ratio}; A={A}')

ax1 = plt.subplot(1,1,1)
# plt.xlim(200, 350)
plt.ylabel('$<N_{droplets}>/2\pi R_0$')
plt.xlabel(r'$t-t_b$')
# plt.plot(x, y2, 'k-', label=r'Total, $\kappa^2 < 0.2$')
# plt.plot(x, y3, 'k--', label=r'Satellite, $\kappa^2 < 0.2$')
# plt.plot(x, y4, 'b-.', label=r'Main, $\kappa^2 < 0.2$')

plt.plot(x, y2, 'k-', label=r'Total')
plt.plot(x, y3, 'k--', label=r'Satellite')
plt.plot(x, y4, 'b-.', label=r'Main')

plt.scatter(max_snap2, num_drops[max_snap2], color='k')
plt.scatter(max_snap3, num_satellite[max_snap3], color='k')
plt.scatter(max_snap4, num_main[max_snap4], color='k')
# plt.grid(True)
# plt.legend(loc='upper left', prop={'size': 11.})
plt.legend(loc='upper left')
# plt.plot(max_snap2, max(num_drops.values()), 'ko')
# plt.plot(max_snap1, max(num_cluster.values()), 'ko')

print()
print('PERCENT: ', max(num_satellite2.values())/max(num_drops2.values()))
# print('PERCENT: ', num_satellite2[max_snap2]/max(num_drops2.values()))
print(max_snap3, max_snap4)
#
# ax2 = plt.subplot(2,1,2, sharex=ax1)
#
# def catch(func, *args, handle=lambda e : e, **kwargs):
#     try:
#         return func(*args, **kwargs)
#     except:
#         return None
#
# p1 = [catch(lambda : 100*d/c) for c,d in zip(y2,y4)]
# p2 = [catch(lambda : 100*d/c) for c,d in zip(y2,y3)]
#
# plt.xlabel('Snapshot')
# plt.ylabel('% of Valid Droplets')
# plt.plot(x, p2, 'k--', label='Satellite')
# plt.plot(x, p1, 'b-.', label='Main')
# plt.legend(loc='center left', prop={'size': 9})
# plt.grid(True)

# plt.savefig(f'{case}.png', format='png')
# plt.close()
# plt.savefig(f'time.png', transparent=True, dpi=1600)

plt.show()

exit()

plt.figure(2)
ax1 = plt.subplot(2,1,1)
df = pd.read_csv(path+f'{max_snap2}.csv')
df.drop(df[df['size'] <= 1].index, inplace=True)
df.drop(df[df['anisotropy'] > 0.2].index, inplace=True)
df['radius'] = df['radius'] / (np.sqrt(0.6))
# df['radius'].plot.hist(bins=50, alpha=0.5)
df['radius'].plot.kde(bw_method=0.1)
plt.title(f'Droplet Size Distribution, A={A}, snapshot={max_snap2}')
# plt.xlim(0, 15)
# plt.ylim(0, 60)
plt.xlabel('Radius')
plt.ylabel('KDE')
plt.grid(True)

ax2 = plt.subplot(2,1,2, sharex=ax1)
df = pd.read_csv(path+f'{max_snap3}.csv')
df.drop(df[df['size'] <= 1].index, inplace=True)
df.drop(df[df['anisotropy'] > 0.2].index, inplace=True)
df['radius'] = df['radius'] / (np.sqrt(0.6))
# df['radius'].plot.hist(bins=50, alpha=0.5)
df['radius'].plot.kde(bw_method=0.1)
plt.title(f'Droplet Size Distribution, A={A}, snapshot={max_snap3}')
plt.xlim(0, 15)
# plt.ylim(0, 60)
plt.xlabel('Radius')
plt.ylabel('KDE')
plt.grid(True)

# plt.savefig(f'{case}_Dist.png', format='png')
# plt.show()

# scale_x = 1
# scale_y = 1
# ticks_x = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x / scale_x))
# ticks_y = ticker.FuncFormatter(lambda y, pos: '{0:g}'.format(y / scale_y))
# ax3.xaxis.set_minor_locator(AutoMinorLocator())
# ax3.yaxis.set_minor_locator(AutoMinorLocator())
# ax3.xaxis.set_major_formatter(ticks_x)
# ax3.yaxis.set_major_formatter(ticks_y)
# ax3.yaxis.set_ticks_position('both')
# ax3.xaxis.set_ticks_position('both')
# ax3.tick_params(which='minor', direction='in')
