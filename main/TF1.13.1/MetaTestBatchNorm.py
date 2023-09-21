import os.path
import sys
sys.path.append(".")
from main.CONSTANT import *

from constant import *
# from main.CONSTANT import *
from utils import *
import tensorflow as tf
# from keras.layers import BatchNormalization, Input
# from keras.models import Model
import tensorflow._api.v1.keras as K
from tensorflow._api.v1.keras.layers import BatchNormalization, Input
from tensorflow._api.v1.keras.models import Model, clone_model
import numpy as np
import h5py
import csv
import re


def SourceModel(shape):
    x = Input(shape=shape[1:])
    if FORMAT == "NCHW":
        y = BatchNormalization(axis=1, epsilon=1e-3)(x)
    elif FORMAT == "NHWC":
        y = BatchNormalization(axis=-1, epsilon=1e-3)(x)
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
    follow_model.layers[1].epsilon += delta # 写BN层的epsilon
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


def ReadSourceModelPara(source_model):
    epsilon = source_model.layers[1].epsilon
    weights = source_model.get_weights()
    weights_names = [weight.name for layer in source_model.layers for weight in layer.weights]
    weights_names.append("Epsilon")
    weights.append(epsilon)
    return weights_names, weights


def WriteMutaProcess(group, No: int,
                     input, source_result: np.ndarray, follow_result: np.ndarray,
                     model_para: tuple, muta_para: tuple):
    group_no = group.create_group("No_" + str(No))  # 创建子文件夹
    group_no.create_dataset("Input", data=input)
    group_no.create_dataset("SourceResult", data=source_result)
    group_no.create_dataset("FollowResult", data=follow_result)

    group_no_model = group_no.create_group("ModelPara") # 存放模型名称和权重
    for idx, name in enumerate(model_para[0]):  # 将模型层名称作为key值
        name = name.split("/")[-1]
        # print(name)
        group_no_model.create_dataset(name, data=model_para[1][idx])

    group_no_muta = group_no.create_group("MutaPara")   # 存放变质参数和名称
    for idx, name in enumerate(muta_para[0]):   # 将变量名称作为key值
        group_no_muta.create_dataset(name, data=muta_para[1][idx])
    return 0


def maintest():
    OPERATOR = "BN"
    TESTMODE = "metamorphosis"  # differential
    version = lib_version()
    tf.device("/cpu:0") if DEVICE == "cpu" else tf.device(DEVICE)
    # K.backend.set_floatx(DTYPE)  # 设置框架的精度位数

    shape = SHAPE
    data = generate_data(shape)

    # 保存文件到csv
    # csv_path = os.path.join(MediTestRoot, "experiment/{}/{}/text.csv".
    #                         format(version, TESTMODE, version, FORMAT, DEVICE, OPERATOR))
    csv_path = os.path.join(MediTestRoot, "experiment/{}/{}/MetaResult_{}_{}_{}_{}.csv".
                            format(version, TESTMODE, version, FORMAT, DEVICE, OPERATOR))
    with open(file=csv_path, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Lib", "Format", "Device", "Operator", "MutaMode", "Dis", "Delta"])

        source_model = SourceModel(shape)
        for muta_mode in range(0, 1):
            for i in range(100):
                data = generate_data(shape)
                res = [version, FORMAT, DEVICE, OPERATOR]
                if muta_mode == 0:
                    # 方差部分的变异
                    follow_model, delta = FollowModel_1(source_model)
                    source_result = source_model.predict(data)
                    follow_result = follow_model.predict(data)
                    dis = norm_dis(source_result, follow_result)
                elif muta_mode == 1:
                    # 输入部分的变异
                    follow_model, delta = FollowModel_2(source_model)
                    source_result = source_model.predict(data)
                    follow_result = follow_model.predict(data + delta)
                    dis = norm_dis(source_result, follow_result)
                elif muta_mode == 2:
                    # bais部分的变异
                    follow_model, delta = FollowModel_3(source_model)
                    source_result = source_model.predict(data) + delta
                    follow_result = follow_model.predict(data)
                    dis = norm_dis(source_result, follow_result)
                elif muta_mode == 3:
                    # 斜率部分的变异
                    follow_model, delta, beta = FollowModel_4(source_model)
                    beta = beta if FORMAT == "NHWC" else beta.reshape(-1, 1, 1)  # TF默认输出为NHWC
                    source_result = (source_model.predict(data) - beta) * delta
                    follow_result = follow_model.predict(data) - beta
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


if __name__ == "__main__":
    maintest()
    print("end")








