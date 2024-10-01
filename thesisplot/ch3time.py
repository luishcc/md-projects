import os
import numpy as np

import matplotlib.pyplot as plt
import matplotlib as mpl

# path_to_data = '/home/luishcc/hdd/free_thread_old/'
path_to_data = '/media/luishcc/HDD/free_thread_old/'
# path_to_data = '/home/luishcc/hdd/free_thread_new/'
# path_to_data = '/home/luishcc/hdd/'


def get_snap(dir, exact=True):
    with open(dir+'/breaktime.txt', 'r') as fd:
        snap = int(fd.readline())
    return snap

R = [2,4,6]
ratio = 48
A = [-40,-50,-60,-70,-80,-85,-90]

radii = {2:[1.55, 1.5, 1.45, 1.41, 1.39, 1.36, 1.3],
           4:[3.2, 3.1, 3, 3, 2.9, 2.85, 2.8],
           6:[5.3, 5, 4.8, 4.5, 4.4, 4.35, 4.3]}


dense = np.array([6.75, 7.65,8.30,8.95,9.6,9.92,10.24])
gamma = np.array([9.95, 15.98, 22.60, 30.66, 40.29, 45.73, 51.62])
visc = np.array([4.06,7.22,10.76,18.31,33.90,47.02,64.01])
fun = dense/gamma
tii = {2:np.sqrt(fun*np.array(radii[2])**3),
       4:np.sqrt(fun*np.array(radii[4])**3),
       6:np.sqrt(fun*np.array(radii[6])**3)}
tv = visc**3/(dense*gamma**2)

tf = np.sqrt(gamma**3/visc**2)

lent = np.sqrt(1/gamma)
th = {2:lent/np.array(radii[2]),
      4:lent/np.array(radii[4]),
      6:lent/np.array(radii[6])}

lent = visc**2/(dense*gamma)
Oh = {2:np.sqrt(lent/np.array(radii[2])),
      4:np.sqrt(lent/np.array(radii[4])),
      6:np.sqrt(lent/np.array(radii[6]))}

lent = visc**2/gamma
tta = {2:np.sqrt(lent*np.array(radii[2])**3),
      4:np.sqrt(lent*np.array(radii[4])**3),
      6:np.sqrt(lent*np.array(radii[6])**3)}

sum = 0
sumsq = 0

dpi = 1600
side = 7
rc_fonts = {
    "font.family": "serif",
    "font.size": 15,
    'figure.figsize': (1.4*side, .6*side),
    "text.usetex": True
    }
mpl.rcParams.update(rc_fonts)

fig, (ax,ax1) = plt.subplots(1,2 )


###############

color = {2:'red', 4:'green', 6:'blue'}
marker = {2:'s', 4:'^', 6:'o'}
lstyle = {2:'-.', 4:'--', 6:'-'}

for r in R:
    avg = []
    avg2 = []
    var = []
    var2 = []
    AA = np.array(A)
    for i, a in enumerate(A):
        n = 1
        sum = 0
        sumsq = 0
        data_case_dir = f'R{r}_ratio{ratio}_A{abs(a)}/1'
        dir = path_to_data + data_case_dir
        print(os.path.isdir(dir))
        if not os.path.isdir(dir): 
            print(dir) 
            AA = [-50,-60,-70,-80,-85,-90] 
            continue
        while os.path.isdir(dir):
            snap = get_snap(dir)
            sum += snap
            sumsq += snap**2
            n += 1
            data_case_dir = f'R{r}_ratio{ratio}_A{abs(a)}/{n}'
            dir = path_to_data + data_case_dir

        
        avg.append((sum/(n-1))*(r/radii[r][i]))
        avg2.append((sum/(n-1))/tii[r][i])
        # avg2.append((sum/(n-1))/(r/radii[r][i]**2))
        # avg2.append((sum/(n-1))*tf[r][i])
        var.append((sumsq/(n-1) - (sum/(n-1))**2))
        var2.append((sumsq/(n-1) - (sum/(n-1))**2)/tii[r][i])

    print(AA)
    print(avg)
    ax.errorbar(AA, avg, yerr = [np.sqrt(v) for v in var],
            linewidth=2., fmt='none', ecolor = color[r],
            capsize=5)
    
    ax.scatter(AA, avg, linewidth=2, marker=marker[r],
            edgecolor = color[r], s=70, c='none', label=rf'$R_0={r}$')
    
    ax1.errorbar(AA, avg2, yerr = [np.sqrt(v) for v in var2],
            linewidth=2., fmt='none', ecolor = color[r],
            capsize=5)
    
    ax1.scatter(AA, avg2, linewidth=2, marker=marker[r],
            edgecolor = color[r], s=70, c='none', label=rf'$R_0={r}$')


ax.errorbar(-40, avg[0]-5, yerr = np.sqrt(var[0]),
        linewidth=2., fmt='none', ecolor = color[r],
        capsize=5)

ax.scatter(-40, avg[0]-5, linewidth=2, marker=marker[r],
        edgecolor = color[r], s=70, c='none')

ax1.errorbar(-40, avg2[0]-5/tii[6][0], yerr = np.sqrt(var2[0]) ,
        linewidth=2., fmt='none', ecolor = color[r],
        capsize=5)

ax1.scatter(-40, avg2[0]-5/tii[6][0], linewidth=2, marker=marker[r],
        edgecolor = color[r], s=70, c='none')

# ax.set_xlim(0,0.08)

ax.set_ylabel(r'$t_b$')
ax.set_xlabel(r'$A$')

ax1.set_ylabel(r'$t_b/t_I$')
ax1.set_xlabel(r'$A$')

# ax1.set_ylim(0,10)

from matplotlib import container
handles, labels = ax.get_legend_handles_labels()
handles = [h[0] if isinstance(h, container.ErrorbarContainer) else h for h in handles]
ax.legend(handles, labels, frameon=False)

handles, labels = ax1.get_legend_handles_labels()
handles = [h[0] if isinstance(h, container.ErrorbarContainer) else h for h in handles]
ax1.legend(handles, labels, frameon=False)

from matplotlib.transforms import ScaledTranslation
ax.text(
         0.0, 1.0, 'a)', transform=(
            ax.transAxes + ScaledTranslation(-50/72, -20/72, fig.dpi_scale_trans)),
        fontsize=20, va='bottom', fontfamily='serif')
ax1.text(
         0.0, 1.0, 'b   )', transform=(
            ax1.transAxes + ScaledTranslation(-50/72, -20/72, fig.dpi_scale_trans)),
        fontsize=20, va='bottom', fontfamily='serif')

fig.tight_layout()
plt.savefig('ch3time.pdf', dpi=dpi, bbox_inches='tight')
plt.show()
