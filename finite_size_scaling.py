from pathlib import Path
from configparser import ConfigParser

import numpy as np
import matplotlib.pyplot as plt
from lmfit import fit_report

from percolation.model.ffs import ffs, scale_chi, scale_p

path = Path('/home/dominik/Desktop/Percolation/output/ffs')
config = ConfigParser()
config.read(path / 'input.ini')

Ls = 25, 50, 100, 150, 200
ps = np.linspace(0, 0.392, 50, endpoint=True).tolist() + \
     np.linspace(0.4, 0.8, 101, endpoint=True).tolist() + \
     np.linspace(0.808, 1, 25, endpoint=True).tolist()

S = np.loadtxt(path / 'S.np').T

out = ffs(S, Ls, ps)
print(fit_report(out))
pc = out.params['pc'].value
nu = out.params['nu'].value
gamma = out.params['gamma'].value

colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:gray', 'tab:red']
symbols = ['.', '+', 'x', 'h', '^']
i = 0
fig, ax = plt.subplots()
for L, chi in zip(Ls, S):
    x = scale_p(ps, L, pc, nu)
    y = scale_chi(chi, L, nu, gamma)
    ax.plot(x,y, label=r'$L = {0:d}$'.format(L), marker=symbols[i],
            color=colors[i], linestyle='None')
    i += 1

ax.grid()
plt.title(r'Unscaled Data', fontsize=24)
plt.xlabel(r'Probability $p$', fontsize=22)
plt.ylabel(r'Susceptibility $S$', fontsize=22)
ax.tick_params(axis='both', which='major', labelsize=15)
#ax.tick_params(axis='both', which='minor', labelsize=8)
ax.legend(fontsize=22)
plt.show()
