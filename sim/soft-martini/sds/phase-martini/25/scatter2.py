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
data = pipeline.compute()

num = 300

density = data.particles.count/data.cell.volume
length = data.cell.matrix[0,0]/2
pipeline.modifiers.append(SelectTypeModifier(types=[1,2]))
modifier = CoordinationAnalysisModifier(
    cutoff = 15, 
    number_of_bins = num,
    only_selected=False)
pipeline.modifiers.append(modifier)


result = np.zeros(num)
fresult = np.zeros(int(num/2+1))
count = 0
for i in range(340, pipeline.num_frames):
    print(i)
    data = pipeline.compute(i)
    sf = data.tables['coordination-rdf'].xy()
    temp = sf.transpose()[1]
    r = sf.transpose()[0]
    result += temp
    fresult += abs(fft.rfft(temp-1))
    count+=1

g = result/count

q = np.logspace(-2, 0, 1000)
sk = np.zeros(len(q))
for n, i in enumerate(q):
    integrand = 4*np.pi*r**2*(g)*np.sinc(i*r/np.pi)*density
    sk[n] = np.trapezoid(integrand, r) + 1
     

pipeline.modifiers.append(StructureFactorModifier(
    k_bins=num, k_min=0, k_max=6,
    only_selected=False,
    mode=StructureFactorModifier.Mode.Debye,
    partial=False
    ))
data = pipeline.compute(300)
sf = data.tables['structure-factor'].xy().transpose()


pipeline.modifiers.append(StructureFactorModifier(
    k_bins=num, k_min=0, k_max=6,
    only_selected=False,
    mode=StructureFactorModifier.Mode.Direct,
    partial=False
    ))
data = pipeline.compute(300)
sf2 = data.tables['structure-factor.2'].xy().transpose()

import matplotlib.pyplot as plt


fig, ax = plt.subplots(2,2)


ax[0,0].loglog(q, sk)
ax[1,0].plot(q, sk)

ax[0,1].plot(r, g)
# ax[1,1].plot(fft.rfftfreq(num), 1+density*fresult/count)
ax[1,1].loglog(sf[0]/(2*np.pi), sf[1])
ax[1,1].loglog(sf2[0]/(2*np.pi), sf2[1])
ax[1,1].loglog(q, sk)
ax[1,1].set_xlim(0.01,1)


plt.show()