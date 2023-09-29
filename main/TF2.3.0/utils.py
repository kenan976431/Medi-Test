import os
import tensorflow as tf
import numpy as np

from constant import *
from queue import Queue
import re

def lib_version():
    return LIB_NAME+tf.__version__


def generate_data(shape):
    return np.random.uniform(DATA_RANGE[0], DATA_RANGE[1], shape).astype(DTYPE)


def FindWeightsIdx(name, weights_names):
    # 寻找模型权重中名字匹配的那个
    for idx, names in enumerate(weights_names):
        if re.search(name, names):
            return idx
    return -1


def norm_dis(source_reslut, follow_result, ord="l1"):
    if ord == "l1":
        dis = np.sum(abs(source_reslut-follow_result))
    elif ord == "l2":
        dis = np.linalg.norm(source_reslut - follow_result)  # l1距离
    return dis


def ReadMutaProcess(MutaNo):
    # 读取h5文件的蜕变过程用于差分测试
    input = MutaNo["Input"][:]
    source_result = MutaNo["SourceResult"][:]
    follow_result = MutaNo["FollowResult"][:]
    model_weights_name = [key for key in MutaNo["ModelPara"].keys()]  # 模型权重的名字
    model_weights = [MutaNo["ModelPara"][key].value for key in MutaNo["ModelPara"].keys()]  # 模型权重
    muta_para_name = [key for key in MutaNo["MutaPara"].keys()]  # 变质参数
    muta_para = [MutaNo["MutaPara"][key].value for key in MutaNo["MutaPara"].keys()]

    return input, source_result, follow_result, (model_weights_name, model_weights), (muta_para_name, muta_para)


def WriteDiffProcess(group, No: int, source_result: np.ndarray, follow_result: np.ndarray):
    group_no = group.create_group("No_" + str(No))  # 创建子文件夹
    # group_no.create_dataset("Input", data=input)
    group_no.create_dataset("SourceResult", data=source_result)
    group_no.create_dataset("FollowResult", data=follow_result)
    return 0


