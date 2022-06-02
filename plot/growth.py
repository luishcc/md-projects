import numpy as np
import matplotlib.pyplot as plt

# plt.rcParams.update({
#     "text.usetex": True,
#     "font.family": "sans-serif",
#     "font.size": 14,
#     "font.sans-serif": ["Helvetica"]})


def growth_rate(x, oh):
    x2 = x**2
    x4 = x2**2
    t1 = 0.5*(x2-x4)
    t2 = 2.25*oh**2*x4
    t3 = 1.5*oh*x2
    return np.sqrt(t1+t2)-t3

def max_growth(oh):
    return np.sqrt(1 / (2+np.sqrt(18)*oh))


rate1 = []
rate2 = []
rate3 = []
rate4 = []

num=100
x = np.linspace(0,1,num)
for i in x:
    rate1.append(growth_rate(i, 0.3))
    rate2.append(growth_rate(i, 0.6))
    rate3.append(growth_rate(i, 1.0))
    rate4.append(growth_rate(i, 1.5))

fig = plt.figure()
plt.plot(x, rate1, 'b-', markersize=1.4, label=f'Oh=0.3')
plt.plot(x, rate2, 'k-', markersize=1.4, label=f'Oh=0.6')
plt.plot(x, rate3, 'r-', markersize=1.4, label=f'Oh=1.0')
plt.plot(x, rate4, 'y-', markersize=1.4, label=f'Oh=1.5')

ohh = [0.3, 0.6, 1.0, 1.5]
for oh in ohh:
    m = max_growth(oh)
    plt.plot(m, growth_rate(m, oh), 'ko', markersize=3.4)
        

plt.title('Growth Rate')
plt.xlabel(r'$\chi$')
plt.ylabel(r'$\omega / \omega_0$')
plt.legend(loc='upper right')
plt.grid('on')
#fig.savefig('temp.png', transparent=True)

plt.show()
