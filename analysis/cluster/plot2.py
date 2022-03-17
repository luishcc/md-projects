import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


R = 6
ratio = 48
A = -50

case = f'R{R}_ratio{ratio}_A{abs(A)}'
path = f'/home/luishcc/md-projects/analysis/cluster/R{R}_ratio{ratio}_A{abs(A)}/'
dir_out = '/'.join([path, 'fig'])

if not os.path.isdir(dir_out):
    os.mkdir(dir_out)

for file in os.scandir(path):

    name = file.name.split('.')[0]

    try:
        df = pd.read_csv(file.path)
    except:
        continue

    print(df.shape)

    df.drop(df[df['size'] <= 1].index, inplace=True)
    # df.drop(df[df['radius'] > 5].index, inplace=True)
    # df.drop(df[df['size'] > 1000].index, inplace=True)
    df.drop(df[df['anisotropy'] > 0.2].index, inplace=True)
    # df.drop(df[df['asphericity'] > 3].index, inplace=True)

    # Radius of Gyration to sphere:
    df['radius'] = df['radius'].multiply(np.sqrt(5/3))

    print(df.shape)
    print()

    plt.figure(1)

    try:
        # df['radius'].plot(marker='.', linestyle='none')
        df['radius'].plot.kde(bw_method=0.1)
        # df['size'].plot.kde(bw_method=0.01)
        df['radius'].plot.hist(bins=50, alpha=0.5, density=True)
        # df['size'].plot.hist(bins=50, alpha=0.5)
        # df['anisotropy'].plot.hist(bins=50, alpha=0.5)
        # df['asphericity'].plot.hist(bins=20, alpha=0.5)
        # df['acylindricity'].plot.hist(bins=20, alpha=0.5)
    except:
        open(f'{dir_out}/{name}.png', 'w').close()
        continue

    plt.title(f'Droplet Size Distribution, A={A}, snapshot={name}')
    plt.xlim(0, 15)
    plt.ylim(0, 0.5)
    plt.xlabel('Radius')
    plt.ylabel('Density')
    plt.grid(True)
    plt.savefig(f'{dir_out}/{name}.png', format='png')
    plt.close(1)
    # plt.show()






#
