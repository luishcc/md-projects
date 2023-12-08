import os
import numpy as np

def get_breaktime(dir):
    with open(f'{dir}/breaktime.txt', 'r') as fd:
        snap = int(fd.readline())
    return snap

def read_sim(dir):
    shape = {}
    shift = 0
    breaktime = get_breaktime(dir)
    for i in range(breaktime + 10):
        h = []
        z = []
        file_check  = f'{dir}/surface_profile/{i+1}.dat'
        file = f'{dir}/surface_profile/{i}.dat'
        if not os.path.isfile(file_check): break
        with open(file, 'r') as fd:
            next(fd)
            next(fd)
            for line in fd:
                data = line.split()
                h.append(float(data[1]))
                z.append(float(data[0]))
        h = np.array(h)
        z = np.array(z)
        # if not shift: shift = int(np.floor(len(h)/2)) - minH_id
        # if not shift: shift = -h.argmax()
        # h = np.roll(h, shift)
        shape[i] = [h, (z+0.5)*1.2019]
        shift = int(np.floor(len(h)/2)) - h.argmin()
    shape = { i: [np.roll(j[0], shift), j[1]] for i, j in shape.items() }
    return shape 


# case = '/home/luishcc/hdd/radius_scaling/high-Oh'
# case = '/home/luishcc/hdd/radius_scaling/low-Oh'
# case = '/home/luishcc/hdd/radius_scaling/surfactant/0.5'
case = '/home/luishcc/hdd/radius_scaling/surfactant/2.9'
# case = '/home/luishcc/md-projects/sim/radius-scaling/surfactant/0.5'
# case = '/home/luishcc/md-projects/sim/radius-scaling/surfactant/2.9'
nn = 10
shape = read_sim(f'{case}/{nn}')
# shape = read_sim(f'{case}')


import matplotlib.pyplot as plt
import matplotlib.animation as animation

class PauseAnimation:
    def __init__(self, shape):
        
        fig, ax = plt.subplots()
        
        self.line = ax.plot(shape[0][1], shape[0][0], 'b-', label=f'Snapshot = 0')[0]
        self.line2 = ax.plot(shape[0][1], -shape[0][0], 'b-')[0]
        ax.set(ylim=[-18, 18], xlabel='z', ylabel='h')
        ax.set_aspect('equal', adjustable='box')
        self.legend = ax.legend(loc='upper left')
               
        self.animation = animation.FuncAnimation(
            fig, self.update, frames=len(shape), interval=5, blit=True)
        self.paused = False

        fig.canvas.mpl_connect('button_press_event', self.toggle_pause)

    def toggle_pause(self, *args, **kwargs):
        if self.paused:
            self.animation.resume()
        else:
            self.animation.pause()
        self.paused = not self.paused

    def update(self, frame):
        # for each frame, update the data stored on each artist.
        h = shape[frame][0]
        z = shape[frame][1]
        self.line.set_xdata(z)
        self.line.set_ydata(h)
        self.line2.set_ydata(-h)
        self.legend.get_texts()[0].set_text(f'Snapshot = {frame}') 
        return (self.line, self.line2, self.legend)

pa = PauseAnimation(shape)
plt.show()


  