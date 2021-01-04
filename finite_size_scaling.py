from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

path = Path('./output/04.01.2021')
S = np.loadtxt(path / 'S.np').T

fig, ax = plt.subplots()
for lattice_size in S:
    ax.plot(lattice_size)

ax.grid()
plt.show()
