import numpy as np


def accuracy(output, target):
    """
    Parameters
    ----------
    output: numpy ndarray, M x 1
    target: numpy ndarray, M x 1

    Returns
    -------
    y: float, 0 <= y <= 1

    Raises
    -----
    TypeError
    ValueError
    """
    return np.count_nonzero(np.equal(output, target)) / len(output)


def l1_loss(output, target):
    return np.sum(np.abs(output - target)) / len(target)


def l2_loss(output, target):
    return np.sqrt(np.sum(np.power(output - target, 2))) / len(target)


def default(output, target):
    return -1
