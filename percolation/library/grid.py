# Third Party Imports
import numpy as np
from numpy.random import choice
import matplotlib.pyplot as plt


class Grid:

    def __init__(self, shape):
        """
        This class encapsulates a regular 2D-square grid (lattice) with
        periodic boundary conditions in each direction.

        :param shape: Shape of the grid as a list of two ints. First int is the
                      number of rows, second number of columns.
        """

        # The percolation state of each site in the grid
        self.config = np.zeros(shape, dtype=np.bool_)

    @property
    def size(self):
        """
        Returns the number of points on the lattice.

        :return int: Size of the lattice.
        """

        return self.config.size

    @property
    def shape(self):
        """
        Returns the shape of the lattice.

        :return int, int: Shape of the square lattice (row, column).
        """

        return self.config.shape

    @property
    def N(self):
        """
        Returns the number of rows in the lattice.

        :return int: Number of rows.
        """

        return self.shape[0]

    @property
    def M(self):
        """
        Returns the number of columns in the lattice.

        :return int: Number of columns.
        """

        return self.shape[1]

    def __getitem__(self, coor):
        """
        Returns the state of the lattice point at corr coordinate.

        :param coor: Tuple of two int coordinates x and y.

        :return bool: State of the site.
        """

        return self.config[coor]

    def is_top(self, x, y):
        """
        Returns  whether the site at (x,y) is in the top row.

        :param x: Row index of the site.
        :param y: Column index of the site.

        :return bool: Whether (x,y) is in the top row.
        """

        return True if x == 0 else False

    def is_left(self, x, y):
        """
        Returns  whether the site at (x,y) is in the left column.

        :param x: Row index of the site.
        :param y: Column index of the site.

        :return bool: Whether (x,y) is in the left column.
        """

        return True if y == 0 else False

    def is_bottom(self, x, y):
        """
        Returns  whether the site at (x,y) is in the bottom row.

        :param x: Row index of the site.
        :param y: Column index of the site.

        :return bool: Whether (x,y) is in the bottom row.
        """

        return True if x == (self.N - 1) else False

    def is_right(self, x, y):
        """
        Returns  whether the site at (x,y) is in the right column.

        :param x: Row index of the site.
        :param y: Column index of the site.

        :return bool: Whether (x,y) is in the right column.
        """

        return True if y == (self.M - 1) else False

    def get_top_neighbour(self, x, y):
        """
        Returns the top neighbour of the lattice site (x,y).

        :param x: Row index of the original site.
        :param y: Column index of the original site.

        :return int, int: (x,y) coordinate of the top neighbour.
        """

        x = x - 1 if x > 0 else self.N - 1

        return x, y

    def get_left_neighbour(self, x, y):
        """
        Returns the left neighbour of the lattice site (x,y).

        :param x: Row index of the original site.
        :param y: Column index of the original site.

        :return int, int: (x,y) coordinate of the left neighbour.
        """

        y = y - 1 if y > 0 else self.M - 1

        return x, y

    def get_bottom_neighbour(self, x, y):
        """
        Returns the bottom neighbour of the lattice site (x,y).

        :param x: Row index of the original site.
        :param y: Column index of the original site.

        :return int, int: (x,y) coordinate of the bottom neighbour.
        """

        x = (x + 1) % self.N

        return x, y

    def get_right_neighbour(self, x, y):
        """
         Returns the right neighbour of the lattice site (x,y).

         :param x: Row index of the original site.
         :param y: Column index of the original site.

         :return int, int: (x,y) coordinate of the right neighbour.
         """

        y = (y + 1) % self.M

        return x, y

    def randomize(self, p=0.5):
        """
        Randomizes the configuration with a probability p for each site to be
        occupied.

        :param p: Probability for each site to be occupied (0 <= p <= 1).

        :return None:
        """

        choices = (True, False)
        prob = (p, 1 - p)
        self.config = choice(choices, size=self.shape, replace=True,
                             p=prob)

    def plot(self, ax=None, labels=None):
        if ax is None:
            fig, ax = plt.subplots()

        im = ax.imshow(self.config, cmap='seismic', vmax=2, vmin=-1)

        if labels is not None:
            labels = labels.reshape(self.shape)
            for x in range(self.N):
                for y in range(self.M):
                    ax.text(y, x, labels[x, y], ha='center', va='center',
                            color='k')

        ax.set_xticks(list(range(self.M)))
        ax.set_yticks(list(range(self.N)))
        ax.set_xticklabels(list(range(self.M)))
        ax.set_yticklabels(list(range(self.N)))

        fig.tight_layout()

        return ax
