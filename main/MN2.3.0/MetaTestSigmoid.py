import sys
sys.path.append(".")
from main.CONSTANT import *

import MNN as mn
import MNN.nn as nn
import MNN.expr as _F
from MNN.nn import conv
from MNN.nn import Module
from MNN.expr import sigmoid
import numpy
import MNN.numpy as np
import csv
import constant
from utils import *
import time


if __name__ == "__main__":
    OPERATOR = "Sigmoid"
    TESTMODE = "metamorphosis"  # differential
    version = lib_version()

    shape = SHAPE
    data = generate_data(shape)

    csv_path = os.path.join(MediTestRoot, "experiment/{}/{}/MetaResult_{}_{}_{}_{}.csv".
                            format(version, TESTMODE, version, FORMAT, DEVICE, OPERATOR))
    with open(file=csv_path, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Lib", "Format", "Device", "Operator", "MutaMode", "Dis", "Delta"])

        for muta_mode in range(1):
            for i in range(100):
                data = generate_data(shape)
                print(data.shape)
                res = [version, FORMAT, DEVICE, OPERATOR]
                if muta_mode == 0:
                    # 输入蜕变
                    # delta = generate_distur(-DELTA, DELTA, 1)[0]
                    if FORMAT=="NCHW":
                        source_result = np.transpose(sigmoid(data),axes=[0,1,3,2])
                        follow_result = sigmoid( np.transpose(data,axes=[0,1,3,2]))
                    elif FORMAT=="NHWC":
                        source_result = np.transpose(sigmoid(data), axes=[0, 2, 1, 3])
                        follow_result = sigmoid(np.transpose(data, axes=[0, 2, 1, 2]))

                    dis = norm_dis(source_result, follow_result)
                else:
                    break
                # 保存到csv
                delta=0
                res.append("MutaMode" + str(muta_mode))
                res.append(dis)
                res.append(delta)
                csv_writer.writerow(res)
                # 输出显示
                print("{};{};{};{};Iter:{};MutaMode:{};Dis:{};".format(version, OPERATOR, FORMAT, DEVICE, i, muta_mode,
                                                                       dis))
    print("end")











