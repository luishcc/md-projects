import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve



def eos_warren(a, b, rho, rc=1, rd=0.75, kbT=1):
  alpha = 0.101
  c = 4.16
  d = 18
  t2 = alpha*a*rho**2
  t3 = 2*alpha*b*0.75**4*(rho**3-c*rho**2+d) 
  return rho*kbT + t2  + t3 
  

def eos_jamali(a, b, rho, rc=1, rd=0.75, kbT=1):
  alpha = 0.101
  c = 4.63
  d = 7.55
  t2 = alpha*a*rc**4*rho**2
  t3 = 2*alpha*b*rd**4*(rho**3-c*rho**2+d) 
  t4 = (alpha*b*rd**4*rho**2) / (np.sqrt(abs(a)))
  return rho*kbT + t2  + t3 - t4

def sigma_fit(a, b, rho, rc=1, rd=0.75, kbT=1):
  return   -(np.pi/240) * (0.42*a*rc**5*rho**2 + 0.003*b*rd**5*rho**3)


def oh_number(rho, mu, sigma, l):
  return mu/np.sqrt(rho*sigma*l)
  

#func1 = lambda x: eos_warren(-85, 25, x)
#print( sigma_fit(-85,25, fsolve(func1, 9 )))

#exit()

mu = [7.22, 10.76, 18.31, 33.9, 64.01]

guess1 = 6
guess2 = 6
for a, m in zip(np.linspace(-50, -90, 5), mu):
  func1 = lambda x: eos_warren(a, 25, x)
  func2 = lambda x: eos_jamali(a, 25, x)
  guess1 = fsolve(func1, guess1)
  guess2 = fsolve(func2, guess2)
  st1 = sigma_fit(a,25,guess1)
  st2 = sigma_fit(a,25,guess2)
  print('density:         ', guess1, guess2)
  print('surface tension: ', st1, st2)
  print('Oh:              ', oh_number(guess1, m, st1, 6), oh_number(guess2, m, st2, 6))

exit()

density = np.linspace(5, 11, 100)
plt.figure()
for a in np.linspace(-50, -90, 5):
  plt.plot(density, [eos_jamali(a,25,r) for r in density], label = a)



plt.legend(loc='upper left')
plt.plot([min(density), max(density)], [0, 0], 'k--')
plt.show()
