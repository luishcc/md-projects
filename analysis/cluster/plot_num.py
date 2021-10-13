import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np


R = 6
ratio = 48
A = -50

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

plt.figure()

ax1 = plt.subplot(2,1,1)
plt.ylabel('Number of Clusters')
plt.plot(x, y1, 'k-', label='Unfiltered')
plt.plot(x, y2, 'b-', label='Filtered')
plt.grid(True)
plt.legend(loc='lower right')
plt.plot(int(max(num_drops, key=num_drops.get)), max(num_drops.values()), 'bo')
plt.plot(int(max(num_cluster, key=num_cluster.get)), max(num_cluster.values()), 'ko')

ax2 = plt.subplot(2,1,2, sharex=ax1)
plt.xlabel('Snapshot')
plt.ylabel('% of Valid Clusters')
plt.plot(x, [100*d/c for c,d in zip(y1,y2)])
plt.grid(True)

plt.savefig(f'{name}.png', format='png')
# plt.show()





#
