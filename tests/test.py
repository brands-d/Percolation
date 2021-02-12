import numpy as np
import matplotlib.pyplot as plt

from percolation.library.grid import Grid
from percolation.model.hk import HoshenKopelman
from percolation.library.misc import *

N, M = 20, 20
ps = np.linspace(0, 1, 20)
num = 10
grid = Grid((N, M))
hk = HoshenKopelman(grid)
S = []

for p in ps:
    temp = []
    for _ in range(num):
        grid.randomize(p)
        hk.setup()
        _, sizes = hk.run()
        temp.append(get_p_inf(sizes, grid.shape))

    S.append(np.mean(temp))

plt.plot(ps, S)
plt.show()
