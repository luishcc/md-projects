import numpy as np
import sys
import os
sys.path.insert(0, os.path.expanduser('~')+'/md-projects/lampy')
from grid import Grid
from readLammps import DumpReader
from math import floor

from scipy.fft import fft, fftfreq, fftshift, rfft, rfftfreq

import matplotlib.pyplot as plt


# plt.rcParams.update({
#     "text.usetex": True,
#     "font.family": "sans-serif",
#     "font.size": 14,
#     "font.sans-serif": ["Helvetica"]})


rd = DumpReader('thread.lammpstrj')
rd.map_snapshot_in_file()


for time in rd.timesteps.keys():
    print(time/100 - 100)
    rd.read_snapshot(time)
    grd = Grid(rd.snapshots[time], size = float(sys.argv[1]))
    res = []
    rrange = int(sys.argv[2])
    for r in range(rrange):
        a = grd.compute_density_correlation(r)
        res.append(a)

    num = floor(grd.num_z/2)
    plt.figure()
    for r in range(rrange):
        if float('Nan') in res[r]:
            continue
        plt.plot(np.linspace(0, grd.length_z/2, num), res[r], label=f'R={r}')
    plt.xlabel(r'$\delta z$')
    plt.ylabel(r'$G(r,\delta z)$')
    plt.legend(loc='right')
    plt.savefig(f'gif/{time}.png', format='png')


    f = fftshift(fft(res[5]))
    freq = fftshift(fftfreq(len(res[5])))

    f = rfft(res[5]) / len(res[5])
    freq = rfftfreq(len(res[5]))

    plt.figure()
    plt.plot(freq[:], f.real[:], 'k-', marker='o')
    # plt.plot([min(freq[1:20]), max(freq[1:20])], [0,0], 'r-.')
    # plt.ylim(-0.6,3)
    plt.xlim(0,0.2)
    plt.savefig(f'gif2/{time}.png', format='png')

# rd.read_snapshot(20500)
# data = rd.snapshots[20500]
# grd = Grid(data, size = float(sys.argv[1]))

for snap in rd.snapshots.values():
    grd = Grid(snap, size = float(sys.argv[1]))
    res = []
    rrange = int(sys.argv[2])
    for r in range(rrange):
        a = grd.compute_density_correlation(r)
        res.append(a)


    plt.figure(1)
    # print(grd.length_z)
    for r in range(rrange):
        if float('Nan') in res[r]:
            continue
        plt.plot(np.linspace(0, grd.length_z/2, num), res[r], label=f'R={r}')
    plt.xlabel(r'$\delta z$')
    plt.ylabel(r'$G(r,\delta z)$')
    plt.legend(loc='right')
    plt.savefig(f'gif/{snap}.jpg', format='jpg')



    f = fftshift(fft(res[5]))
    freq = fftshift(fftfreq(len(res[5])))

    f = rfft(res[5]) / len(res[5])
    freq = rfftfreq(len(res[5]))

    plt.figure(2)
    plt.plot(freq[:], f.real[:], 'k-', marker='o')
    # plt.plot([min(freq[1:20]), max(freq[1:20])], [0,0], 'r-.')
    # plt.ylim(-0.6,3)
    plt.xlim(0,0.2)
    plt.savefig(f'gif2/{snap}.jpg', format='jpg')

    # plt.plot(freq, f.imag, 'b-')

    # spec = np.abs(f)**2

    # plt.subplot(133)
    # plt.plot(freq, spec/max(spec), 'b-')

    # plt.show()

    # idr = []
    # idz = []
    # d = []
    # for key, cell in grd.cell.items():
    #     idr.append(cell.id[0])
    #     idz.append(cell.id[2])
    #     d.append(cell.get_density()/cell.nangle)
    #
    # from scipy.sparse import coo_matrix
    # coo = coo_matrix((d, (idr, idz)))
    #
    # coo = coo.todense().transpose()
    #
    #
    # fig, ax = plt.subplots(1,1)
    # im = ax.imshow(coo, extent=[0, 1, 0, 1], aspect=10)
    # fig.colorbar(im)
    # ax.set_xlabel('Radius')
    # ax.set_ylabel('Length')
    # ax.yaxis.set_major_locator(plt.NullLocator()) # remove y axis ticks
    # ax.xaxis.set_major_locator(plt.NullLocator()) # remove x axis ticks
    # fig.set_dpi(460)


# plt.show()
