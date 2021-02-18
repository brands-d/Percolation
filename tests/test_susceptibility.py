from percolation.library.grid import Grid
from percolation.model.hk import HoshenKopelman
from percolation.model.measurment import *
from percolation.model.correlation import *
from percolation.model.fss import *

import matplotlib.pyplot as plt

Ls = [25, 50]
ps = [0.2, 0.3, 0.4, 0.5, 0.55, 0.57, 0.59, 0.6]
num = 500
S = np.zeros((len(Ls), len(ps)))

for i, L in enumerate(Ls):
    grid = Grid((L, L))

    for j, p in enumerate(ps):
        hk = HoshenKopelman(grid)
        temp = []
        for _ in range(num):
            grid.randomize(p)
            hk.setup()
            labels, sizes = hk.run()

            temp.append(get_susceptibility(sizes))

        S[i, j] = np.mean(temp)

for data in S:
    plt.plot(ps, data)

out = fss(S, Ls, ps)
print(fit_report(out))
plt.show()
