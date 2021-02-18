# Third Party Imports
import numpy as np

# Own Imports
from ..library.oneindexedlist import OneIndexedList
from ..library.misc import timeit


class HoshenKopelman:

    def __init__(self, grid):
        """
        This class encapsulates the cluster finding and labelling via the
        Hoshen-Kopelman algorithm.

        :param grid: Grid to be classified. Has to be a subclass of
                     ..library.grid.
        """

        self.grid = grid

    def setup(self):
        """
        Sets the class up for a run. Can be called after changing the grid
        again such that you do not need multiple instances of this class.

        :return None:
        """

        # labels is flat array the size of grid. Contains the cluster label for
        # each lattice site. If site is not occupied or not yet attributed to
        # a cluster the label will be 0
        self.labels = np.zeros(self.grid.size, dtype=np.int_)
        # An empty list (starting index is 1 not 0!) that will contain the
        # size of each cluster or the reference to its root cluster
        self.sizes = OneIndexedList()

    def run(self):
        """
        Starts the algorithm, classifies all lattice sites and returns the
        labels as well as sizes for each cluster.

        :return list, list: The first list contains the labels for each
                            lattice site (or 0 for unoccupied ones).
                            The second list contains the size for each label.
        """

        # Go through all lattice sites individually, starting from the top
        # left (row major).
        for i in range(self.grid.size):
            self.classify(i)

        self.compactify_cluster()

        return self.labels.reshape(self.grid.shape), self.sizes

    def classify(self, i):
        """
        Classifies (i.e. labels) i-th site.

        :param i: Flatted index of the site which is to be classified.

        :return None:
        """

        x, y = np.unravel_index(i, self.grid.shape)

        if not self.grid[x, y]:
            # ==> lattice site is not occupied --> do nothing
            return

        # ==> lattice site is occupied
        # Get neighbour to the top and to the left of the site
        top = self.grid.get_top_neighbour(x, y)
        left = self.grid.get_left_neighbour(x, y)

        if not self.grid.is_top(x, y) and self.grid[top]:
            # ==> site is not in the top row and its top neighbour is occupied
            if not self.grid.is_left(x, y) and self.grid[left]:
                # ==> site is not in the left most column and the neighbour to
                # the left is occupied ==> both neighbours are occupied and
                # are part of a cluster already --> get their root labels
                top_root = self.find(*top)
                left_root = self.find(*left)

                if top_root != left_root:
                    # ==> they are not part of the same cluster already
                    # --> use smaller root label as label for the site
                    roots = np.sort((top_root, left_root))
                    self.labels[i] = roots[0]
                    # This site is the bridge between the two previously
                    # separated clusters --> union those two
                    self.union(*roots)
                    # Add this site to the size of the root cluster
                    self.sizes[roots[0]] += 1
                else:
                    # ==> top and left neighbour are already part of the same
                    # cluster --> add this site to it
                    self.labels[i] = left_root
                    self.sizes[left_root] += 1

            else:
                # ==> only the top neighbour is occupied --> site gets part of
                # this cluster
                L = self.find(*top)
                self.labels[i] = L
                self.sizes[L] += 1

        elif not self.grid.is_left(x, y) and self.grid[left]:
            # ==> only the left neighbour is occupied --> site gets part of
            # this cluster
            L = self.find(*left)
            self.labels[i] = L
            self.sizes[L] += 1

        else:
            # ==> neither neighbour is occupied --> new cluster
            # Add this new cluster to the list of clusters (sizes)
            self.sizes.append(1)
            self.labels[i] = len(self.sizes)

        if self.grid.is_right(x, y):
            # ==> this site is in the right column
            right = self.grid.get_right_neighbour(x, y)
            if self.grid[right]:
                # ==> the site in the left column (this sites right neighbour)
                # is occupied and thus already in a cluster. Combine the two
                # clusters (similar to above)
                right_root = self.find(*right)
                self_root = self.find(x, y)
                if self_root != right_root:
                    roots = np.sort((right_root, self_root))
                    self.union(*roots)

        if self.grid.is_bottom(x, y):
            # ==> site is in the bottom row
            bottom = self.grid.get_bottom_neighbour(x, y)
            if self.grid[bottom]:
                # ==> site in top row is occupied --> unify the two clusters
                # (see above)
                bottom_root = self.find(*bottom)
                self_root = self.find(x, y)
                if self_root != bottom_root:
                    roots = np.sort((bottom_root, self_root))
                    self.union(*roots)

    def find(self, x, y):
        """
        Finds the label of the root cluster the lattice site at (x,y)
        is part of.

        :param x: Row index of the site.
        :param y: Column index of the site.

        :return int: Root label.
        """

        i = np.ravel_multi_index((x, y), self.grid.shape)
        # Get the label of the lattice site
        l = self.labels[i]

        return self.find_by_label(l)

    def find_by_label(self, l):
        """
        Finds the root label of the label l.

        :param l: Label.

        :return int: Root label.
        """

        # If the size of the cluster label (which is also the index of the
        # cluster in the size array) is negative, then it's absolute value is
        # its root cluster (which in turn could have a root cluster => while)
        while self.sizes[l] < 0:
            l = -self.sizes[l]

        return l

    def union(self, l_i, l_j):
        """
        Unifies the cluster with the label l_i and the cluster with the label
        l_j.

        :param l_i: Label of the first cluster (root cluster).
        :param l_j: Label of the second cluster (non root cluster).

        :return None:
        """

        # Add the size of the non root cluster to the root clusters size
        self.sizes[l_i] += self.sizes[l_j]
        # Set the size of the non root cluster as a reference (negative value)
        # to the root cluster
        self.sizes[l_j] = -l_i

    def compactify_cluster(self):
        """
        'Cleans' the labels and sizes arrays. Both still contain non root
        clusters. Combines all clusters with their root clusters and relabels
        them if necessary. Sets sizes array to a regular list!

        :return None:
        """

        # Firstly, change all labels to their root labels
        # Go through all clusters. l is its improper label, size its size
        for l, size in zip(range(1, len(self.sizes) + 1), self.sizes):
            if size < 0:
                # ==> this cluster is not a root cluster
                root = self.find_by_label(l)
                # Rename all occurrences of this cluster label to the root
                # cluster label
                self.labels[self.labels == l] = root

        # Secondly, relabel clusters to remove gaps in the cluster numbering
        # aux holds the proper (desired) cluster labelling (i.e. no gaps)
        aux = 1
        for l, size in zip(range(1, len(self.sizes) + 1), self.sizes):
            if size < 0:
                continue

            self.labels[self.labels == l] = aux
            aux += 1

        # Clean sizes array by only keeping non negative entries (i.e. roots)
        self.sizes = [l for l in self.sizes if l > 0]
