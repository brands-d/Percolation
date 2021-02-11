# Third Party Imports
import numpy as np

# Own Imports
from ..library.misc import OneIndexedList


class HoshenKopelman:

    def __init__(self, grid):
        """
        This class encapsulates the cluster finding and labelling via the
        Hoshen-Kopelman algorithm.

        :param grid: Has to be a subclass of ..library.grid.
        """

        self.grid = grid

    def setup(self):
        """
        Sets the class up for a run. Can be called after changing the grid
        again such that you do not need multiple instances of this class.

        :return: None
        """

        # labels is flat array the size of grid. Contains the cluster label for
        # each lattice site. If site is not occupied or not yet attributed to
        # a cluster the label will be 0
        self.labels = np.zeros(self.grid.size, dtype=np.int_)
        # Highest cluster label number in use so far. First cluster will be
        # labelled 1
        self.largest_label = 0
        # A empty list (OneIndexedList is a custom subclass of list with a
        # starting index of 1 instead of 0 to better suit the problem) that
        # will contain the size of each cluster or the reference to its root
        # cluster
        self.sizes = OneIndexedList()

    def run(self):
        """
        Starts the algorithm, classifies all lattice sites and returns the
        labels as well as sizes for each site/cluster.

        :return: labels, sizes: The labels array containing the labels for each
                                lattice site (or 0 for unoccupied ones) and the
                                sizes for each cluster label as list.
        """

        # Go through all lattice sites individually, starting from the top
        # left row major
        for i in range(self.grid.size):
            self.classify(i)

        self.compactify_cluster()
        return self.labels, self.sizes

    def classify(self, i):
        """
        Classifies (i.e. labels) the site with the (flat) index i.

        :param i: Flat index of the site to be labeled.

        :return: None
        """

        if not self.grid[i]:
            # ==> lattice site is not occupied --> do nothing
            return

        # ==> lattice site is occupied
        # Get neighbour to the top and to the left of the site
        top = self.grid.get_top_neighbour(i)
        left = self.grid.get_left_neighbour(i)

        if not self.grid.is_top(i) and self.grid[top]:
            # ==> site is not in the top row and its top neighbour is occupied
            if not self.grid.is_left(i) and self.grid[left]:
                # ==> site is not in the left most column and the neighbour to
                # the left is occupied ==> both neighbours are occupied and
                # are part of a cluster already --> get their root labels
                top_root = self.find(top)
                left_root = self.find(left)

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
                L = self.find(top)
                self.labels[i] = L
                self.sizes[L] += 1

        elif not self.grid.is_left(i) and self.grid[left]:
            # ==> only the left neighbour is occupied --> site gets part of
            # this cluster
            L = self.find(left)
            self.labels[i] = L
            self.sizes[L] += 1

        else:
            # ==> neither neighbour is occupied --> new cluster
            self.largest_label += 1
            self.labels[i] = self.largest_label
            # Add this new cluster to the list of clusters (sizes)
            self.sizes.append(1)

        if self.grid.periodic and self.grid.is_right(i):
            # ==> grid is periodic and this site is in the right column
            right = self.grid.get_right_neighbour(i)
            if self.grid[right]:
                # ==> the site in the left column (this sites right neighbour)
                # is occupied and thus already in a cluster. Combine the two
                # clusters (similar to above)
                right_root = self.find(right)
                self_root = self.find(i)
                if self_root != right_root:
                    roots = np.sort((right_root, self_root))
                    self.union(*roots)

        if self.grid.periodic and self.grid.is_bottom(i):
            # ==> grid is periodic and this site is in the bottom row
            bottom = self.grid.get_bottom_neighbour(i)
            if self.grid[bottom]:
                # ==> site in top row is occupied --> unify the two clusters
                # (see above)
                bottom_root = self.find(bottom)
                self_root = self.find(i)
                if self_root != bottom_root:
                    roots = np.sort((bottom_root, self_root))
                    self.union(*roots)

    def find(self, i, label=False):
        """
        Finds the label of the root cluster the lattice site i is part of.

        :param i: Flat index of the lattice site which root is to be found.
        :param label: Boolean whether i is an index of a lattice site or
                      already a label of a (possibly non root) cluster.

        :return: Root label.
        """

        # Get the label of the lattice site if i is not a label
        l = i if label else self.labels[i]
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

        :return: None
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
        them if necessary.

        :return: None
        """

        # aux holds the proper (desired) cluster labelling (i.e. no gaps)
        aux = 1
        # Go through all clusters. l is its improper label, size its size
        for l, size in zip(range(1, len(self.sizes) + 1), self.sizes):
            if size < 0:
                # ==> this cluster is not a root cluster
                root = self.find(l, label=True)
                # Rename all occurrences of this cluster label to the root
                # cluster label
                self.labels[self.labels == l] = root

            elif l != aux:
                # ==> this cluster is root but not labelled properly --> rename
                self.labels[self.labels == l] = aux
                aux += 1

            else:
                # ==> cluster is correctly labelled
                aux += 1

        # Clean sizes array by only keeping non negative entries (i.e. roots)
        self.sizes = [l for l in self.sizes if l > 0]
