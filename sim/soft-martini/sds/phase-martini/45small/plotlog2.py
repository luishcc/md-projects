import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

dpi = 1600
side = 7
rc_fonts = {
    "font.family": "serif",
    "font.size": 15,
    'figure.figsize': (1.7*side, 1.*side),
    "text.usetex": True
    }
mpl.rcParams.update(rc_fonts)

from matplotlib.animation import FuncAnimation


try:
    file = sys.argv[1]
except: 
    file = 'log.lammps'

def read_data(_file):

    temp = []
    time = []
    eng = []
    press = []

    with open(_file, 'r') as fd:
        for line in fd:
            l  = line.split()
            try:
                tt = (float(l[0]))
                tt = (float(l[1]))
                tt = (float(l[5]))
                tt = (float(l[4]))
                # print(line, l[1])
            except Exception as e:
                continue
            time.append(float(l[0])*20/1e6)
            temp.append(float(l[1]))
            press.append(float(l[5]))
            eng.append(float(l[4]))
    return temp, time, eng, press


fig, ax = plt.subplots(3,1, sharex=True)


def update(frame):
    temp, time, eng, press = read_data(file)
    for a in ax:
        a.clear()
    ax[0].plot(time, temp, 'ko')
    ax[0].plot([time[0], time[-1]], [300, 300], 'b--')
    ax[0].set_ylim(200,350)
    ax[0].set_ylabel('Temperature [K]')

    ax[1].plot(time, press, 'ko')
    ax[1].plot([time[0], time[-1]], [1, 1], 'b--')
    ax[1].set_ylim(-500,500)
    ax[1].set_ylabel('Pressure [bar]')

    ax[2].plot(time, eng, 'ko')
    ax[2].set_ylim(-10000,-7500)
    ax[2].set_ylabel('Total Energy [kcal/mol]')
    ax[2].set_xlabel('Time [ns]')
    fig.canvas.draw()

anim = FuncAnimation(fig, update)
plt.show()

