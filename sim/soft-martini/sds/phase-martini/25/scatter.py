import math
import os
os.environ['OVITO_GUI_MODE'] = '1' # Request a session with OpenGL support
import ovito
from ovito.io import *
from ovito.modifiers import *
from ovito.vis import *
import numpy as np

pipeline = import_file("sds.lammpstrj")

num = 300

pipeline.modifiers.append(SelectTypeModifier(types=[1,2]))
pipeline.modifiers.append(StructureFactorModifier(
    k_bins=num, k_min=0, k_max=6,
    only_selected=0,
    mode=StructureFactorModifier.Mode.Debye,
    partial=True
    ))
# data = pipeline.compute(10)

result = np.zeros(num)
count = 0
for i in range(340, pipeline.num_frames):
    print(i)
    data = pipeline.compute(i)
    sf = data.tables['structure-factor'].xy()
    result += sf.transpose()[5]
    count+=1


import matplotlib.pyplot as plt


fig, ax = plt.subplots(1,1)

ax.loglog(sf.transpose()[0]/(2*np.pi), result/count)
ax.set_ylim(0.1, 10)
ax.set_xlim(0.01, 0.7)
plt.show()