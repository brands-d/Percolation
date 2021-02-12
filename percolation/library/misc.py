import time

import numpy as np


def timeit(func):
    """
    Simple wrapper to time a function. Prints the execution time after the
    method finishes.
    """

    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()

        print('Execution Time ({0}): {1:.5f} seconds'.format(
            func.__name__, end_time - start_time))

        return result

    return wrapper


def manhattan_distance(shape, center):
    """
    Returns the distance for each entry in a matrix from the center according
    to the Manhatten (taxicab) metric and periodic boundary conditions.

    :param shape: Shape of the matrix. Row first.
    :param center: Which entry is the origin. Starting from top left, first
                   component is the row, second the column.

    :return ndarray: 2D ndarray with shape entered. Each entry has its shortest
                     distance from the entered center. Only integers since
                     as metrix the Manhatten metric is used.
    """

    x0, y0 = center
    N, M = shape

    # Calculate distance in x direction
    dx = np.abs(np.arange(N) - x0)
    # If distance is too large going the other way (periodic boundary) is
    # shorter
    dx[dx > N / 2] = N - dx[dx > N / 2]

    # Same in the y direction
    dy = np.abs(np.arange(M) - y0)
    dy[dy > M / 2] = M - dy[dy > M / 2]

    # Add the distances (like a meshgrid)
    r = dy + np.array([dx]).T

    return r
