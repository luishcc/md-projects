import pandas as pd
import matplotlib.pyplot as plt


file = '/home/luishcc/md-projects/analysis/cluster/R6_ratio48_A50/200.csv'
# file = 'a.csv'


df = pd.read_csv(file)

df.drop(df[df['size'] < 10].index, inplace=True)

# df['radius'].plot()
# df['radius'].plot.kde(bw_method=0.2)
df['radius'].plot.hist(bins=20, alpha=0.5)
plt.show()
