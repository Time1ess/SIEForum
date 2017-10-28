import numpy as np


def accuracy(output, target):
    return output - target
    return np.equal(output, target).count_nonzero() / len(target)


def l1_loss(output, target):
    return np.sum(np.abs(output - target)) / len(target)


def l2_loss(output, target):
    return np.sqrt(np.sum(np.power(output - target, 2))) / len(target)


def default(output, target):
    return -1
