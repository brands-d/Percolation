import numpy as np
from numpy.random import choice


class Grid():

    def __init__(self, shape, periodic=False):
        self.config = np.zeros(shape=shape, dtype=np.bool_)
        self.periodic = periodic

    @property
    def shape(self):
        return self.config.shape

    @property
    def M(self):
        return self.config.shape[0]

    @property
    def N(self):
        return self.config.shape[1]

    def is_top(self, idx):
        return idx < self.N

    def is_bottom(self, idx):
        return idx >= self.N * (self.M - 1)

    def is_left(self, idx):
        return idx % self.N == 0

    def is_right(self, idx):
        return idx % self.N == self.N - 1

    def get_top_neighbour(self, idx):
        if self.is_top(idx):
            if self.periodic:
                return idx + self.N * (self.M - 1)
            else:
                return np.nan
        else:
            return idx - self.N

    def get_bottom_neighbour(self, idx):
        if self.is_bottom(idx):
            if self.periodic:
                return idx - self.N * (self.M - 1)
            else:
                return np.nan
        else:
            return idx + self.N

    def get_left_neighbour(self, idx):
        if self.is_left(idx):
            if self.periodic:
                return idx + (self.N - 1)
            else:
                return np.nan
        else:
            return idx - 1

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
        self.config = choice(choices, size=self.shape, replace=True,
                             p=[p, 1 - p])
