import matplotlib.pyplot as plt
from percolation.data_processing.crit_exponents import *
from percolation.library.bootstraping import bootstrap_mean
from percolation.model.fss import *
from lmfit import minimize, Parameters, fit_report

font = {'size': 20}

plt.rc('font', **font)

path = '/output/crit'
processing = CritExponentEstimator(path)
S = np.nanmean(processing.S, axis=0)
Ls = processing.args['Ls']
ps = processing.args['ps']
sigma = np.nanstd(processing.S, axis=0) / np.sqrt(5000)
nu = 4 / 3
S = S[-1]
sigma = sigma[-1]
pc = 0.57959
# pc = 0.5927
# S = S[:20]
# ps = ps[:20]
# sigma = sigma[:20]
# params = Parameters()
# params.add('gamma', value=43 / 18)
# params.add('A', value=1)
#
#
# def residual(params):
#     A = params['A'].value
#     gamma = params['gamma'].value
#     resi = abs(S - A * abs(ps - pc)**(-gamma))/sigma
#
#     return resi

#
# out = minimize(residual, params)
# print(fit_report(out))
# gamma = out.params['gamma'].value
# A = out.params['A'].value
# plt.plot(ps, S)
# plt.plot(ps, A * abs(ps - pc)**(-gamma))


fig, ax = plt.subplots()
ax.errorbar(ps[20:24], S[20:24], sigma[20:24], linestyle='', marker='x',
            markersize=8, color='tab:blue', alpha=.5)
fit1, = ax.plot(ps[24:], 0.092 * abs(ps[24:] - pc)**(-1.783), linestyle='-',
               color='tab:orange')
fit2, = ax.plot(ps[:20], 0.764 * abs(ps[:20] - pc)**(-1.604), linestyle='-',
               color='tab:green')

S = np.delete(S, (20, 21, 22, 23))
ps = np.delete(ps, (20, 21, 22, 23))
sigma = np.delete(sigma, (20, 21, 22, 23))

data = ax.errorbar(ps, S, sigma, linestyle='', marker='x', markersize=12,
                   color='tab:blue')
line1 = ax.axvline(x=0.5927, color='k',
                   linestyle='--')
line2 = ax.axvline(x=pc, color='k',
                   linestyle='-')
ax.set(xlabel=r'Probability $p$',
       ylabel=r'Susceptibility $\chi$')

ax.legend(handles=[data, fit1, fit2, line1, line2],
          labels=['Data', 'Left Fit', 'Right Fit',
                  r'Critical Threshold $p_c$',
                  r'Literature Value $p_c$'])
ax.grid()
plt.show()
