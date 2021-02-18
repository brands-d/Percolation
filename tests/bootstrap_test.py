import bootstrapped.bootstrap as bs
import bootstrapped.stats_functions as bs_stats
import itertools
import numpy as np
from sklearn.utils import resample
from percolation.library.bootstraping import *

lam_true = 1
org_sample = np.random.poisson(1, size=500)
num = 1000
mean, std = bootstrap_mean(org_sample, num)
print(mean, std)
print(abs(mean - 1) / std)
print(bs.bootstrap(org_sample, stat_func=bs_stats.mean, num_iterations=num))
