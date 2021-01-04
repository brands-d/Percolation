from percolation.library.grid import Grid
from percolation.model.hk import HoshenKopelman
import numpy as np
import matplotlib.pyplot as plt

N, M = 250, 250
grid = Grid((N, M), periodic=True)
hk = HoshenKopelman(grid)
P_infty = []
num = 10
ps = np.array(range(40, 60,2)) / 100

for p in ps:
    print(p)
    temp = []
    for i in range(num):
        grid.randomize(p)
        hk.setup()
        _, sizes = hk.run()
        temp.append(max(sizes) / grid.size)

    P_infty.append(np.mean(temp))

plt.plot(ps, P_infty)
plt.show()
