from pathlib import Path
from configparser import ConfigParser
from multiprocessing import Pool

import numpy as np

from percolation.library.grid import Grid
from percolation.model.hk import HoshenKopelman
from percolation.model.measurment import get_susceptibility


class SusceptDataCollector:

    def __init__(self, path):
        self.args = {'path': Path(path)}

        self.read_input()

    def read_input(self):
        config = ConfigParser()
        config.read(self.args['path'] / 'input.ini')

        processors = int(config.get('main', 'num_processors'))
        Ls = [int(x) for x in config.get('main', 'lattice-sizes').split(',')]
        start, stop, num = config.get('main', 'probabilities').split(',')
        ps = np.linspace(float(start), float(stop), int(num), endpoint=True)
        num = int(config.get('main', 'num_iterations'))

        self.args.update({'processors': processors,
                          'Ls': Ls, 'ps': ps, 'num': num})

    def run(self):
        with Pool(self.args['processors']) as pool:
            pool.map(self.func, self.args['ps'])

    def func(self, p):
        S = np.zeros((len(self.args['Ls']), self.args['num']), dtype=np.float_)

        for i, L in enumerate(self.args['Ls']):
            grid = Grid((L, L))
            hk = HoshenKopelman(grid)

            for j in range(self.args['num']):
                grid.randomize(p)
                hk.setup()
                _, sizes = hk.run()
                S[i, j] = get_susceptibility(sizes)

        file_path = self.args['path'] / f'p_{p:.3f}.csv'
        np.savetxt(file_path, S.T, delimiter=',')
