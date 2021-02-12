from percolation.library.grid import Grid
from percolation.model.hk import HoshenKopelman
from percolation.model.measurment import *

import matplotlib.pyplot as plt

N, M, p = 50, 50, 0.3
grid = Grid((N, M))
hk = HoshenKopelman(grid)
grid.randomize(p)
hk.setup()
labels, sizes = hk.run()

# grid.plot(labels=labels)
connectivity = get_connectivity(labels)
plt.plot(range(len(connectivity)), connectivity)
plt.show()
