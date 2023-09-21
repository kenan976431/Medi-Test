import sys
sys.path.append(".")
from main.CONSTANT import *
import numpy as np
import copy
import csv
import mindspore as ms
from mindspore import Tensor, Parameter, ops, Model
from mindspore.nn import AvgPool2d
from mindspore import dtype as mstype
from constant import *
from utils import *


def SourceModel():
    pool_size = np.random.randint(1, 5)
    strides = np.random.randint(1, 5)

    pool = AvgPool2d(kernel_size=pool_size, stride=strides,
                     pad_mode="valid", data_format=FORMAT)
    return pool


def maintest():
    OPERATOR = "Avgpool"
    TESTMODE = "metamorphosis"  # differential
    version = lib_version()
    ms.context.set_context(device_target=DEVICE.upper())  # 设置设备

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
                    # 输入系数
                    delta = np.random.uniform(-DELTA, DELTA, 1)[0]
                    source_result = source_model(data) * delta
                    follow_result = source_model(data * delta)
                    dis = norm_dis(source_result, follow_result)
                elif muta_mode == 1:
                    # 输入偏置
                    delta = np.random.uniform(-DELTA, DELTA, 1)[0]
                    source_result = source_model(data) + delta
                    follow_result = source_model(data + delta)
                    dis = norm_dis(source_result, follow_result)
                elif muta_mode == 2:
                    delta = 0
                    if FORMAT == "NHWC":
                        source_result = source_model(data).transpose(0, 2, 1, 3)
                        follow_result = source_model(data.transpose(0, 2, 1, 3))
                    elif FORMAT == "NCHW":
                        source_result = source_model(data).transpose(0, 1, 3, 2)
                        follow_result = source_model(data.transpose(0, 1, 3, 2))
                    dis = norm_dis(source_result, follow_result)
                else:
                    break
                # 保存到csv
                res.append("MutaMode" + str(muta_mode))
                print(dis, delta)
                res.append(dis)
                res.append(delta)
                csv_writer.writerow(res)
                # 输出显示
                print("{};{};{};{};Iter:{};MutaMode:{};Dis:{};".format(version, OPERATOR, FORMAT, DEVICE, i, muta_mode,
                                                                       dis))


if __name__ == "__main__":
    # maintest()
    OPERATOR = "Avgpool"
    TESTMODE = "metamorphosis"  # differential
    version = lib_version()
    ms.context.set_context(device_target=DEVICE.upper())  # 设置设备

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
                    # 输入系数
                    delta = np.random.uniform(-DELTA, DELTA, 1)[0]
                    source_result = source_model(data) * delta
                    follow_result = source_model(data * delta)
                    dis = norm_dis(source_result, follow_result).asnumpy()[()]
                elif muta_mode == 1:
                    # 输入偏置
                    delta = np.random.uniform(-DELTA, DELTA, 1)[0]
                    source_result = source_model(data) + delta
                    follow_result = source_model(data + delta)
                    dis = norm_dis(source_result, follow_result).asnumpy()[()]
                elif muta_mode == 2:
                    delta = DELTA / 2
                    if FORMAT == "NHWC":
                        source_result = source_model(data).transpose(0, 2, 1, 3)
                        follow_result = source_model(data.transpose(0, 2, 1, 3))
                    elif FORMAT == "NCHW":
                        source_result = source_model(data).transpose(0, 1, 3, 2)
                        follow_result = source_model(data.transpose(0, 1, 3, 2))
                    dis = norm_dis(source_result, follow_result).asnumpy()[()]
                else:
                    break
                # 保存到csv
                res.append("MutaMode" + str(muta_mode))
                res.append(dis)
                res.append(delta)
                res.append(abs(dis / delta))
                csv_writer.writerow(res)
                # 输出显示
                print("{};{};{};{};Iter:{};MutaMode:{};Dis:{};".format(version, OPERATOR, FORMAT, DEVICE, i, muta_mode,
                                                                       dis))
    print("end")



