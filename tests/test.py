import numpy as np
import matplotlib.pyplot as plt

from percolation.library.grid import Grid
from percolation.model.hk import HoshenKopelman

N, M, p = 10,10, 0.38
grid = Grid((N, M))
grid.randomize(p)
hk = HoshenKopelman(grid)
hk.setup()
labels, sizes = hk.run()
grid.plot(labels=labels)

for i in range(len(sizes)):
    print(i + 1, ': ', sizes[i])

plt.show()

#
# P_infty = []
# num = 10
# ps = np.array(range(40, 60, 2)) / 100
#
# for p in ps:
#     print(p)
#     temp = []
#     for i in range(num):
#         grid.randomize(p)
#         hk.setup()
#         _, sizes = hk.run()
#         temp.append(max(sizes) / grid.size)
#
#     P_infty.append(np.mean(temp))
#
# plt.plot(ps, P_infty)
# plt.show()
