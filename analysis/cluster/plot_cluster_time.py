import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np


R = 6
ratio = 48
A = -90

separation = 5

case = f'R{R}_ratio{ratio}_A{abs(A)}'
path = f'/home/luis/md-projects/analysis/cluster/R{R}_ratio{ratio}_A{abs(A)}/'
# dir_out = '/'.join([path, 'fig'])
#
# if not os.path.isdir(dir_out):
#     os.mkdir(dir_out)

num_cluster = {}
num_main = {}
num_satellite = {}
num_drops = {}


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

    satellite = df[df['radius'] < separation]
    main = df[df['radius'] > separation]
    #
    # satellite = satellite.multiply(1/(30*1810))
    # main = main.multiply(1/(30*1810))

    print(df.shape)
    num_cluster[name] = df.shape[0] / (30 * 1810)
    num_drops[name] = df.shape[0]  / (30 * 1810)
    num_main[name] = main.shape[0] / (30 * 1810)
    num_satellite[name] = satellite.shape[0] / (30 * 1810)
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
plt.suptitle(f'R={R}; ratio={ratio}; A={A}')

ax1 = plt.subplot(2,1,1)
plt.xlim(200, 350)
plt.ylabel('Clusters Density')
plt.plot(x, y1, 'k-', label=r'Total, any $\kappa^2$')
plt.plot(x, y3, 'k--', label=r'Satellite, $\kappa^2 < 0.2$')
plt.plot(x, y4, 'b-.', label=r'Main, $\kappa^2 < 0.2$')
plt.grid(True)
plt.legend(loc='upper left', prop={'size': 8.5})
# plt.plot(max_snap2, max(num_drops.values()), 'ko')
# plt.plot(max_snap1, max(num_cluster.values()), 'ko')

print()
print('PERCENT: ', max(num_satellite.values())/max(num_main.values()))

ax2 = plt.subplot(2,1,2, sharex=ax1)

def catch(func, *args, handle=lambda e : e, **kwargs):
    try:
        return func(*args, **kwargs)
    except:
        return None

p1 = [catch(lambda : 100*d/c) for c,d in zip(y2,y4)]
p2 = [catch(lambda : 100*d/c) for c,d in zip(y2,y3)]

plt.xlabel('Snapshot')
plt.ylabel('% of Valid Droplets')
plt.plot(x, p2, 'k--', label='Satellite')
plt.plot(x, p1, 'b-.', label='Main')
plt.legend(loc='center left', prop={'size': 9})
plt.grid(True)

# plt.savefig(f'{case}.png', format='png')
# plt.close()
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
