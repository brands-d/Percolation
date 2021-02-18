import numpy as np


def bootstrap_mean(sample, num=1000):
    bootstrap_samples = np.random.choice(sample, replace=True,
                                         size=(num, len(sample)))
    means = np.sort(np.mean(bootstrap_samples, axis=1))
    lower = means[int(num*0.025)]
    higher = means[int(num*0.975)]
    return np.mean(means), lower,higher,np.std(means)
