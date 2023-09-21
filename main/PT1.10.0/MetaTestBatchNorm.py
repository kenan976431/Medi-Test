import sys
sys.path.append(".")
from main.CONSTANT import *
import re
import csv
import h5py
import numpy as np
import torch
import copy
import torchvision
from torch import tensor
from torch.nn import BatchNorm2d
from constant import *
from utils import *


def SourceModel(dim):
    bn = BatchNorm2d(dim)
    return bn


def FollowModel_1(source_model, device):
    # 复制模型
    follow_model = copy.deepcopy(source_model)
    # 读取参数
    old_para = follow_model.state_dict()
    epsilon = follow_model.eps
    new_para = copy.deepcopy(old_para)
    # 模型变异
    follow_model.train()    # 便于修改参数
    delta = tensor(np.random.uniform(-1e-3, 1e-3, 1)[0].astype(DTYPE)).to(device)
    new_para["running_var"] = new_para["running_var"] + delta
    follow_model.eps -= delta.cpu().detach().numpy()
    follow_model.load_state_dict(new_para)
    follow_model.eval()     # 固定模型参数

    return follow_model, delta


def FollowModel_2(source_model, device):
    # 复制模型
    follow_model = copy.deepcopy(source_model)
    # 读取参数
    old_para = follow_model.state_dict()
    new_para = copy.deepcopy(old_para)
    # 模型变异
    follow_model.train()
    delta = tensor(np.random.uniform(-DELTA, DELTA, 1)[0].astype(DTYPE), device=device)
    new_para["running_mean"] = new_para["running_mean"] + delta
    follow_model.load_state_dict(new_para)
    follow_model.eval()

    return follow_model, delta


def FollowModel_3(source_model, device):
    # 复制模型
    follow_model = copy.deepcopy(source_model)
    # 读取参数
    old_para = follow_model.state_dict()
    new_para = copy.deepcopy(old_para)
    # 模型变异
    follow_model.train()
    delta = tensor(np.random.uniform(-DELTA, DELTA, 1)[0].astype(DTYPE), device=device)
    new_para["bias"] = new_para["bias"] + delta
    follow_model.load_state_dict(new_para)
    follow_model.eval()

    return follow_model, delta


def FollowModel_4(source_model, device):
    # 复制模型
    follow_model = copy.deepcopy(source_model)
    # 读取参数
    old_para = follow_model.state_dict()
    new_para = copy.deepcopy(old_para)
    # 模型变异
    follow_model.train()
    delta = tensor(np.random.uniform(1-DELTA, 1+DELTA, 1)[0].astype(DTYPE), device=device)
    new_para["weight"] *= delta
    bias = new_para["bias"]
    follow_model.load_state_dict(new_para)
    follow_model.eval()
    return follow_model, bias, delta


def maintest():
    OPERATOR = "BN"
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
        source_model = SourceModel(shape[1]).to(device)
        source_model.to(memory_format=d_format)

        # source_model.to(memory_format)

        source_model.eps = 1e-3  # tensorflow的eps初始值设为1e-3
        source_model.eval()  # 固定模型参数
        for muta_mode in range(0, 4):
            for i in range(100):
                data = generate_data(shape, device).to(memory_format=d_format)
                res = [version, FORMAT, DEVICE, OPERATOR]
                if muta_mode == 0:
                    # 方差蜕变
                    follow_model, delta = FollowModel_1(source_model, device)
                    source_result = source_model.forward(data)
                    follow_result = follow_model.forward(data)
                    dis = norm_dis(source_result, follow_result).cpu().detach().numpy()[()]
                elif muta_mode == 1:
                    # 输入+模型蜕变
                    follow_model, delta = FollowModel_2(source_model, device)
                    source_result = source_model.forward(data)
                    follow_result = follow_model.forward(data + delta)
                    dis = norm_dis(source_result, follow_result).cpu().detach().numpy()[()]
                elif muta_mode == 2:
                    # bias蜕变
                    follow_model, delta = FollowModel_3(source_model, device)
                    source_result = source_model.forward(data) + delta
                    follow_result = follow_model.forward(data)
                    dis = norm_dis(source_result, follow_result).cpu().detach().numpy()[()]
                elif muta_mode == 3:
                    # 斜率蜕变
                    follow_model, bias, delta = FollowModel_4(source_model, device)
                    source_result = (source_model.forward(data) - bias.reshape(-1, 1, 1)) * delta
                    follow_result = follow_model.forward(data) - bias.reshape(-1, 1, 1)
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




