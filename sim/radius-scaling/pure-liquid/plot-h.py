import numpy as np

def get_breaktime(dir):
    with open(f'{dir}/breaktime.txt', 'r') as fd:
        snap = int(fd.readline())
    return snap

def read_sim(dir):
    shape = {}
    breaktime = get_breaktime(dir)
    for i in range(breaktime + 10):
        h = []
        z = []
        file = f'{dir}/surface_profile/{i}.dat'
        with open(file, 'r') as fd:
            next(fd)
            next(fd)
            for line in fd:
                data = line.split()
                h.append(float(data[1]))
                z.append(float(data[0]))
        shape[i] = [np.array(h), np.array(z)]
    return shape 


case = '/home/luishcc/hdd/radius_scaling/high-Oh'
# case = '/home/luishcc/hdd/radius_scaling/low-Oh'
nn = 2
shape = read_sim(f'{case}/{nn}')


import matplotlib.pyplot as plt
import matplotlib.animation as animation

class PauseAnimation:
    def __init__(self, shape):
        
        fig, ax = plt.subplots()
        
        self.line = ax.plot(shape[0][1], shape[0][0], 'b-', label=f'Snapshot = 0')[0]
        self.line2 = ax.plot(shape[0][1], -shape[0][0], 'b-')[0]
        ax.set(ylim=[-12, 12], xlabel='z', ylabel='h')
        self.legend = ax.legend()
               
        self.animation = animation.FuncAnimation(
            fig, self.update, frames=len(shape), interval=.1, blit=True)
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


  