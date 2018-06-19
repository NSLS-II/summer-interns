import numpy as np
import matplotlib.pyplot as plt
vertical = 294
horizontal = 528

martix = []
d = np.loadtxt('res_int_pr_se.dat')
d2 = d.reshape((vertical, horizontal))
matrix = d2

fig = plt.figure()

ax2 = fig.add_subplot(212)
ax2.plot(np.linspace(-10, 10, len(np.array(matrix[0, :]))), np.array(matrix[0, :]))
ax2.set_xlim(-10, 10)

ax1 = fig.add_subplot(211, sharex=ax2)
ax1.imshow(matrix, extent=(-10, 10, -20, 20), aspect='auto')


plt.show()
