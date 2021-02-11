# Third Party Imports
import numpy as np
from numpy.random import choice


class Grid:

    def __init__(self, shape, periodic=False):
        """
        This class encapsulates the grid (lattice) and provides simple methods
        for the outside to use.

        :param shape: Shape of the grid as a list of two ints. First int is the
                      number of rows, second number of columns.
        :param periodic: Whether the grid is periodic or not.
        """

        self.shape = shape
        self.periodic = periodic
        # The percolation state of each site in the grid (flattened)
        self.config = np.zeros(self.size, dtype=np.bool_)

    @property
    def size(self):
        """
        Returns the number of points on the lattice.

        :return: Size of the lattice.
        """

        return self.N * self.M

    @property
    def N(self):
        """
        Returns the number of columns in the lattice.

        :return: Number of columns.
        """

        return self.shape[1]

    @property
    def M(self):
        """
        Returns the number of rows in the lattice.

        :return: Number of rows.
        """

        return self.shape[0]

    def __getitem__(self, i):
        """
        Returns the state of the ith lattice points.

        :param i: Flat index of the site.

        :return: State of the site.
        """

        return self.config[i]

    def is_top(self, i):
        """
        Whether the site i is in the top row of the lattice.

        :param i: Flat index of the site.

        :return: Whether i is in the top row.
        """

        return i < self.N

    def is_left(self, i):
        """
        Whether the site i is in the left column of the lattice.

        :param i: Flat index of the site.

        :return: Whether i is in the left column.
        """

        return i % self.N == 0

    def is_bottom(self, i):
        """
        Whether the site i is in the bottom row of the lattice.

        :param i: Flat index of the site.

        :return: Whether i is in the bottom row.
        """

        return i >= self.N * (self.M - 1)

    def is_right(self, i):
        """
        Whether the site i is in the right column of the lattice.

        :param i: Flat index of the site.

        :return: Whether i is in the right column.
        """

        return (i + 1) % self.N == 0

    def get_top_neighbour(self, i):
        """
        Returns the top neighbour of the site i or nan if not possible.

        :param i: Flat index of the site.

        :return: Flat index of the top neighbour.
        """

        if self.is_top(i):
            if self.periodic:
                return i + self.N * (self.M - 1)
            else:
                return np.nan
        else:
            return i - self.N

    def get_left_neighbour(self, idx):
        """
         Returns the left neighbour of the site i or nan if not possible.

         :param i: Flat index of the site.

         :return: Flat index of the left neighbour.
         """

        if self.is_left(idx):
            if self.periodic:
                return idx + (self.N - 1)
            else:
                return np.nan
        else:
            return idx - 1

    def get_bottom_neighbour(self, idx):
        """
         Returns the bottom neighbour of the site i or nan if not possible.

         :param i: Flat index of the site.

         :return: Flat index of the bottom neighbour.
         """

        if self.is_bottom(idx):
            if self.periodic:
                return idx - self.N * (self.M - 1)
            else:
                return np.nan
        else:
            return idx + self.N

    def get_right_neighbour(self, i):
        """
         Returns the right neighbour of the site i or nan if not possible.

         :param i: Flat index of the site.

         :return: Flat index of the right neighbour.
         """

        if self.is_right(i):
            if self.periodic:
                return i - (self.N - 1)
            else:
                return np.nan
        else:
            return i + 1

    def randomize(self, p=0.5):
        """
        Randomizes the configuration with a probability p for each site to be
        occupied.

        :param p: Probability for each site to be occupied (0 <= p <= 1)

        :return: None
        """

        choices = [True, False]
        self.config = choice(choices, size=self.size, replace=True,
                             p=[p, 1 - p])
