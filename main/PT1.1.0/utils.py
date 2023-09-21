import torch
import numpy as np
from torch import tensor
import re
from constant import *


def lib_version():
    return LIB_NAME+torch.__version__


def generate_data(shape, device):
    return torch.from_numpy(np.random.uniform(DATA_RANGE[0], DATA_RANGE[1], shape).astype(DTYPE)).float().to(device)


def norm_dis(source_result, follow_result, ord="l1"):
    sor = source_result.cpu().detach().numpy()
    fol = follow_result.cpu().detach().numpy()
    if ord == "l1":
        dis = np.sum(abs(sor-fol))
    elif ord == "l2":
        dis = np.linalg.norm(source_result - follow_result)
    return dis


def FindWeightsIdx(name, weights_names):
    # 寻找模型权重中名字匹配的那个
    for idx, names in enumerate(weights_names):
        if re.search(name, names):
            return idx
    return -1


def ReadMutaProcess(MutaNo, device):
    # 读取h5文件的蜕变过程用于差分测试
    input = MutaNo["Input"][:]
    source_result = MutaNo["SourceResult"][:]
    follow_result = MutaNo["FollowResult"][:]
    model_weights_name = [key for key in MutaNo["ModelPara"].keys()]  # 模型权重的名字
    model_weights = [MutaNo["ModelPara"][key][()] for key in MutaNo["ModelPara"].keys()]  # 模型权重
    muta_para_name = [key for key in MutaNo["MutaPara"].keys()]  # 变质参数
    muta_para = [MutaNo["MutaPara"][key][()] for key in MutaNo["MutaPara"].keys()]

    # 将numpy矩阵转为tensor
    input = tensor(input, device=device)
    source_result = tensor(source_result, device=device)
    follow_result = tensor(follow_result, device=device)

    return input, source_result, follow_result, (model_weights_name, model_weights), (muta_para_name, muta_para)


def WriteDiffProcess(group, No: int, source_result, follow_result):
    # 将tensor转为numpy
    source_result = source_result.cpu().detach().numpy()
    follow_result = follow_result.cpu().detach().numpy()

    group_no = group.create_group("No_" + str(No))  # 创建子文件夹
    # group_no.create_dataset("Input", data=input)
    group_no.create_dataset("SourceResult", data=source_result)
    group_no.create_dataset("FollowResult", data=follow_result)
    return 0
