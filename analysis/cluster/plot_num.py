import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np


R = 6
ratio = 48
A = -90

case = f'R{R}_ratio{ratio}_A{abs(A)}'
path = f'/home/luishcc/md-projects/analysis/cluster/R{R}_ratio{ratio}_A{abs(A)}/'
# dir_out = '/'.join([path, 'fig'])
#
# if not os.path.isdir(dir_out):
#     os.mkdir(dir_out)

num_cluster = {}
num_drops = {}

for file in os.scandir(path):


    try:
        df = pd.read_csv(file.path)
    except:
        continue
    name = int(file.name.split('.')[0])

    print(df.shape)
    num_cluster[name] = df.shape[0]

    df.drop(df[df['size'] <= 1].index, inplace=True)
    # df.drop(df[df['radius'] > 5].index, inplace=True)
    # df.drop(df[df['size'] > 1000].index, inplace=True)
    df.drop(df[df['anisotropy'] > 0.2].index, inplace=True)
    # df.drop(df[df['asphericity'] > 3].index, inplace=True)

    print(df.shape)
    num_drops[name] = df.shape[0]
    print()


list1 = sorted(num_cluster.items())
list2 = sorted(num_drops.items())

x1, y1 = zip(*list1)
x2, y2 = zip(*list2)
x = np.linspace(int(x1[0]), int(x1[-1]), len(y2))

max_snap1 = max(num_drops, key=num_cluster.get)
max_snap2 = max(num_drops, key=num_drops.get)

plt.figure(1)
plt.suptitle(f'R={R}; ratio={ratio}; A={A}')

ax1 = plt.subplot(2,1,1)
plt.xlim(100, 400)
plt.ylabel('Number of Clusters')
plt.plot(x, y1, 'k-', label='Unfiltered')
plt.plot(x, y2, 'b-', label='Filtered')
plt.grid(True)
plt.legend(loc='lower right')
plt.plot(max_snap2, max(num_drops.values()), 'bo')
plt.plot(max_snap1, max(num_cluster.values()), 'ko')

ax2 = plt.subplot(2,1,2, sharex=ax1)
plt.xlabel('Snapshot')
plt.ylabel('% of Valid Clusters')
plt.plot(x, [100*d/c for c,d in zip(y1,y2)])
plt.grid(True)

plt.savefig(f'{case}.png', format='png')
plt.close()
# plt.show()

plt.figure(2)
df = pd.read_csv(path+f'{max_snap2}.csv')
df.drop(df[df['size'] <= 1].index, inplace=True)
df.drop(df[df['anisotropy'] > 0.2].index, inplace=True)
df['radius'].plot.hist(bins=50, alpha=0.5)
plt.title(f'Droplet Size Distribution, A={A}, snapshot={max_snap2}')
# plt.xlim(0, 15)
# plt.ylim(0, 60)
plt.xlabel('Radius')
plt.grid(True)
plt.savefig(f'{case}_Dist.png', format='png')
plt.show()

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
