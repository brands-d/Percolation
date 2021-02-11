import gzip, os, shutil, sys
from configparser import ConfigParser
from argparse import ArgumentParser
from pathlib import Path
from multiprocessing import Pool

import numpy as np

from percolation.library.grid import Grid
from percolation.library.writer import CritWriter
from percolation.library.misc import timeit
from percolation.model.hk import HoshenKopelman


def func(args):
    L, p = args
    grid = Grid((L, L), periodic=True)
    hk = HoshenKopelman(grid)
    grid.randomize(p)
    hk.setup()

    _, sizes = hk.run()
    writer.write(L, p, sizes)


def compress(file_name):
    file_in = path / (file_name + '.txt')
    file_out = path / (file_name + '.gz')
    with open(file_in, 'rb') as f_in:
        with gzip.open(file_out, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    os.remove(file_in)


@timeit
def calc():
    for L in Ls:
        for p in ps:
            with Pool(processors, initializer=init,
                      initargs=(CritWriter(path),)) as pool:
                pool.map(func, num * [[L, p]])

            # compress('L_{0:d}_p_{1:.3f}'.format(L, p))


def init(arg):
    global writer
    writer = arg


if __name__ == '__main__':
    # Parse command line arguments
    parser = ArgumentParser()
    parser.add_argument('-p', '--path',
                        help='Path to the input/output directory.',
                        default='.', required=False)
    args = parser.parse_args()

    # Read input file
    try:
        path = Path(args.path)
        config = ConfigParser()
        config.read(path / 'input.ini')

        processors = int(config.get('main', 'num_processors'))
        Ls = [int(x) for x in config.get('main', 'lattice-sizes').split(',')]
        start, stop, num = config.get('main', 'probabilities').split(',')
        ps = np.linspace(float(start), float(stop), int(num), endpoint=True)
        num = int(config.get('main', 'num_iterations'))

    except:
        print('Something went wrong. Make sure to have a valid config file'
              'named "input.ini" in the directory passed.')
        sys.exit()

    calc()