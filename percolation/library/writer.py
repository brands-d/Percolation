import multiprocessing
import gzip


class Writer():

    def __init__(self, path):
        self.path = path
        self.write_lock = multiprocessing.Lock()

    def write(self, L, p, sizes):
        with self.write_lock:
            file_name = self.path / 'L_{0:d}_p_{1:.3f}.txt'.format(L, p)
            with open(file_name, 'a+') as file:
                for s in sizes[:-1]:
                    file.write('{0:d},'.format(s))

                if len(sizes) != 0:
                    file.write('{0:d}\n'.format(sizes[-1]))
                else:
                    file.write('\n')
