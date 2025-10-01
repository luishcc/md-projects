# Matches the results obtained in Nat Comm publication 
# doi.org/10.1038/s41467-024-45840-9

import math
import os
os.environ['OVITO_GUI_MODE'] = '1' # Request a session with OpenGL support
import ovito
from ovito.io import *
from ovito.modifiers import *
from ovito.vis import *
import numpy as np



pipeline = import_file("rdf.dump")
data = pipeline.compute()

volume = data.cell.volume

type_list = data.particles.particle_type.array
types = np.unique(type_list)
count_per_type = np.array([len(type_list[type_list==t+1]) for t in range(4)])

xi = count_per_type/data.particles.count  # mol fractions
density = data.particles.count/data.cell.volume

start_frame = 0
end_frame = pipeline.num_frames
num_frames = end_frame-start_frame

num = 1500
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

#q_values = np.logspace(-1, 0, 1000)
q_values = np.arange(0.5, 10, 0.01)
Iq = np.zeros(len(q_values))


para = {1: [
        6.29150,
        2.43860,
        3.03530,
        32.3337,
        1.98910,
        0.678500,
        1.54100,
        81.6937,
        1.14070],        #Si
        0: [
        3.04850,
        13.2771,
        2.28680,
        5.70110,
        1.54630,
        0.323900,
        0.867000,
        32.9089,
        0.250800]}    #O

    
factors = np.zeros((2,len(q_values)))
for i in range(4):
    factors[0] += para[0][2 * i] * np.exp(
    -para[0][2 * i + 1] * (q_values / (np.pi * 4)) ** 2
    )
    factors[1] += para[1][2 * i] * np.exp(
    -para[1][2 * i + 1] * (q_values / (np.pi * 4)) ** 2
    )
factors[1] += para[1][-1]
factors[0] += para[0][-1]


id = 0
term = 0
f = 1
for i in range(len(types)):
    for j in range(i,len(types)):
        if i == j:
            f = 1
        else:
            f = 2
        pre = xi[i] * factors[i] * xi[j] * factors[j]
        integrand = r**2 * (g_array[:,id]-1) * np.sinc(np.outer(q_values,r)/np.pi)
        term += f*pre*(1 + 4 * np.pi * density * np.trapezoid(integrand, r, axis=1)  )
        id += 1

Iq = term

norm = 0
for i in range(len(types)):
    norm += xi[i]*factors[i]
    
Iq /= norm**2

import matplotlib.pyplot as plt


#fig, ax = plt.subplots(2,2)


#ax[0,0].loglog(q_values, Iq)
#ax[1,0].plot(q_values, Iq)

#for i in range(3):
#    ax[0,1].plot(r, g_array[:,i], label=rdf.y.component_names[i])
#ax[0,1].legend()

plt.plot(q_values, Iq)

plt.show()
