import numpy as np
import matplotlib.pyplot as plt

def eos(a,b,rho):
  alph = 0.101
  c = 4.63
  d = 7.55
  t2 = alph*a*rho**2
  t3 = 2*alph*b*0.75**4*(rho**3-c*rho**2+d) 
  t4 = (alph*b*0.75**4*rho**2) / (np.sqrt(abs(a)))
  return rho + t2  + t3 - t4
  
density = np.linspace(6, 11, 100)
plt.figure()
for a in np.linspace(-40, -100, 7):
  plt.plot(density, [eos(a,25,r) for r in density], label = a)

plt.legend(loc='upper left')
plt.plot([min(density), max(density)], [0, 0], 'k--')
plt.show()
