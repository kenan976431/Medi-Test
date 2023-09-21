import sys
sys.path.append(".")
from main.CONSTANT import *
import numpy as np
import copy
import csv
import mindspore as ms
from mindspore import Tensor, Parameter, ops, Model
from mindspore.nn import Sigmoid
from mindspore import dtype as mstype
from constant import *
from utils import *


def SourceModel():
    sm = Sigmoid()
    return sm


def maintest():
    OPERATOR = "Sigmoid"
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
                    if FORMAT == "NHWC":
                        delta = np.random.uniform(-DELTA, DELTA, 1)[0]
                        source_result = Tensor(source_model(data).asnumpy().transpose(0, 2, 1, 3))
                        follow_result = source_model(Tensor(data.asnumpy().transpose(0, 2, 1, 3)))
                        dis = norm_dis(source_result, follow_result).asnumpy()[()]
                    elif FORMAT == "NCHW":
                        delta = np.random.uniform(-DELTA, DELTA, 1)[0]
                        source_result = Tensor(source_model(data).asnumpy().transpose(0, 1, 3, 2))
                        follow_result = source_model(Tensor(data.asnumpy().transpose(0, 1, 3, 2)))
                        dis = norm_dis(source_result, follow_result).asnumpy()[()]
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



