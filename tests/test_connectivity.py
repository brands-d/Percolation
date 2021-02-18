from percolation.library.grid import Grid
from percolation.model.hk import HoshenKopelman
from percolation.model.measurment import *
from percolation.model.correlation import *

import matplotlib.pyplot as plt

N, M, p = 50, 50, 0.5927
grid = Grid((N, M))
hk = HoshenKopelman(grid)
grid.randomize(p)
hk.setup()
labels, sizes = hk.run()

# grid.plot(labels=labels)
connectivity = get_connectivity(labels, sizes[-1])[1:]
out = extract_correlation_length(connectivity)
A = out.params['A'].value
corr = out.params['corr'].value

print(fit_report(out))

r = np.array(range(1, len(connectivity) + 1))
plt.plot(r, connectivity,
         r, model_corr(r, corr, A))

plt.show()
