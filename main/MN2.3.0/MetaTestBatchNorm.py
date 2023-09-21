import sys
sys.path.append(".")
from main.CONSTANT import *

import MNN as mn
import MNN.nn as nn
import MNN.expr as _F
from MNN.nn import batch_norm
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
    source_mdoel = batch_norm(in_channel)
    return source_mdoel


def FollowModel_1(source_model, shape):
    # 读取参数
    gamma = source_model.parameters[0]
    bias = source_model.parameters[1]
    var = source_model.parameters[2]
    mean = source_model.parameters[3]
    # 扰动
    delta = 1 + generate_distur(-1e-5, 1e-5, 1)[0]
    # 变异模型
    follow_model = batch_norm(shape[1], epsilon=1e-5+delta)     # MNN这么设置会报错
    follow_model.load_parameters([gamma, bias, var-delta, mean])
    return follow_model, delta


def FollowModel_2(source_model, shape):
    # 读取参数
    gamma = source_model.parameters[0]
    bias = source_model.parameters[1]
    var = source_model.parameters[2]
    mean = source_model.parameters[3]
    # 扰动
    delta = generate_distur(-1e-5, 1e-5, 1)[0]
    # 变异模型
    follow_model = batch_norm(shape[1])  # MNN这么设置会报错
    follow_model.load_parameters([gamma, bias, var, mean+delta])
    return follow_model, delta


def FollowModel_3(source_model, shape):
    # 读取参数
    gamma = source_model.parameters[0]
    bias = source_model.parameters[1]
    var = source_model.parameters[2]
    mean = source_model.parameters[3]
    # 扰动
    delta = generate_distur(-DELTA, DELTA, 1)[0]
    # 变异模型
    follow_model = batch_norm(shape[1])  # MNN这么设置会报错
    follow_model.load_parameters([gamma, bias + delta, var, mean])

    return follow_model, delta


def FollowModel_4(source_model, shape):
    # 读取参数
    gamma = source_model.parameters[0]
    bias = source_model.parameters[1]
    var = source_model.parameters[2]
    mean = source_model.parameters[3]
    # 扰动
    delta = 1 + generate_distur(-DELTA, DELTA, 1)[0]
    # 变异模型
    follow_model = batch_norm(shape[1])  # MNN这么设置会报错
    follow_model.load_parameters([gamma * delta, bias, var, mean])

    return follow_model, delta, bias


if __name__ == "__main__":
    OPERATOR = "BN"
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
        for muta_mode in range(1, 4):
            for i in range(100):
                data = generate_data(shape)
                res = [version, FORMAT, DEVICE, OPERATOR]

                if muta_mode == 0:
                    # 方差部分的变异
                    follow_model, delta = FollowModel_1(source_model, shape)
                    source_result = source_model(data)
                    follow_result = follow_model(data)
                    dis = norm_dis(source_result, follow_result)
                elif muta_mode == 1:
                    # 输入均值变异
                    follow_model, delta = FollowModel_2(source_model, shape)
                    source_result = source_model(data)
                    follow_result = follow_model(data + delta)
                    dis = norm_dis(source_result, follow_result)
                elif muta_mode == 2:
                    # bais部分的变异
                    follow_model, delta = FollowModel_3(source_model, shape)
                    source_result = source_model(data) + delta
                    follow_result = follow_model(data)
                    dis = norm_dis(source_result, follow_result)
                elif muta_mode == 3:
                    # 斜率部分的变异
                    follow_model, delta, beta = FollowModel_4(source_model, shape)
                    source_result = (source_model(data) - beta) * delta
                    follow_result = follow_model(data) - beta
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

