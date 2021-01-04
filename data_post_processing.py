import os
from pathlib import Path

import numpy as np

from percolation.library.misc import get_susceptibility


def get_parameters(files):
    Ls = []
    ps = []

    for file in files:
        _, L, _, p = file[:-4].split('_')

        L = int(L)
        if L not in Ls:
            Ls.append(L)

        p = float(p)
        if p not in ps:
            ps.append(p)

    return np.sort(Ls), np.sort(ps)


def line_to_list(line):
    if len(line) == 1:
        return []

    else:
        temp = line.split(',')
        sizes = [int(x) for x in temp[:-1]]
        sizes.append(int(temp[-1][:-1]))

        return sizes


def process_file(file_name, L):
    S = []

    try:
        with open(file_name) as file:
            for line in file:
                sizes = line_to_list(line)
                S.append(get_susceptibility(sizes, L))

        return np.mean(S)

    except FileNotFoundError:
        return np.nan


if __name__ == '__main__':
    path = Path('./output/04.01.2021')

    # Find all output files
    files = [file for file in os.listdir(path) if file.endswith('.txt')]
    Ls, ps = get_parameters(files)
    S = np.empty(shape=(len(ps), len(Ls)), dtype=np.float_) * np.nan

    for i, L in enumerate(Ls):
        for j, p in enumerate(ps):
            file_name = path / 'L_{0:d}_p_{1:.3f}.txt'.format(L, p)
            S[j, i] = process_file(file_name, L)

    np.savetxt(path / 'S.np', S)
