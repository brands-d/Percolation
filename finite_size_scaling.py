from pathlib import Path
from configparser import ConfigParser

import numpy as np
import matplotlib.pyplot as plt

path = Path('./output/04.01.2021')
config = ConfigParser()
config.read(path / 'input.ini')

Ls = [int(x) for x in config.get('main', 'lattice-sizes').split(',')]
start, stop, num = config.get('main', 'probabilities').split(',')
ps = np.linspace(float(start), float(stop), int(num), endpoint=True)

S = np.loadtxt(path / 'S.np').T

fig, ax = plt.subplots()
for L, chi in zip(Ls, S):
    ax.plot(abs(ps - 0.59) * L, chi * L**(7 / 4),
            label=r'$L = {0:d}$'.format(L))

ax.grid()
ax.set(xlabel='Probability $p$',
       ylabel='Avg. Cluster Size per Lattice Point $S$',
       title='Finite Size Scaling')
ax.legend()
plt.show()
