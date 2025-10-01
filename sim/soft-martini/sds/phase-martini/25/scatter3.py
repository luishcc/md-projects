import math
import os
os.environ['OVITO_GUI_MODE'] = '1' # Request a session with OpenGL support
import ovito
from ovito.io import *
from ovito.modifiers import *
from ovito.vis import *
import numpy as np

form_factors = {
    1: 1.0,   # Type 1 bead (e.g. Qd)
    2: 1.0,   # Type 2 bead (e.g. C1)
    3: 1.0,   # Type 3 bead (e.g. Qa)
    4: 1.0    # Type 4 bead P4
}

pipeline = import_file("sds.lammpstrj")
data = pipeline.compute()

volume = data.cell.volume

type_list = data.particles.particle_type.array
types = np.unique(type_list)
count_per_type = np.array([len(type_list[type_list==t+1]) for t in range(4)])

xi = count_per_type/data.particles.count  # mol fractions
density = data.particles.count/data.cell.volume

start_frame = 100
end_frame = pipeline.num_frames
num_frames = end_frame-start_frame

num = 300
cutoff = 15
# cutoff = data.cell.matrix[0,0]/2 # Half sim box

rdf_mod = CoordinationAnalysisModifier(
    cutoff = cutoff, 
    number_of_bins = num,
    partial = True)
pipeline.modifiers.append(rdf_mod)

avg_mod = TimeAveragingModifier(
    operate_on='table:coordination-rdf',
    interval=(start_frame,end_frame-1))
pipeline.modifiers.append(avg_mod)

data = pipeline.compute()

# exit()

rdf = data.tables['coordination-rdf[average]']
r = rdf.xy().transpose()[0]
g_array = rdf.y

q_values = np.logspace(-2, 0, 1000)
Iq = np.zeros(len(q_values))
for n, q in enumerate(q_values):
    id = 0
    term1 = 0
    term2 = 0
    for i in range(len(types)):
        term1 += xi[i]*form_factors[i+1]**2
        for j in range(i,len(types)):
            pre = xi[i]*form_factors[i+1]*xi[j]*form_factors[j+1]
            integrand = r**2 * (g_array[:,id]) * np.sinc(q*r/np.pi)
            term2 += pre * np.trapezoid(integrand, r)  
            id += 1

    Iq[n] = term1 + term2 * 4*np.pi*density

Iq/=4


import matplotlib.pyplot as plt


fig, ax = plt.subplots(2,2)


ax[0,0].loglog(q_values, Iq)
ax[1,0].plot(q_values, Iq)

for i in range(10):
    ax[0,1].plot(r, g_array[:,i], label=rdf.y.component_names[i])
ax[0,1].legend()



plt.show()