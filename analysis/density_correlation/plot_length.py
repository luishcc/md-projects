import numpy as np
import matplotlib.pyplot as plt

# r6 = [0.017699, 0.019868, 0.015957, 0.017699,
#         0.018939, 0.019933, 0.017699, 0.018785, 0.01657]
# xr6 = [226, 301, 376, 452, 527, 603, 904, 1809, 1809]

r6 = [0.017699, 0.019868, 0.015957, 0.017699,
        0.018939, 0.019933, 0.017699, 0.017685]
xr6 = [226, 301, 376, 452, 527, 603, 904, 1809]


r8 = [0.013245, 0.013289, 0.013267]
xr8 = [301, 603, 1206]

r10 = [0.010638, 0.010610]
xr10 = [376, 753]

red = np.array([6,8,10]) * 2*np.pi *0.833
# red = [1,1,1]

plt.figure()

plt.title('Reduced Wavenumber')
plt.ylabel('Wavenumber')

# plt.title('Max Fourier Frequency')
# plt.ylabel('Frequency')

plt.plot(xr6, [i*red[0] for i in r6], 'ko--', label='R=6')
plt.plot(xr8, [i*red[1] for i in r8], 'b+--', label='R=8')
plt.plot(xr10, [i*red[2] for i in r10], 'gs--', label='R=10')
plt.ylim(0.1,0.8)
plt.legend(loc='lower right')
plt.xlabel('Cylinder Length')

plt.show()
