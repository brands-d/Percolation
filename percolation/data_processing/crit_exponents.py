from pathlib import Path
from configparser import ConfigParser

import numpy as np

from percolation.model.fss import fss


class CritExponentEstimator:

    def __init__(self, path):
        self.args = {'path': Path(path)}

        self.read_input()
        self.read_output()

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

    def read_output(self):
        self.S = np.zeros((len(self.args['ps']), self.args['num'],
                           len(self.args['Ls'])), dtype=np.float_)

        for i, p in enumerate(self.args['ps']):
            file_path = self.args['path'] / f'p_{p:.3f}.csv'
            self.S[i, :, :] = np.loadtxt(file_path, delimiter=',')

        self.S = np.swapaxes(self.S, 0, 1)
        self.S = np.swapaxes(self.S, 1, 2)

    def estimate(self):
        pc = []

        for data in self.S:
            out = fss(data, self.args['Ls'], self.args['ps'],
                      vary_exponents=False)
            pc.append(out.params['pc'].value)

        return np.array(pc)
