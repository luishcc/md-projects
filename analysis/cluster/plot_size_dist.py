import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy import stats


R = 6
ratio = 48
A = -50

case = f'R{R}_ratio{ratio}_A{abs(A)}'
path = f'/home/luis/md-projects/analysis/cluster/R{R}_ratio{ratio}_A{abs(A)}/'
dir_out = path + 'fig'

if not os.path.isdir(dir_out):
    os.mkdir(dir_out)




for file in os.scandir(path):


    # name = file.name.split('.')[0]

    name = '220.csv'

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
        # df['size'].plot.kde(bw_method=0.01)
        df['radius'].plot.kde(bw_method=0.1)
        df['radius'].plot.hist(bins=50, alpha=0.5, density=True)
        # df['size'].plot.hist(bins=50, alpha=0.5)
        # df['anisotropy'].plot.hist(bins=50, alpha=0.5)
        # df['asphericity'].plot.hist(bins=20, alpha=0.5)
        # df['acylindricity'].plot.hist(bins=20, alpha=0.5)
    except:
        open(f'{dir_out}/{name}.png', 'w').close()
        continue

    main = df.drop(df[df['radius'] < 5].index)
    satellite = df.drop(df[df['radius'] > 5].index)

    # main_log = main.copy()
    # for iter, item in enumerate(main_log['radius']):
    #     print(item)
    #     main_log[iter] = np.log(item)
    # main_log['radius'].plot.kde(bw_method=0.1)

    # try:
    #     am, locm, scalem = stats.skewnorm.fit(main['radius'].tolist())
    #     ass, locs, scales = stats.skewnorm.fit(satellite['radius'].tolist())
    #     xs = np.linspace(0, 5, 100)
    #     xm = np.linspace(5, 18, 100)
    #     pm = stats.skewnorm.pdf(xm, am, locm, scalem)
    #     ps = stats.skewnorm.pdf(xs, ass, locs, scales)
    #
    #     plt.plot(xs, ps)
    #     plt.plot(xm, pm)
    # except:
    #     pass

    try:
        avg = main['radius'].mean()
        std = main['radius'].std()
        median = main['radius'].median()
        # avg_log = main_log['radius'].mean()

        avg_sat = satellite['radius'].mean()
        std_sat = satellite['radius'].std()

        plt.errorbar(avg, 0.6, xerr = std, fmt='o',ecolor = 'black ',color='black')
        plt.errorbar(avg_sat, 0.6, xerr = std_sat, fmt='o',ecolor = 'black',color='black')
        plt.scatter(median, 0.7, 'ko')
        plt.text(median, 0.75, 'ko')

    except:
        pass

    plt.title(f'Droplet Size Distribution, A={A}, snapshot={name}')
    plt.xlim(0, 15)
    plt.ylim(0, 0.8)
    plt.xlabel('Radius')
    plt.ylabel('Density')
    plt.grid(True)
    # plt.savefig(f'{dir_out}/{name}.png', format='png')
    plt.show()
    plt.close(1)






#
