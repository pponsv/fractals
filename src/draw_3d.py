import numpy as np
import matplotlib.pyplot as plt
import mandelbrot as mb
from time import thread_time_ns

res = 300
iters = 8
x = np.linspace(-1.5, 1.5, res)
y = np.linspace(-1.5, 1.5, res)
z = np.linspace(-1.5, 1.5, res)

w = 0.25
c =  (-0.218,-0.113,-0.181,-0.496)

t0 = thread_time_ns()
out = mb.fractal_4d(x, y, z, w, c, iters)
print(1e-9*(thread_time_ns()-t0))

print(out.shape)
points = out[:, 0:3][out[:,3]>=6]

fig, ax = plt.subplots(1,1, subplot_kw={'projection':'3d'})
ax.plot(*points.T, ',', color='k')

plt.show()
# print('Done, saving...')
# np.savetxt('out.txt', out.reshape(-1,4))
# print('Done')