import sys
sys.path.append(".")
from main.CONSTANT import *

import MNN as mn
import MNN.nn as nn
import MNN.expr as _F
from MNN.nn import conv
from MNN.nn import Module
from MNN.expr import tanh
import numpy
import MNN.numpy as np
import csv
import constant
from utils import *
import time


if __name__ == "__main__":
    OPERATOR = "Tanh"
    TESTMODE = "metamorphosis"  # differential
    version = lib_version()

    shape = SHAPE
    data = generate_data(shape)

    csv_path = os.path.join(MediTestRoot, "experiment/{}/{}/MetaResult_{}_{}_{}_{}.csv".
                            format(version, TESTMODE, version, FORMAT, DEVICE, OPERATOR))
    with open(file=csv_path, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Lib", "Format", "Device", "Operator", "MutaMode", "Dis", "Delta"])

        for muta_mode in range(2):
            for i in range(100):
                data = generate_data(shape)

                res = [version, FORMAT, DEVICE, OPERATOR]
                if muta_mode == 0:
                    delta = 0
                    # 对称性
                    source_result = tanh(data)
                    follow_result = -tanh(-data)
                    dis = norm_dis(source_result, follow_result)
                elif muta_mode == 1:
                    # 和角公式
                    delta = generate_distur(-DELTA, DELTA, 1)[0]
                    source_result = tanh(data + delta)
                    follow_result = (tanh(data) + tanh(delta)) \
                                    / (1 + tanh(data) * tanh(delta))
                    dis = norm_dis(source_result, follow_result)
                else:
                    break
                # 保存到csv
                res.append("MutaMode" + str(muta_mode))
                res.append(dis)
                res.append(delta)
                csv_writer.writerow(res)
                # 输出显示
                print(delta)
                print("{};{};{};{};Iter:{};MutaMode:{};Dis:{};".format(version, OPERATOR, FORMAT, DEVICE, i, muta_mode,
                                                                       dis))

    print("end")











