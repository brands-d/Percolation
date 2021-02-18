from itertools import combinations

import numpy as np
from scipy.interpolate import interp1d
from lmfit import minimize, Parameters, fit_report


def fss(S, Ls, ps, vary_exponents=False):
    """
    Estimates the critical exponents gamma and nu as well as the critical
    threshold pc via finite size scaling.

    :param S: A matrix with len(Ls) rows and len(ps) columns. Each entry is the
              susceptibility for the system with the corresponding size L and
              occupation probability p.
    :param Ls: List of integers denoting the system sizes the rows of S
               correspond to.
    :param ps: List of floats denoting the probabilities for the columns of S.
    :param vary_exponents: Boolean whether to vary and find optimal critical
                           exponents or fixate them at the "true" value.
    :return MinimizerResult: Minimizing result from lmfit with the estimated
                             critical exponents and probability threshold.
    """

    params = Parameters()
    params.add('pc', value=0.5927)
    params.add('gamma', value=43 / 18, vary=vary_exponents)
    params.add('nu', value=4 / 3, vary=vary_exponents)

    out = minimize(residual, params, args=(S, Ls, ps))

    return out


def residual(params, S, Ls, ps):
    """
     Residual method for the finite size scaling.

     :param params: A lmfit parameter set with a critical exponent nu, gamma
                    and the critical threshold pc.
     :param S: A matrix with len(Ls) rows and len(ps) columns. Each entry is the
              susceptibility for the system with the corresponding size L and
              occupation probability p.
     :param Ls: List of integers denoting the system sizes the rows of S
               correspond to.
     :param ps: List of floats denoting the probabilities for the columns of S.

     :return list: Array with the sum of the pair wise absolute differences
                   between all data series.
     """

    pc = params['pc'].value
    nu = params['nu'].value
    gamma = params['gamma'].value

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
        temp = abs(y_new[combo[0]] - y_new[combo[1]])
        residual.append(temp)

    return np.nansum(residual, axis=0)


def scale_p(p, L, pc, nu):
    """
     Scales the probability p according to finite size scaling.

     :param p: List of values p to be scaled.
     :param L: System size.
     :param pc: Critical threshold.
     :param nu: Critical exponent.

     :return list: Scaled probabilites.
     """

    return (p - pc) * L**(1 / nu)


def scale_chi(chi, L, nu, gamma):
    """
     Scales the susceptibility chi according to finite size scaling.

     :param chi: List of values chi to be scaled.
     :param L: System size.
     :param nu: Critical exponent.
     :param gamma: Critical exponent.

     :return list: Scaled probabilites.
     """

    return chi / L**(gamma / nu)
