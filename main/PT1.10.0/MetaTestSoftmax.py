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
from torch.nn import Softmax
from constant import *
from utils import *


def SourceModel(shape):
    sm = Softmax(dim=shape[1])
    return sm


def maintest():
    OPERATOR = "Softmax"
    TESTMODE = "metamorphosis"  # differential
    version = lib_version()
    # torch.set_default_dtype(torch.float32)
    torch.set_printoptions(precision=8)

    device = torch.device('cuda' if DEVICE == "gpu" else "cpu")
    shape = SHAPE
    d_format = torch.channels_last if FORMAT == "NHWC" else torch.contiguous_format

    # 保存文件到csv
    csv_path = os.path.join(MediTestRoot, "experiment/{}/{}/MetaResult_{}_{}_{}_{}.csv".
                            format(version, TESTMODE, version, FORMAT, DEVICE, OPERATOR))
    with open(file=csv_path, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Lib", "Format", "Device", "Operator", "MutaMode", "Dis", "Delta"])

        source_model = SourceModel(shape).to(device).to(memory_format=d_format).eval()
        for muta_mode in range(0, 1):
            for i in range(100):

                data = generate_data(shape, device).to(memory_format=d_format)

                res = [version, FORMAT, DEVICE, OPERATOR]
                if muta_mode == 0:
                    # 输入系数
                    delta = tensor(np.random.uniform(-DELTA, DELTA, 1)[0]).to(device)
                    source_result = source_model.forward(data)
                    follow_result = source_model.forward(data + delta)
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

