import os

import pandas as pd
import numpy as np
from scipy import stats

import matplotlib as mpl
import matplotlib.pyplot as plt
dpi = 1600
side = 7
rc_fonts = {
    "font.family": "serif",
    "font.size": 12,
    'figure.figsize': (0.8*side, 0.6*side),
    "text.usetex": True
    }
mpl.rcParams.update(rc_fonts)


R = 4
ratio = 48
A = -90


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
# path = f'/home/luishcc/md-projects/analysis/cluster/break-avg/R{R}_ratio{ratio}_A{abs(A)}'



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
    df.drop(df[df['anisotropy'] > 0.2].index, inplace=True)
    df['radius'] = df['radius'].multiply(np.sqrt(5/3))

    satellite = df[df['radius'] < separation]
    main = df[df['radius'] > separation]

    print(df.shape)

    num_main[name] = main.shape[0] / (30 * 2*np.pi*R*0.8)

snap = max(num_main, key=num_main.get)


file = path + f'/{snap}.csv'

df = pd.read_csv(file)

print(df.shape)

df.drop(df[df['size'] <= 1].index, inplace=True)
df.drop(df[df['anisotropy'] > 0.2].index, inplace=True)

# Radius of Gyration to sphere:
df['radius'] = df['radius'].multiply(np.sqrt(5/3))

print(df.shape)

plt.figure(1)

# df['radius'].plot.kde(bw_method=0.1)
df['radius'].plot.hist(bins=50, alpha=0.5, density=True)
data = df['radius'].plot.kde(bw_method=0.2).get_lines()[0].get_xydata()

main = df.drop(df[df['radius'] < separation].index)
satellite = df.drop(df[df['radius'] > separation].index)

data = data.swapaxes(0,1)

for i,d in enumerate(data[0]):
    if d > separation:
        sep_id = i
        break

print(data[0][np.argmax(data[1][:sep_id])])
print(data[0][np.argmax(data[1][sep_id:])+sep_id])

plt.title(f'Droplet Size Distribution, A={A}, snapshot={snap}')
plt.xlim(0, 10)
# plt.ylim(0, 0.7)
plt.xlabel('Radius')
plt.ylabel('Density')
plt.grid(True)
plt.show()
plt.close(1)






#
