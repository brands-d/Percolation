import numpy as np

from ..library.misc import manhattan_distance


def get_susceptibility(clusters):
    """
    Returns the susceptibility for site percolation from cluster sizes.

    :param list: List cluster sizes.

    :return float: Susceptibility - average size of a finite cluster. All
                   clusters except the largest one are considered 'finite'.
                   If the list is empty nan is returned.
    """

    # If there is no or only one cluster then there is no finite cluster
    if len(clusters) <= 1:
        return np.nan

    # Remove largest, i.e. infinite, cluster
    clusters.remove(max(clusters))

    sizes = np.array(list(set(clusters)))
    n_s = []

    for size in sizes:
        n_s.append(clusters.count(size))

    temp = sizes * n_s
    S = np.sum(sizes * temp) / np.sum(temp)

    return S


def get_p_inf(clusters, shape):
    """
    Returns the probability for a lattice site to be part of the infinite
    cluster.

    :param clusters: List cluster sizes.
    :param shape: Tuple with the shape of the lattice (row first).

    :return float: Probability for any site to be part of the infinite cluster.
    """

    if len(clusters) == 0:
        return 0

    else:
        return max(clusters) / (shape[0] * shape[1])


def get_connectivity(config):
    """
    Returns connectivity (two point correlation function) in dependence of the
    distance.

    :param config: A labelled cluster configuration, i.e. a regular 2D grid
                   with each site labelled 0 if not occupied and otherwise
                   the label of the cluster it belongs to.

    :return list: A list with the connectivity in dependence of r. Starts with
                  0 distance and goes up to the highest possible distance.
    """

    N, M = config.shape
    # For Manhatten metric on a periodic lattice the maximum distance is half
    # the width/height for each direction
    max_r = int(np.floor(N / 2) + np.floor(M / 2))
    # Count of how many sites at distance r are in the same cluster. The first
    # two entries are 1 because they don't need to be calculated
    count = np.array([1] + [1] + [0] * (max_r - 1), dtype=np.int_)
    # Count of how many occupied sites at distance exist regardless of cluster.
    # First two entries are 1 because they don't need to be calculated
    norm = np.array([1] + [1] + [0] * (max_r - 1), dtype=np.float_)

    # Go through the entire lattice
    for x in range(N):
        for y in range(M):
            # If the site is not occupied ignore
            if config[x, y] == 0:
                continue

            # Calculate the distances from the site
            dist = manhattan_distance(config.shape, (x, y))
            # Label of the site
            cluster = config[x, y]
            # See next if statement
            cluster_edge_reached = False
            # Go through all distances except 0 and 1 because they are always
            # part of the same cluster
            for r in range(2, max_r + 1):
                # Mask for occupied sites at distance r
                at_dist_r = np.logical_and(dist == r, config != 0)
                norm[r] += np.sum(at_dist_r)

                # If the same_cluster for last distance was 0 then it has to
                # be 0 for all larger values of r -> skip
                if not cluster_edge_reached:
                    # Number of occupied sites at dist r that are part of the
                    # same cluster
                    same_cluster = np.sum(np.logical_and(at_dist_r,
                                                         config == cluster))
                    if same_cluster:
                        count[r] += same_cluster
                    else:
                        cluster_edge_reached = True

    return count / norm
