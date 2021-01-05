from itertools import combinations

import numpy as np
from scipy.interpolate import interp1d
from lmfit import minimize, Parameters


def ffs(S, Ls, ps):
    params = Parameters()
    params.add('pc', value=0.59)
    params.add('gamma', value=43 / 18)
    params.add('nu', value=4 / 3)

    return minimize(residual, params, args=(S, Ls, ps))


def residual(params, S, Ls, ps):
    pc = params['pc']
    nu = params['nu']
    gamma = params['gamma']

    x = []
    y = []
    for L, chi in zip(Ls, S):
        x.append(scale_p(ps, L, pc, nu))
        y.append(scale_chi(chi, L, nu, gamma))

    x = np.array(x)
    y = np.array(y)

    min_ = np.nanmax(x.T[0])
    max_ = np.nanmin(x.T[-1])
    x_new = np.linspace(min_, max_, len(x[0]), endpoint=True)
    y_new = []
    for i in range(len(x)):
        inter = interp1d(x[i], y[i], kind='linear', bounds_error=False)
        y_new.append(inter(x_new))

    residual = []
    for combo in combinations(range(len(Ls)), 2):
        temp = (y_new[combo[0]] - y_new[combo[1]])**2
        residual.append(temp)

    return np.nansum(residual, axis=0)


def scale_p(p, L, pc, nu):
    return (p - pc) * L**(1 / nu)


def scale_chi(chi, L, nu, gamma):
    return chi / L**(gamma / nu)
