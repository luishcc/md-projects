import math
import os
os.environ['OVITO_GUI_MODE'] = '1' # Request a session with OpenGL support
import ovito
from ovito.io import *
from ovito.modifiers import *
from ovito.vis import *
import numpy as np
from scipy import fft
pipeline = import_file("sds.lammpstrj")

num = 300

pipeline.modifiers.append(SelectTypeModifier(types=[1,2]))
modifier = CoordinationAnalysisModifier(cutoff = 20.0, number_of_bins = num)
pipeline.modifiers.append(modifier)


result = np.zeros(num)
fresult = np.zeros(int(num/2+1))
count = 0
for i in range(200, pipeline.num_frames):
    print(i)
    data = pipeline.compute(i)
    sf = data.tables['coordination-rdf'].xy()
    temp = sf.transpose()[1]
    result += temp
    fresult += abs(fft.rfft(temp-1))
    count+=1

density = data.particles.count/data.cell.volume

import matplotlib.pyplot as plt


fig, ax = plt.subplots(1,2)

ax[0].loglog(fft.rfftfreq(300), 1+density*fresult/count)
# ax.set_ylim(0.1, 10)
ax[0].set_xlim(0.01, 1)


ax[1].plot(sf.transpose()[0], temp)

plt.show()