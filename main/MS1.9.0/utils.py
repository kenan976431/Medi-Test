import mindspore as ms
from mindspore import Tensor
import numpy as np
from constant import *


def lib_version():
    return LIB_NAME+ms.__version__


def generate_data(shape):
    return Tensor(np.random.uniform(-1, 1, shape).astype(DTYPE))


def norm_dis(source_result, follow_result, ord="l1"):
    if ord == "l1":
        dis = ms.numpy.sum(ms.numpy.abs(source_result - follow_result))
    elif ord == "l2":
        dis = ms.numpy.norm(source_result - follow_result)
    return dis
