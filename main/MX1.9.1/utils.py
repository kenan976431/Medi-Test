import os
import mxnet as mx
import numpy as np

from constant import *
from mxnet import nd            # Tensor模块

def lib_version():
    return LIB_NAME+mx.__version__


def generate_data(shape, device):
    if device == "cpu":
        return nd.random.uniform(DATA_RANGE[0], DATA_RANGE[1], shape, ctx=mx.cpu()).astype(DTYPE)
    elif device == "gpu":
        return nd.random.uniform(DATA_RANGE[0], DATA_RANGE[1], shape, ctx=mx.gpu()).astype(DTYPE)


def norm_dis(source_reslut, follow_result, ord="l1"):
    if ord == "l1":
        dis = nd.sum(abs(source_reslut-follow_result))
    elif ord == "l2":
        dis = nd.norm(source_reslut - follow_result)  # l1距离
    return dis


if __name__ == "__main__":
    v = lib_version()
    print("end")