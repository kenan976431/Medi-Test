import torch
import numpy as np
from constant import *


def lib_version():
    return LIB_NAME+torch.__version__.split("+")[0]

def generate_data(shape, device):
    return torch.from_numpy(np.random.uniform(DATA_RANGE[0], DATA_RANGE[1], shape).astype(DTYPE)).float().to(device)


def norm_dis(source_result, follow_result, ord="l1"):
    if ord == "l1":
        dis = torch.sum(torch.abs_(source_result-follow_result))
    elif ord == "l2":
        dis = torch.norm(source_result - follow_result)
    return dis






