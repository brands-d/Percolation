import numpy as np
from lmfit import minimize, Parameters, fit_report


def residual_correlation(params, connectiviy, r):
    """
     Residual method for the correlation length fitting.

     :param params: A lmfit parameter set with a correlation length corr and a
                    pre factor A.
     :param connectivity: List of values of the correlation function at
                          different r.
     :param r: Distances r the connectivity array contains the value of the
               correlation function.

     :return list: Array with the residual: model - data.
     """

    corr = params['corr'].value
    A = params['A'].value

    return model_corr(r, corr, A) - connectiviy


def model_corr(r, corr, A):
    """
     Correlation function model.

     :param r: The distances r between two occupied sites.
     :param corr: Correlation length.
     :param A: Pre factor.

     :return float: Value of the correlation function at r.
     """

    return A * np.exp(-r / corr)


def extract_correlation_length(connectivity):
    """
     Estimates the correlation length by fitting an exponential decay:
         A*exp(-r/corr)
     to the two point correlation function.

     :param connectivity: List of values of the correlation function at r=1 to
                          r=len(connectivity).

     :return MinimizerResult: Minimizing result from lmfit with the estimated
                              correlation length and the pre factor.
     """

    params = Parameters()
    params.add('A', value=1)
    params.add('corr', value=1, min=0)

    r = np.array(range(1, len(connectivity)+1))
    out = minimize(residual_correlation, params, args=(connectivity, r))

    return out
