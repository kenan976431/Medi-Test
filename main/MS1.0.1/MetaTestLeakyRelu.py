import sys
sys.path.append(".")
from main.CONSTANT import *
import os
import numpy as np
import copy
import csv
import mindspore as ms
from mindspore import context
from mindspore import Tensor, Parameter, ops, Model
from mindspore.nn import LeakyReLU
from mindspore import dtype as mstype
from constant import *
from utils import *


def SourceModel():
    relu = LeakyReLU(alpha=0.05)
    return relu


def maintest():
    OPERATOR = "LeakyRelu"
    TESTMODE = "metamorphosis"  # differential
    alpha=0.05
    version = lib_version()
    context.set_context(device_target=DEVICE.upper())  # 设置设备

    shape = SHAPE
    data = generate_data(shape)

    # 保存文件到csv
    csv_path = os.path.join(MediTestRoot, "experiment/{}/{}/MetaResult_{}_{}_{}_{}.csv".
                            format(version, TESTMODE, version, FORMAT, DEVICE, OPERATOR))
    with open(file=csv_path, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Lib", "Format", "Device", "Operator", "MutaMode", "Dis", "Delta"])

        for muta_mode in range(0, 4):
            for i in range(100):
                source_model = SourceModel()
                data = generate_data(shape)

                res = [version, FORMAT, DEVICE, OPERATOR]
                if muta_mode == 0:
                    delta = 0
                    # 输入系数
                    source_result = Tensor((1+alpha)*data)
                    follow_result = source_model(data) - source_model(-data)
                    dis = norm_dis(source_result, follow_result)
                elif muta_mode == 1:
                    delta = np.random.uniform(0, DELTA, 1)[0]
                    source_result = source_model(data * delta)
                    follow_result = source_model(data) * delta
                    dis = norm_dis(source_result, follow_result)
                else:
                    break
                # 保存到csv
                res.append("MutaMode" + str(muta_mode))
                res.append(dis)
                res.append(delta)
                csv_writer.writerow(res)
                # 输出显示
                print("{};{};{};{};Iter:{};MutaMode:{};Dis:{};".format(version, OPERATOR, FORMAT, DEVICE, i, muta_mode,
                                                                       dis))


if __name__ == "__main__":
    maintest()
    print("end")





