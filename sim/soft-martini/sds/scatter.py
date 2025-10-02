import math
import os
os.environ['OVITO_GUI_MODE'] = '1' # Request a session with OpenGL support
import ovito
from ovito.io import *
from ovito.modifiers import *
from ovito.vis import *
import numpy as np


# path = 'phase-mdpd/4'
# path = 'phase-mdpd/25'
# path = 'phase-martini/5'
path = 'phase-martini/25'

# convert = 8.42
convert = 1

num = 200
cutoff = 30.5/convert

pipeline = import_file(f'{path}/sds.lammpstrj')
data = pipeline.compute()

volume = data.cell.volume

type_list = data.particles.particle_type.array
types = np.unique(type_list)
count_per_type = np.array([len(type_list[type_list==t+1]) for t in range(4)])

xi = count_per_type/data.particles.count  # mol fractions
density = data.particles.count/data.cell.volume

start_frame = int(pipeline.num_frames/2)
end_frame = pipeline.num_frames
num_frames = end_frame-start_frame

# cutoff = data.cell.matrix[0,0]/2 # Half sim box
only_selected = True

if only_selected:
    types = [1,2,3]
    pipeline.modifiers.append(SelectTypeModifier(types=types))


num_pairs = np.sum([i for i in range(len(types))])

rdf_mod = CoordinationAnalysisModifier(
    cutoff = cutoff, 
    number_of_bins = num,
    partial = True,
    only_selected=only_selected)
pipeline.modifiers.append(rdf_mod)

avg_mod = TimeAveragingModifier(
    operate_on='table:coordination-rdf',
    interval=(start_frame,end_frame-1))
pipeline.modifiers.append(avg_mod)

data = pipeline.compute()

rdf = data.tables['coordination-rdf[average]']
r = rdf.xy().transpose()[0]*convert
g_array = rdf.y

# q_values = np.logspace(-2, 0, 1000)
q_values = np.linspace(0.008, 0.7, 100)
Iq = np.zeros(len(q_values))


# ###########################################################
# # Compute factors for xray scattering 
# para = {1: [6.29150, 2.43860, 3.03530, 32.3337, 1.98910,
#             0.678500, 1.54100, 81.6937, 1.14070],        #Si
#         0: [3.04850, 13.2771, 2.28680, 5.70110, 1.54630,
#             0.323900, 0.867000, 32.9089, 0.250800]}    #O
    
# factors = np.zeros((2,len(q_values)))
# for i in range(4):
#     factors[0] += para[0][2 * i] * np.exp(
#     -para[0][2 * i + 1] * (q_values / (np.pi * 4)) ** 2
#     )
#     factors[1] += para[1][2 * i] * np.exp(
#     -para[1][2 * i + 1] * (q_values / (np.pi * 4)) ** 2
#     )
# factors[1] += para[1][-1]
# factors[0] += para[0][-1]
# ###########################################################

###########################################################
# Factors for coherent neutron scattering 

factors = {i:1 for i in range(len(types))} # all 1 for CG sim
###########################################################

id = 0
f = 1
for i in range(len(types)):
    for j in range(i,len(types)):
        if i == j:
            f = 1
        else:
            f = 2
        pre = xi[i] * factors[i] * xi[j] * factors[j]
        integrand = (r**2 * (g_array[:,id]-1) * 
                     np.sinc(np.outer(q_values,r)/np.pi))
        Iq += (f * pre * 
                 (1 + 4 * np.pi * density * 
                  np.trapezoid(integrand, r, axis=1)))
        id += 1

# norm = 0
# for i in range(len(types)):
#     norm += xi[i]*factors[i]
# Iq /= norm**2

Iq /= max(Iq)


with open(f'{path}/scatter.dat', 'w') as fd:
    fd.write('q Sq\n')
    for q, sq in zip(q_values, Iq):
        fd.write(f'{q} {sq}\n')


# pipeline.modifiers.append(StructureFactorModifier(
#     k_bins=num, k_min=0, k_max=6,
#     only_selected=only_selected,
#     mode=StructureFactorModifier.Mode.Debye,
#     partial=False
#     ))
# data = pipeline.compute(600)
# sf = data.tables['structure-factor'].xy().transpose()


# pipeline.modifiers.append(StructureFactorModifier(
#     k_bins=num, k_min=0, k_max=6,
#     only_selected=only_selected,
#     mode=StructureFactorModifier.Mode.Direct,
#     partial=False
#     ))
# data = pipeline.compute(600)
# sf2 = data.tables['structure-factor.2'].xy().transpose()


import matplotlib.pyplot as plt

# fig, ax = plt.subplots(2,2)

# ax[0,0].loglog(q_values, Iq, 'k-o', markerfacecolor='none')
# ax[1,0].plot(q_values, Iq)

# for i in range(num_pairs):
#    ax[0,1].plot(r, g_array[:,i], label=rdf.y.component_names[i])
# ax[0,1].legend()

# # ax[1,1].loglog(sf[0]/(2*np.pi), sf[1])
# # ax[1,1].loglog(sf2[0]/(2*np.pi), sf2[1])
# ax[1,1].loglog(q_values, Iq)
# ax[1,1].set_xlim(0.01,1)

plt.loglog(q_values, Iq, 'k-o', markerfacecolor='none')
plt.show()
