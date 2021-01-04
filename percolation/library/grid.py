import numpy as np
from numpy.random import choice


class Grid():

    def __init__(self, shape, periodic=False):
        self.shape = shape
        self.config = np.zeros(self.size, dtype=np.bool_)
        self.periodic = periodic

    def __getitem__(self, i):
        return self.config[i]

    def __repr__(self):
        return self.config.reshape(self.shape).__repr__()

    @property
    def size(self):
        return self.N * self.M

    @property
    def N(self):
        return self.shape[1]

    @property
    def M(self):
        return self.shape[0]

    def mask(self):
        return self.config

    def is_top(self, idx):
        return idx < self.N

    def is_left(self, idx):
        return idx % self.N == 0

    def is_bottom(self, idx):
        return idx >= self.N * (self.M - 1)

    def is_right(self, idx):
        return (idx + 1) % self.N == 0

    def get_top_neighbour(self, idx):
        if self.is_top(idx):
            if self.periodic:
                return idx + self.N * (self.M - 1)
            else:
                return np.nan
        else:
            return idx - self.N

    def get_left_neighbour(self, idx):
        if self.is_left(idx):
            if self.periodic:
                return idx + (self.N - 1)
            else:
                return np.nan
        else:
            return idx - 1

    def get_bottom_neighbour(self, idx):
        if self.is_bottom(idx):
            if self.periodic:
                return idx - self.N * (self.M - 1)
            else:
                return np.nan
        else:
            return idx + self.N

    def get_right_neighbour(self, idx):
        if self.is_right(idx):
            if self.periodic:
                return idx - (self.N - 1)
            else:
                return np.nan
        else:
            return idx + 1

    def randomize(self, p=0.5):
        choices = [True, False]
        self.config = choice(choices, size=self.size, replace=True,
                             p=[p, 1 - p])
