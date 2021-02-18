import matplotlib.pyplot as plt
import bootstrapped.bootstrap as bs
import bootstrapped.stats_functions as bs_stats

from percolation.data_collection.susceptibility import *
from percolation.data_processing.crit_exponents import *
from percolation.library.bootstraping import bootstrap_mean

path = '/home/dominik/Desktop/Percolation/output/crit'

collector = SusceptDataCollector(path)
# collector.run()

processing = CritExponentEstimator(path)
#pc = processing.estimate()
pc = np.loadtxt('pcs.txt')
print(*bootstrap_mean(pc, num=100000))
print(bs.bootstrap(pc, stat_func=bs_stats.mean))
