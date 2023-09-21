import sys
sys.path.append(".")
from main.CONSTANT import *
import os.path
import re
import csv
import h5py
import numpy as np
import torch
import copy
from torch import tensor
from torch.nn import AvgPool2d
from constant import *
from utils import *


def SourceModel():
    pool_size = np.random.randint(1, 5)
    strides = np.random.randint(1, 5)

    pool = AvgPool2d(kernel_size=(pool_size, pool_size), stride=(strides, strides))
    return pool


def maintest():
    OPERATOR = "Avgpool"
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

        for muta_mode in range(0, 3):
            for i in range(100):
                source_model = SourceModel().to(device).eval()
                data = generate_data(shape, device)

                res = [version, FORMAT, DEVICE, OPERATOR]
                if muta_mode == 0:
                    # 输入系数
                    delta = tensor(np.random.uniform(-DELTA, DELTA, 1)[0]).to(device)
                    source_result = source_model.forward(data) * delta
                    follow_result = source_model.forward(data * delta)
                    dis = norm_dis(source_result, follow_result)
                elif muta_mode == 1:
                    # 输入偏置
                    delta = tensor(np.random.uniform(-DELTA, DELTA, 1)[0]).to(device)
                    source_result = source_model.forward(data) + delta
                    follow_result = source_model.forward(data + delta)
                    dis = norm_dis(source_result, follow_result)
                elif muta_mode == 2:
                    delta = tensor(0).to(device)
                    # 转置
                    source_result = torch.transpose(source_model.forward(data), 2, 3)
                    follow_result = source_model.forward(torch.transpose(data, 2, 3))
                    dis = norm_dis(source_result, follow_result)
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

