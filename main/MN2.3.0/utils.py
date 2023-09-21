import MNN as mn
import MNN.numpy as np
import MNN.expr as _F
import numpy
from constant import *


def lib_version():
    return LIB_NAME+mn.version()


def generate_data(shape):
    return np.array(numpy.random.uniform(DATA_RANGE[0], DATA_RANGE[1], shape).tolist(), dtype=_F.float)
    # return np.random.randint(DATA_RANGE[0], DATA_RANGE[1], shape, _F.float)

def generate_distur(low, high, shape):
    return np.array(numpy.random.uniform(low, high, shape).tolist(), dtype=_F.float)


def norm_dis(source_reslut, follow_result, ord="l1"):
    if ord == "l1":
        dis = np.sum(abs(source_reslut-follow_result))
    elif ord == "l2":
        dis = np.linalg.norm(source_reslut - follow_result)  # l1距离
    return dis

if __name__ == "__main__":

    print("end")



