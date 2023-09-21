import sys
sys.path.append(".")
from main.CONSTANT import *

import MNN as mn
import MNN.nn as nn
import MNN.expr as _F
from MNN.nn import conv
from MNN.nn import Module
from MNN.expr import relu
import numpy
import MNN.numpy as np
import csv
import constant
from utils import *
import time



if __name__ == "__main__":
    OPERATOR = "Relu"
    TESTMODE = "metamorphosis"  # differential
    version = lib_version()

    shape = SHAPE
    data = generate_data(shape)

    csv_path = os.path.join(MediTestRoot, "experiment/{}/{}/MetaResult_{}_{}_{}_{}.csv".
                            format(version, TESTMODE, version, FORMAT, DEVICE, OPERATOR))
    with open(file=csv_path, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Lib", "Format", "Device", "Operator", "MutaMode", "Dis", "Delta"])

        for muta_mode in range(4):
            for i in range(100):
                data = generate_data(shape)

                res = [version, FORMAT, DEVICE, OPERATOR]
                if muta_mode == 0:
                    delta = 0
                    # 输入蜕变
                    source_result = np.abs(data)
                    follow_result = relu(data) + relu(-data)
                    dis = norm_dis(source_result, follow_result)
                elif muta_mode == 1:
                    delta = generate_distur(0, DELTA, 1)[0]
                    source_result = relu(delta * data)
                    follow_result = delta * relu(data)
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

    print("end")











