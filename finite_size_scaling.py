from pathlib import Path
from configparser import ConfigParser

import numpy as np
import matplotlib.pyplot as plt
from lmfit import fit_report

from percolation.model.ffs import ffs, scale_chi, scale_p

path = Path('/home/dominik/Desktop/Percolation/output/04.01.2021')
config = ConfigParser()
config.read(path / 'input.ini')

Ls = [int(x) for x in config.get('main', 'lattice-sizes').split(',')]
start, stop, num = config.get('main', 'probabilities').split(',')
ps = np.linspace(float(start), float(stop), int(num), endpoint=True)

S = np.loadtxt(path / 'S.np').T

out = ffs(S, Ls, ps)
print(fit_report(out))
pc = out.params['pc'].value
nu = out.params['nu'].value
gamma = out.params['gamma'].value

fig, ax = plt.subplots()
for L, chi in zip(Ls, S):
    x = scale_p(ps, L, pc, nu)
    y = scale_chi(chi, L, nu, gamma)
    ax.plot(x, y, label=r'$L = {0:d}$'.format(L))

ax.grid()
ax.set(xlabel='Probability $p$',
       ylabel='Avg. Cluster Size per Lattice Point $S$',
       title='Finite Size Scaling')
ax.legend()
plt.show()
