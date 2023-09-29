import sys
sys.path.append(".")
from main.CONSTANT import *

import tensorflow as tf
import tensorflow.keras as K
from tensorflow.keras.layers import BatchNormalization, Input
from tensorflow.keras.models import Model, clone_model
from tensorflow.keras.initializers import Constant, random_uniform
import numpy as np
import h5py
import csv
import re
# from main.CONSTANT import *
# from constant import *
from utils import *


def SourceModel(shape):
    x = Input(shape=shape[1:])
    if FORMAT == "NCHW":
        y = BatchNormalization(axis=1)(x)
    elif FORMAT == "NHWC":
        y = BatchNormalization(axis=-1)(x)
    return Model(x, y)


def FollowModel_1(source_model):
    follow_model = clone_model(source_model)
    # 读取参数
    weights = source_model.get_weights()
    weights_names = [weight.name for layer in source_model.layers for weight in layer.weights]
    variance_idx = FindWeightsIdx("variance", weights_names)
    variance = weights[variance_idx]    # 源模型的方差
    epsilon = source_model.layers[1].epsilon    # 读取BN层的epsilon

    # 变异模型
    delta = np.random.uniform(-1e-3, 1e-3, 1)[0].astype(DTYPE)
    # delta = np.random.uniform(-DELTA, DELTA, 1)[0].astype(DTYPE)
    follow_model.layers[1].epsilon += delta     # 写BN层的epsilon
    weights[variance_idx] -= delta
    follow_model.set_weights(weights)

    return follow_model, delta


def FollowModel_2(source_model):
    follow_model = clone_model(source_model)
    # 读取参数
    weights = source_model.get_weights()
    weights_names = [weight.name for layer in source_model.layers for weight in layer.weights]
    mean_idx = FindWeightsIdx("mean", weights_names)
    mean = weights[mean_idx]    # 源BN的均值

    # 变异模型
    # delta = np.random.uniform(-np.average(mean)/100, np.average(mean)/100, 1)[0].astype(np.float32)
    delta = np.random.uniform(-DELTA, DELTA, 1)[0].astype(DTYPE)
    weights[mean_idx] += delta
    follow_model.set_weights(weights)

    return follow_model, delta


def FollowModel_3(source_model):
    follow_model = clone_model(source_model)
    # 读取参数
    weights = source_model.get_weights()
    weights_names = [weight.name for layer in source_model.layers for weight in layer.weights]
    beta_idx = FindWeightsIdx("beta", weights_names)
    beta = weights[beta_idx]

    # 变异模型
    delta = np.random.uniform(-DELTA, DELTA, 1)[0].astype(DTYPE)
    weights[beta_idx] += delta
    follow_model.set_weights(weights)

    return follow_model, delta


def FollowModel_4(source_model):
    follow_model = clone_model(source_model)
    # 读取参数
    weights = source_model.get_weights()
    weights_names = [weight.name for layer in source_model.layers for weight in layer.weights]
    gamma_idx = FindWeightsIdx("gamma", weights_names)
    gamma = weights[gamma_idx]
    beta_idx = FindWeightsIdx("beta", weights_names)
    beta = weights[beta_idx]

    # 变异模型
    delta = 1+np.random.uniform(-DELTA, DELTA, 1)[0].astype(DTYPE)
    weights[gamma_idx] *= delta
    follow_model.set_weights(weights)

    return follow_model, delta, beta


def maintest():
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
        for muta_mode in range(0, 4):
            for i in range(100):
                data = generate_data(shape)
                res = [version, FORMAT, DEVICE, OPERATOR]
                if muta_mode == 0:
                    # 方差部分的变异
                    follow_model, delta = FollowModel_1(source_model)
                    source_result = source_model(data)
                    follow_result = follow_model(data)
                    dis = norm_dis(source_result, follow_result)
                elif muta_mode == 1:
                    # 输入部分的变异
                    follow_model, delta = FollowModel_2(source_model)
                    source_result = source_model(data)
                    follow_result = follow_model(data + delta)
                    dis = norm_dis(source_result, follow_result)
                elif muta_mode == 2:
                    # bais部分的变异
                    follow_model, delta = FollowModel_3(source_model)
                    source_result = source_model(data) + delta
                    follow_result = follow_model(data)
                    dis = norm_dis(source_result, follow_result)
                elif muta_mode == 3:
                    # 斜率部分的变异
                    follow_model, delta, beta = FollowModel_4(source_model)
                    beta = beta if FORMAT == "NHWC" else beta.reshape(-1, 1, 1)  # TF默认输出为NHWC
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
                print("{};{};{};{};Iter:{};MutaMode:{};Dis:{};".format(version, OPERATOR, FORMAT, DEVICE, i, muta_mode,
                                                                       dis))



if __name__ == "__main__":
    # maintest()

    print("end")








