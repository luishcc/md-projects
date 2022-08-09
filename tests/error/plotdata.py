import matplotlib.pyplot as plt

from mdpkg.rwfile import read_dat

file = 'foo-0/foo.dat'
filef = 'foo-0/ff.dat'

data = read_dat(file)
dataf = read_dat(filef)

fig, [ax1, ax2] = plt.subplots(2,1)
for i in range(3):
    ax1.plot(data['x'], data[str(i+1)],  label=f'{i+1}')
    ax2.plot(dataf['x'], dataf[str(i+1)],  label=f'{i+1}')


plt.show()
