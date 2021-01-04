import numpy as np

from percolation.library.misc import OneIndexedList, timeit


class HoshenKopelman():

    def __init__(self, grid):
        self.grid = grid

    def setup(self):
        self.labels = np.zeros(self.grid.size, dtype=np.int_)
        self.largest_label = 0
        self.sizes = OneIndexedList()

    # @timeit
    def run(self):
        for i in range(self.grid.size):
            self.classify(i)

        self.compactify_cluster()
        return self.labels, self.sizes

    def classify(self, i):
        if self.grid[i]:
            # Lattice point is occupied
            # Get neighbour to the top and to the left as grid index
            top = self.grid.get_top_neighbour(i)
            left = self.grid.get_left_neighbour(i)

            if not self.grid.is_top(i) and self.grid[top]:
                if not self.grid.is_left(i) and self.grid[left]:
                    # Both left and top neighbour exist and are occupied,
                    # thus are already part of a cluster
                    top_root = self.find(top)
                    left_root = self.find(left)
                    if top_root != left_root:
                        # Assign smaller root label and unify labels
                        roots = np.sort((top_root, left_root))
                        self.labels[i] = roots[0]
                        self.union(*roots)
                        self.sizes[roots[0]] += 1
                    else:
                        # Top and left neighbour are part of the same cluster
                        self.labels[i] = left_root
                        self.sizes[left_root] += 1

                else:
                    # Only top neighbour exists and is occupied
                    L = self.find(top)
                    self.labels[i] = L
                    self.sizes[L] += 1

            elif not self.grid.is_left(i) and self.grid[left]:
                # Only left neighbour exists and is occupied
                L = self.find(left)
                self.labels[i] = L
                self.sizes[L] += 1

            else:
                # Neither neighbour exists and is occupied -> new cluster
                self.largest_label += 1
                self.labels[i] = self.largest_label
                self.sizes.append(1)

            if self.grid.periodic and self.grid.is_right(i):
                right = self.grid.get_right_neighbour(i)
                if self.grid[right]:
                    # Lattice is periodic, the point is at the end of the row
                    # and the start of the row is in a cluster -> unify both
                    right_root = self.find(right)
                    self_root = self.find(i)
                    if self_root != right_root:
                        roots = np.sort((right_root, self_root))
                        self.union(*roots)

            if self.grid.periodic and self.grid.is_bottom(i):
                bottom = self.grid.get_bottom_neighbour(i)
                if self.grid[bottom]:
                    # Lattice is periodic, the point is at the end of the col
                    # and the start of the col is in a cluster -> unify both
                    bottom_root = self.find(bottom)
                    self_root = self.find(i)
                    if self_root != bottom_root:
                        roots = np.sort((bottom_root, self_root))
                        self.union(*roots)

    def find(self, i, L=False):
        L = i if L else self.labels[i]
        while self.sizes[L] < 0:
            L = -self.sizes[L]

        return L

    def union(self, L_i, L_j):
        self.sizes[L_i] += self.sizes[L_j]
        self.sizes[L_j] = -L_i

    def compactify_cluster(self):
        aux = 1
        for L, size in zip(range(1, len(self.sizes) + 1), self.sizes):
            if size < 0:
                root = self.find(L, L=True)
                self.labels[self.labels == L] = root
            elif L != aux:
                self.labels[self.labels == L] = aux
                aux += 1
            else:
                aux += 1

        self.sizes = [L for L in self.sizes if L > 0]
