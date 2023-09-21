import sys
sys.path.append(".")
from main.CONSTANT import *

import MNN as mn
import MNN.nn as nn
import MNN.expr as _F
from MNN.nn import conv
from MNN.nn import Module
from MNN.expr import max_pool
import numpy
import MNN.numpy as np
import csv
import constant
from utils import *
import time



if __name__ == "__main__":
    OPERATOR = "Maxpool"
    TESTMODE = "metamorphosis"  # differential
    version = lib_version()

    shape = SHAPE
    data = generate_data(shape)

    # 保存文件到csv
    csv_path = os.path.join(MediTestRoot, "experiment/{}/{}/MetaResult_{}_{}_{}_{}.csv".
                            format(version, TESTMODE, version, FORMAT, DEVICE, OPERATOR))
    with open(file=csv_path, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Lib", "Format", "Device", "Operator", "MutaMode", "Dis", "Delta"])

        for muta_mode in range(0, 3):
            for i in range(100):
                pool_size = np.random.randint(1, 5)[0]
                strides = np.random.randint(1, 5)[0]
                data = generate_data(shape)

                res = [version, FORMAT, DEVICE, OPERATOR]
                if muta_mode == 0:
                    # 输入系数
                    delta = generate_distur(-DELTA, DELTA, 1)[0]
                    source_result = max_pool(data, kernel=[pool_size, pool_size], stride=[strides, strides]) * delta
                    follow_result = max_pool(data * delta, kernel=[pool_size, pool_size], stride=[strides, strides])
                    dis = norm_dis(source_result, follow_result)
                elif muta_mode == 1:
                    # 输入偏置
                    delta = generate_distur(-DELTA, DELTA, 1)[0]
                    source_result = max_pool(data, kernel=[pool_size, pool_size], stride=[strides, strides]) + delta
                    follow_result = max_pool(data + delta, kernel=[pool_size, pool_size], stride=[strides, strides])
                    dis = norm_dis(source_result, follow_result)
                elif muta_mode == 2:
                    delta = 0
                    # 转置 NCHW
                    source_result = max_pool(data, kernel=[pool_size, pool_size], stride=[strides, strides])
                    source_result = np.transpose(source_result, (0, 1, 3, 2))
                    follow_result = max_pool(data.transpose((0, 1, 3, 2)),
                                             kernel=[pool_size, pool_size], stride=[strides, strides])
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










