import time

import numpy as np


class OneIndexedList(list):
    def __getitem__(self, i):
        return super().__getitem__(i - 1)

    def __setitem__(self, i, value):
        return super().__setitem__(i - 1, value)


def timeit(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()

        print('Execution Time ({0}): {1:.5f} seconds'.format(
            func.__name__, end_time - start_time))

        return result

    return wrapper


def get_susceptibility(data, L):
    if len(data) == 0:
        return np.nan

    else:
        data.remove(max(data))

    sizes = np.array(list(set(data)))
    L_2 = L**2
    n_s = []

    for size in sizes:
        n_s.append(data.count(size) / L_2)

    temp = sizes * n_s
    S = np.sum(sizes * temp) / np.sum(temp)

    return S
