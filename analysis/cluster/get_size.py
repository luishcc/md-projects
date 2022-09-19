import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy import stats


R = 6
ratio = 48
A = -80

snap = 71

case = f'R{R}_ratio{ratio}_A{abs(A)}'
path = f'/home/luis/md-projects/analysis/cluster/R{R}_ratio{ratio}_A{abs(A)}/'

path = f'/home/luis/md-projects/analysis/cluster/break_avg/R{R}_ratio{ratio}_A{abs(A)}/'


file = path + f'{snap}.csv'




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
data = df['radius'].plot.kde(bw_method=0.1).get_lines()[0].get_xydata()

main = df.drop(df[df['radius'] < 5].index)
satellite = df.drop(df[df['radius'] > 5].index)

data = data.swapaxes(0,1)

for i,d in enumerate(data[0]):
    if d > 5:
        sep_id = i
        break

print(data[0][np.argmax(data[1][:sep_id])])
print(data[0][np.argmax(data[1][sep_id:])+sep_id])

plt.title(f'Droplet Size Distribution, A={A}, snapshot={snap}')
plt.xlim(0, 15)
plt.ylim(0, 0.8)
plt.xlabel('Radius')
plt.ylabel('Density')
plt.grid(True)
plt.show()
plt.close(1)






#
