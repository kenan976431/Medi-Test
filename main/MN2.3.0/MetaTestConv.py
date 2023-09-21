import sys
sys.path.append(".")
from main.CONSTANT import *

import MNN as mn
import MNN.nn as nn
import MNN.expr as _F
from MNN.nn import depthwiseconv
from MNN.nn import Module
import numpy
import MNN.numpy as np
import csv
import constant
from utils import *
import time


def SourceModel(shape):
    if FORMAT == "NCHW":
        in_channel = shape[1]
    else:
        print("MNN 只支持NCHW")
    source_mdoel = depthwiseconv(in_channel, 32, [5, 5])
    return source_mdoel


def FollowModel_1(source_model, shape):
    # 读取参数
    bias = source_model.parameters[0]
    weight = source_model.parameters[1]
    # 扰动
    delta = 1+generate_distur(-DELTA, DELTA, 1)[0]
    # delta = 1+np.random.randint(-DELTA, DELTA, 1, _F.float)[0]
    # 变异模型
    follow_model = SourceModel(shape)
    follow_model.load_parameters([bias, weight])

    return follow_model, bias, delta


def FollowModel_2(source_model, shape):
    # 读取参数
    bias = source_model.parameters[0]
    weight = source_model.parameters[1]
    # 扰动
    delta = 1 + generate_distur(-DELTA, DELTA, 1)[0]
    # 变异模型
    follow_model = SourceModel(shape)
    follow_model.load_parameters([bias, weight*delta])

    return follow_model, bias, delta


def FollowModel_3(source_model, shape):
    # 读取参数
    bias = source_model.parameters[0]
    weight = source_model.parameters[1]
    # 转置
    weight = np.transpose(weight, (0,1,3,2))
    # 变异模型
    follow_model = SourceModel(shape)
    follow_model.load_parameters([bias, weight])

    return follow_model, bias


def FollowModel_4(source_model, shape):
    # 读取参数
    bias = source_model.parameters[0]
    weight = source_model.parameters[1]
    # 扰动
    delta = generate_distur(-DELTA, DELTA, 1)[0]
    # 变异模型
    follow_model = SourceModel(shape)
    follow_model.load_parameters([bias+delta, weight])

    return follow_model, delta


if __name__ == "__main__":
    OPERATOR = "DepthwiseConv"
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

        source_model = SourceModel(shape)
        source_model(data)
        for muta_mode in range(0, 4):
            for i in range(100):
                data = generate_data(shape)
                res = [version, FORMAT, DEVICE, OPERATOR]

                if muta_mode == 0:
                    # 输入线性变异
                    follow_model, bias, delta = FollowModel_1(source_model, shape)
                    bias = bias if FORMAT == "NHWC" else bias.reshape(-1, 1, 1)
                    source_result = (source_model(data) - bias) * delta
                    follow_result = follow_model(data * delta) - bias
                    dis = norm_dis(source_result, follow_result)
                elif muta_mode == 1:
                    # 权重变异
                    follow_model, bias, delta = FollowModel_2(source_model, shape)
                    bias = bias if FORMAT == "NHWC" else bias.reshape(-1, 1, 1)
                    source_result = (source_model(data) - bias) * delta
                    follow_result = follow_model(data) - bias
                    dis = norm_dis(source_result, follow_result)
                elif muta_mode == 2:
                    # kernel和输入转置
                    follow_model, bias = FollowModel_3(source_model, shape)
                    bias = bias if FORMAT == "NHWC" else bias.reshape(-1, 1, 1)
                    delta = 0
                    if FORMAT == "NHWC":
                        source_result = np.transpose(source_model(data) - bias, (0, 2, 1, 3))
                        follow_result = follow_model(data.transpose((0, 2, 1, 3))) - bias
                    elif FORMAT == "NCHW":
                        source_result = np.transpose(source_model(data) - bias, (0, 1, 3, 2))
                        follow_result = follow_model(data.transpose((0, 1, 3, 2))) - bias
                    dis = norm_dis(source_result, follow_result)
                elif muta_mode == 3:
                    # bias变质
                    follow_model, delta = FollowModel_4(source_model, shape)
                    source_result = source_model(data) + delta
                    follow_result = follow_model(data)
                    dis = norm_dis(source_result, follow_result)
                else:
                    break
                # 保存到csv
                res.append("MutaMode" + str(muta_mode))
                res.append(dis)
                res.append(delta)
                csv_writer.writerow(res)
                # 输出显示
                print("{};{};{};{};Iter:{};MutaMode:{};Dis:{};".format(version, OPERATOR, FORMAT, DEVICE, i,
                                                                       muta_mode, dis))

    print("end")




