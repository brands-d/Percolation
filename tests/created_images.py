from percolation.library.grid import Grid
from percolation.model.hk import HoshenKopelman
from percolation.model.measurment import *
from percolation.model.correlation import *

import matplotlib.pyplot as plt

font = {'size': 20}

plt.rc('font', **font)

# N, M, p = 8, 8, 0.4
# grid = Grid((N, M))
# # grid.randomize(p)
# for i in [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 1), (1, 2), (1, 3),
#           (1, 5), (1, 6), (1, 7), (2, 1), (2, 4), (2, 6), (3, 5), (4, 0),
#           (4, 3), (4, 7), (5, 3), (5, 5), (5, 7), (6, 0), (6, 4), (6, 7),
#           (7, 1), (7, 2), (7, 5)]:
#     grid.config[i] = True
#
# ax = grid.plot()
#
# plt.xticks(range(N), range(N))
# plt.yticks(range(M), range(M))
# ax.set_xticks([x - 0.5 for x in range(1, N)], minor=True)
# ax.set_yticks([y - 0.5 for y in range(1, M)], minor=True)
# ax.set(title=r'8x8 Lattice; $p=0.5$')
# plt.grid(which="minor", ls="-", lw=2, c='k')
#
# hk = HoshenKopelman(grid)
#
# hk.setup()
# labels, sizes = hk.run()
#
# ax = grid.plot(labels=labels)
# plt.xticks(range(N), range(N))
# plt.yticks(range(M), range(M))
# ax.set_xticks([x - 0.5 for x in range(1, N)], minor=True)
# ax.set_yticks([y - 0.5 for y in range(1, M)], minor=True)
# ax.set(title=r'8x8 Lattice; $p=0.5$')
# plt.grid(which="minor", ls="-", lw=2, c='k')

#############################
# import matplotlib.pyplot as plt
# from percolation.data_processing.crit_exponents import *
# from percolation.library.bootstraping import bootstrap_mean
# from percolation.model.fss import *
#
# path = '/home/dominik/Desktop/Percolation/output/crit'
# processing = CritExponentEstimator(path)
# S = np.nanmean(processing.S, axis=0)
# sigma = np.nanstd(processing.S, axis=0) / np.sqrt(5000)
# Ls = processing.args['Ls']
# ps = processing.args['ps']
# nu, gamma = 4 / 3, 43 / 18
# pc = 0.5925261050005425
#
# fig, ax = plt.subplots()
# ax.errorbar(scale_p(ps, Ls[0], pc, nu), scale_chi(S[0], Ls[0], nu, gamma),
#             scale_chi(sigma[0], Ls[0], nu, gamma),
#             linestyle='', marker='x', markersize=8, label=r'$N=25$')
# ax.errorbar(scale_p(ps, Ls[1], pc, nu), scale_chi(S[1], Ls[1], nu, gamma),
#             scale_chi(sigma[1], Ls[1], nu, gamma),
#             linestyle='', marker='.', markersize=8, label=r'$N=50$')
# ax.errorbar(scale_p(ps, Ls[2], pc, nu), scale_chi(S[2], Ls[2], nu, gamma),
#             scale_chi(sigma[2], Ls[2], nu, gamma),
#             linestyle='', marker='+', markersize=8, label=r'$N=100$')
# ax.set(xlabel=r'Scaled Probability $N^{1/\nu}*|p-p_c|$',
#        ylabel=r'Susceptibility $N^{-\gamma/\nu}*\chi$')
# ax.legend()
# plt.xlim([-2.2, 2.4])
# ax.grid()

# for data, L,s in zip(S, Ls,sigma):
#     plt.errorbar(scale_p(ps, L, pc, nu), scale_chi(data, L, nu, gamma),
#                  scale_chi(s, L, nu, gamma))

########################

from percolation.library.grid import Grid
from percolation.model.hk import HoshenKopelman
from percolation.model.measurment import *
from percolation.model.correlation import *

import matplotlib.pyplot as plt
import numpy as np

# N, M = 50, 50
# grid = Grid((N, M))
# hk = HoshenKopelman(grid)
# corr = []
ps = np.linspace(0.4, 0.8, 20)
# for p in ps:
#     temp = []
#     for i in range(50):
#         grid.randomize(p)
#         hk.setup()
#         labels, sizes = hk.run()
#         connectivity = get_connectivity(labels,
#                                         sizes.index(max(sizes)) + 1)[1:]
#         out = extract_correlation_length(connectivity)
#         temp.append(out.params['corr'].value)
#     corr.append([np.mean(temp), np.std(temp) / np.sqrt(len(temp))])
#

x = np.loadtxt('corr.txt')
corr = x[:,0]
sigma = x[:,1]
fig, ax = plt.subplots()
ax.errorbar(ps,corr,sigma,
            linestyle='', marker='x', markersize=8)

ax.set(xlabel=r'Probability $p$',
       ylabel=r'Correlation Length $\xi$')

ax.grid()

plt.show()
