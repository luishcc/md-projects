import pandas as pd
import matplotlib.pyplot as plt



A = -50
snap = 50
file = f'/home/luishcc/md-projects/analysis/cluster/R6_ratio48_A{abs(A)}/{snap}.csv'
# file = 'a.csv'


df = pd.read_csv(file)

df.drop(df[df['size'] <= 1].index, inplace=True)
df.drop(df[df['radius'] > 20].index, inplace=True)
df.drop(df[df['anisotropy'] > 0.1].index, inplace=True)
# df.drop(df[df['asphericity'] > 3].index, inplace=True)


# df['radius'].plot()
df['radius'].plot.kde(bw_method=0.1)
# df['size'].plot.kde(bw_method=0.01)
# df['radius'].plot.hist(bins=20, alpha=0.5)
# df['anisotropy'].plot.hist(bins=20, alpha=0.5)
# df['asphericity'].plot.hist(bins=20, alpha=0.5)
# df['acylindricity'].plot.hist(bins=20, alpha=0.5)

plt.title(f'Droplet Size Distribution, A={A}, snapshot={snap}')
# plt.xlim(0, 4)
# plt.ylim(0, 0.28)
plt.xlabel('Radius')
plt.grid(True)
plt.show()
