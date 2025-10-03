import os
import numpy as np

import matplotlib.pyplot as plt
import matplotlib as mpl
dpi = 1600
side = 7
rc_fonts = {
    "font.family": "serif",
    "font.size": 14,
    'figure.figsize': (0.8*side, 0.6*side),
    "text.usetex": True
    }
mpl.rcParams.update(rc_fonts)


# convert_surfcon = 1              # In MDPD units (N/rc^-2)
convert_surfcon = 20**2/170**2   # From MDPD r_c^-2 to \AA^-2

def run_avg(file):
    sum = 0
    sumsq = 0
    n = 0
    with open(file, 'r') as fd:
        fd.readline()
        fd.readline()
        while True:
            line = fd.readline()
            try:
                a = float(line.split()[1])
            except:
                break
            sum += a
            sumsq += a**2
            n += 1
    avg = sum/n
    std = np.sqrt(sumsq/n - avg**2)
    return  avg, std

gamma_lst = []
sc_lst =  []
std_lst = []

for entry in os.scandir('surfaceTension-mdpd/sim'):
    if not entry.is_dir():
        continue
    try:
        sc = float(entry.name)
        gamma, std = run_avg('/'.join([entry.path, f'gamma_{sc}.profile']))
        gamma_lst.append(gamma)
        sc_lst.append(sc*convert_surfcon)
        std_lst.append(std)
    except FileNotFoundError:
        print(f'gamma_{sc}.profile not found, skipping')
        continue


zip_lst = zip(sc_lst, gamma_lst, std_lst)
sort_lst = sorted(zip_lst)
tuples = zip(*sort_lst)
sc_lst, gamma_lst, std_lst  = [list(tuple) for tuple in tuples]

const_conv = 300*1.380649/8.42**2 #KbT/rc^2 --> mN/m

gamma_lst = [const_conv*i for i in gamma_lst]
std_lst = [const_conv*i for i in std_lst]


fig, ax = plt.subplots(1,1)


ax.errorbar([0]+sc_lst, [72]+gamma_lst,
            yerr = [std_lst[0]*0.9]+std_lst, fmt='o',
            ecolor = 'black', capsize= 2, capthick=1,
            color='black', label=r'MDPD')

# ax.plot([0]+sc_lst, [72]+gamma_lst, 'ko-', label='$\gamma$')
ax.set_xlabel(r'C [\AA$^{-2}$]')
# ax.set_xlim(-.1,1.9)
ax.set_ylabel(r'$\gamma$ [mN/m]')
ax.set_ylim(20, 75)



gamma_lst = []
sc_lst =  []
std_lst = []

for entry in os.scandir('surfaceTension-martini/sim'):
    if not entry.is_dir():
        continue
    try:
        sc = float(entry.name)
        gamma, std = run_avg('/'.join([entry.path, f'gamma_{sc}.profile']))
        gamma_lst.append(gamma)
        sc_lst.append(sc*convert_surfcon)
        std_lst.append(std)
    except FileNotFoundError:
        print(f'gamma_{sc}.profile not found, skipping')
        continue

zip_lst = zip(sc_lst, gamma_lst, std_lst)
sort_lst = sorted(zip_lst)
tuples = zip(*sort_lst)
sc_lst, gamma_lst, std_lst  = [list(tuple) for tuple in tuples]


ax.errorbar(sc_lst, gamma_lst, yerr = std_lst, fmt='s',
ecolor = 'blue', capsize= 2, capthick=1,color='blue', label=r'MD')



#####################

c = []
g = []
with open('plot-data.csv', 'r') as fd:
    fd.readline()
    for line in fd:
        c.append((np.log10(float(line.split(',')[0]))))
        g.append(float(line.split(',')[1])/1000)


# for i in range(1,5):
#     c.append(min(c)**i)
#     g.append(0.072-0.0001**i)

c.append(-5)
g.append(0.0718)

c.append(-6)
g.append(0.072)

sorting = sorted(zip(c,g))
c = []
g = []
for tuple in sorting:
    c.append(tuple[0])
    g.append(tuple[1])

def fexp(x,a,b,c):
    return -a*np.exp(x*b)+c

# def fexp(x,a,b,c):
#     return a*x**2+c*x+b

# def fexp(x,a,b,c):
#     return a*np.exp(b*x) + c

def para(x, a, b, c):
    return a*x**2 + b*x + c

from scipy.optimize import curve_fit
pars, cov = curve_fit(f=fexp, xdata=c, 
                      ydata=g, p0=[1, 1, 0.072], bounds=(-np.inf, np.inf))

kb = 1.380649e-23   # in J/K
Na = 6.02214076e23  # in mol^-1
Rg = kb*Na

def para(x, a, b, c):
    return a*x**2 + b*x + c 

a1, a2, a3 = np.polyfit(c, g, 2)

x = np.linspace(min(c)+0.5, max(c), 100000)
y = para(x,a1,a2,a3)
# y = fexp(x, *pars)


grad = np.gradient(y, x, edge_order=2)
# grad2 = -(1/(kb*300)) * grad * 1e-20
grad2 = -(1/(kb*300)) * grad * 1e-20 /4

ax.plot(grad2, y*1000-1, 'r--', label='Experimental')



#####################




lines, labels = ax.get_legend_handles_labels()
ax.legend(lines, labels, loc='upper right', frameon=False)

plt.tight_layout()
plt.savefig('st2.pdf', dpi=dpi)
plt.show()

