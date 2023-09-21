import sys
sys.path.append(".")
from main.CONSTANT import *

import re
import csv
import h5py
import numpy as np
import torch
import copy
# import torchvision
from torch import tensor
from torch.nn import Conv2d
from constant import *
from utils import *


def SourceModel(shape, device):
    model = Conv2d(in_channels=shape, out_channels=32, kernel_size=(5, 5)).to(device)
    return model


def FollowModel_1(source_model, device):
    # 复制模型
    follow_model = copy.deepcopy(source_model)
    # 读取参数
    bias = follow_model.bias.data  # 卷积偏置 浅拷贝
    bias = copy.deepcopy(bias)
    # 变异模型
    follow_model.train()
    delta = tensor(1+np.random.uniform(-DELTA, DELTA, 1)[0].astype(DTYPE)).to(device)
    follow_model.eval()

    return follow_model, bias, delta


def FollowModel_2(source_model, device):
    # 复制模型
    follow_model = copy.deepcopy(source_model)
    # 读取参数
    weight = follow_model.weight.data  # 卷积权重
    bias = follow_model.bias.data  # 卷积偏置 浅拷贝
    # 模型变异
    follow_model.train()
    delta = tensor(1+np.random.uniform(-DELTA, DELTA, 1)[0].astype(DTYPE)).to(device)
    follow_model.weight.data *= delta
    follow_model.eval()

    return follow_model, copy.deepcopy(bias), delta


def FollowModel_3(source_model, device):
    # 复制模型
    follow_model = copy.deepcopy(source_model)
    # 读取参数
    weight = follow_model.weight.data  # 卷积权重
    bias = follow_model.bias.data  # 卷积偏置 浅拷贝
    bias = copy.deepcopy(bias)
    # 模型变异
    follow_model.train()
    follow_model.weight.data = weight.transpose(2, 3)
    follow_model.eval()

    return follow_model, bias


def FollowModel_4(source_model, device):
    # 复制模型
    follow_model = copy.deepcopy(source_model)
    # 读取参数
    weight = follow_model.weight.data  # 卷积权重
    bias = follow_model.bias.data  # 卷积偏置 浅拷贝
    # 变异模型
    follow_model.train()
    delta = tensor(np.random.uniform(-DELTA, DELTA, 1)[0].astype("float32")).to(device)
    follow_model.bias.data += delta
    follow_model.eval()

    return follow_model, delta


def ReadSourceModelPara(source_model):
    old_para = source_model.state_dict()
    new_para = copy.deepcopy(old_para)

    weights_names = []
    weights = []
    for key in new_para.keys():
        weights_names.append(key)
        weights.append(new_para[key].cpu().detach().numpy())

    return weights_names, weights


def WriteMutaProcess(group, No: int,
                     input, source_result: np.ndarray, follow_result: np.ndarray,
                     model_para: tuple, muta_para: tuple):
    group_no = group.create_group("No_" + str(No))  # 创建子文件夹
    group_no.create_dataset("Input", data=input)
    group_no.create_dataset("SourceResult", data=source_result)
    group_no.create_dataset("FollowResult", data=follow_result)

    group_no_model = group_no.create_group("ModelPara") # 存放模型名称和权重
    for idx, name in enumerate(model_para[0]):  # 将模型层名称作为key值
        name = name.split("/")[-1]
        group_no_model.create_dataset(name, data=model_para[1][idx])

    group_no_muta = group_no.create_group("MutaPara")   # 存放变质参数和名称
    for idx, name in enumerate(muta_para[0]):   # 将变量名称作为key值
        group_no_muta.create_dataset(name, data=muta_para[1][idx])
    return 0


def maintest():
    OPERATOR = "Conv"
    TESTMODE = "metamorphosis"  # differential
    version = lib_version()
    # torch.set_default_dtype(torch.float32)
    torch.set_printoptions(precision=8)

    device = torch.device('cuda' if DEVICE == "gpu" else "cpu")
    shape = SHAPE

    # 保存文件到csv
    csv_path = os.path.join(MediTestRoot, "experiment/{}/{}/MetaResult_{}_{}_{}_{}.csv".
                            format(version, TESTMODE, version, FORMAT, DEVICE, OPERATOR))
    with open(file=csv_path, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Lib", "Format", "Device", "Operator", "MutaMode", "Dis", "Delta"])

        # 初始化source模型
        # source_model = SourceModel(shape[1] if FORMAT == "NCHW" else shape[-1]).to(device)
        d_format = torch.channels_last if FORMAT == "NHWC" else torch.contiguous_format
        source_model = SourceModel(shape[1], device).to(device)
        source_model.to(memory_format=d_format)
        for muta_mode in range(0, 4):

            for i in range(100):
                data = generate_data(shape, device).to(memory_format=d_format)
                res = [version, FORMAT, DEVICE, OPERATOR]
                if muta_mode == 0:
                    # 输入蜕变
                    follow_model, bias, delta = FollowModel_1(source_model, device)
                    source_result = (source_model.forward(data) - bias.reshape(-1, 1, 1)) * delta
                    follow_result = follow_model.forward(delta * data) - bias.reshape(-1, 1, 1)
                    dis = norm_dis(source_result, follow_result).cpu().detach().numpy()[()]
                elif muta_mode == 1:
                    # 模型蜕变 斜率
                    follow_model, bias, delta = FollowModel_2(source_model, device)
                    source_result = (source_model.forward(data) - bias.reshape(-1, 1, 1)) * delta
                    follow_result = follow_model.forward(data) - bias.reshape(-1, 1, 1)
                    dis = norm_dis(source_result, follow_result).cpu().detach().numpy()[()]
                elif muta_mode == 2:
                    # 输入+模型蜕变 转置
                    follow_model, bias = FollowModel_3(source_model, device)
                    delta = tensor(0).to(device)
                    source_result = (source_model.forward(data) - bias.reshape(-1, 1, 1)).transpose(2, 3)
                    follow_result = follow_model.forward(data.transpose(2, 3)) - bias.reshape(-1, 1, 1)
                    dis = norm_dis(source_result, follow_result).cpu().detach().numpy()[()]
                elif muta_mode == 3:
                    # 偏移蜕变
                    follow_model, delta = FollowModel_4(source_model, device)
                    source_result = source_model.forward(data) + delta
                    follow_result = follow_model.forward(data)
                    dis = norm_dis(source_result, follow_result).cpu().detach().numpy()[()]
                else:
                    break

                # 保存到csv
                res.append("MutaMode" + str(muta_mode))
                res.append(dis)
                res.append(delta.cpu().detach().numpy()[()])
                csv_writer.writerow(res)
                # 输出显示
                print("{};{};{};{};Iter:{};MutaMode:{};Dis:{};".format(version, OPERATOR, FORMAT, DEVICE, i, muta_mode,
                                                                       dis))


if __name__ == "__main__":
    maintest()
    print("end")



