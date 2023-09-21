import sys
sys.path.append(".")
from main.CONSTANT import *

import csv
import mxnet as mx
from mxnet import nd            # Tensor模块
from mxnet import init          # 初始化
from mxnet.gluon import nn      # 神经网络基本结构
from mxnet.gluon.nn import BatchNorm
from mxnet.initializer import Constant

from constant import *
from utils import *


def SourceModel(device):
    net = nn.Sequential()
    if FORMAT == "NCHW":
        axis = 1
    elif FORMAT == "NHWC":
        axis = -1
    net.add(BatchNorm(axis=axis, epsilon=1e-3))
    if device == "gpu":
        net.initialize(ctx=mx.gpu())
    elif device == "cpu":
        net.initialize(ctx=mx.cpu())
    return net


def FollowModel_1(source_model, device):
    follow_model = nn.Sequential()
    # 读取模型参数
    gamma = source_model[0].gamma.data().copy()
    beta = source_model[0].beta.data().copy()
    mean = source_model[0].running_mean.data().copy()
    var = source_model[0].running_var.data().copy()
    eps = source_model[0]._kwargs["eps"]
    axis = source_model[0]._kwargs["axis"]
    # 扰动
    if device == "gpu":
        delta = nd.random.uniform(-1e-3, 1e-3, 1, ctx=mx.gpu())[0].astype(DTYPE)
        # delta = nd.random.uniform(-DELTA, DELTA, 1, ctx=mx.gpu())[0].astype(DTYPE)
    elif device == "cpu":
        delta = nd.random.uniform(-1e-3, 1e-3, 1, ctx=mx.cpu())[0].astype(DTYPE)
        # delta = nd.random.uniform(-DELTA, DELTA, 1, ctx=mx.cpu())[0].astype(DTYPE)
    # 变异模型
    follow_model.add(BatchNorm(axis=axis, epsilon=eps+delta.asnumpy()[0],
                               gamma_initializer=Constant(gamma),
                               beta_initializer=Constant(beta),
                               running_mean_initializer=Constant(mean),
                               running_variance_initializer=Constant(var-delta)))
    # 选择设备
    if device == "gpu":
        follow_model.initialize(ctx=mx.gpu())
    elif device == "cpu":
        follow_model.initialize(ctx=mx.cpu())
    return follow_model, delta


def FollowModel_2(source_model, device):
    follow_model = nn.Sequential()
    # 读取模型参数
    gamma = source_model[0].gamma.data().copy()
    beta = source_model[0].beta.data().copy()
    mean = source_model[0].running_mean.data().copy()
    var = source_model[0].running_var.data().copy()
    eps = source_model[0]._kwargs["eps"]
    axis = source_model[0]._kwargs["axis"]
    # 扰动
    if device == "gpu":
        delta = nd.random.uniform(-DELTA, DELTA, 1, ctx=mx.gpu())[0].astype(DTYPE)
    elif device == "cpu":
        delta = nd.random.uniform(-DELTA, DELTA, 1, ctx=mx.cpu())[0].astype(DTYPE)
    # 变异模型
    follow_model.add(BatchNorm(axis=axis, epsilon=eps,
                               gamma_initializer=Constant(gamma),
                               beta_initializer=Constant(beta),
                               running_mean_initializer=Constant(mean+delta),
                               running_variance_initializer=Constant(var)))
    # 选择设备
    if device == "gpu":
        follow_model.initialize(ctx=mx.gpu())
    elif device == "cpu":
        follow_model.initialize(ctx=mx.cpu())
    return follow_model, delta


def FollowModel_3(source_model, device):
    follow_model = nn.Sequential()
    # 读取模型参数
    gamma = source_model[0].gamma.data().copy()
    beta = source_model[0].beta.data().copy()
    mean = source_model[0].running_mean.data().copy()
    var = source_model[0].running_var.data().copy()
    eps = source_model[0]._kwargs["eps"]
    axis = source_model[0]._kwargs["axis"]
    # 扰动
    if device == "gpu":
        delta = nd.random.uniform(-DELTA, DELTA, 1, ctx=mx.gpu())[0].astype(DTYPE)
    elif device == "cpu":
        delta = nd.random.uniform(-DELTA, DELTA, 1, ctx=mx.cpu())[0].astype(DTYPE)
    # 变异模型
    follow_model.add(BatchNorm(axis=axis, epsilon=eps,
                               gamma_initializer=Constant(gamma),
                               beta_initializer=Constant(beta+delta),
                               running_mean_initializer=Constant(mean),
                               running_variance_initializer=Constant(var)))
    # 选择设备
    if device == "gpu":
        follow_model.initialize(ctx=mx.gpu())
    elif device == "cpu":
        follow_model.initialize(ctx=mx.cpu())
    return follow_model, delta


def FollowModel_4(source_model, device):
    follow_model = nn.Sequential()
    # 读取模型参数
    gamma = source_model[0].gamma.data().copy()
    beta = source_model[0].beta.data().copy()
    mean = source_model[0].running_mean.data().copy()
    var = source_model[0].running_var.data().copy()
    eps = source_model[0]._kwargs["eps"]
    axis = source_model[0]._kwargs["axis"]
    # 扰动
    if device == "gpu":
        delta = 1+nd.random.uniform(-DELTA, DELTA, 1, ctx=mx.gpu())[0].astype(DTYPE)
    elif device == "cpu":
        delta = 1+nd.random.uniform(-DELTA, DELTA, 1, ctx=mx.cpu())[0].astype(DTYPE)
    # 变异模型
    follow_model.add(BatchNorm(axis=axis, epsilon=eps,
                               gamma_initializer=Constant(gamma*delta),
                               beta_initializer=Constant(beta),
                               running_mean_initializer=Constant(mean),
                               running_variance_initializer=Constant(var)))
    # 选择设备
    if device == "gpu":
        follow_model.initialize(ctx=mx.gpu())
    elif device == "cpu":
        follow_model.initialize(ctx=mx.cpu())
    return follow_model, delta, beta


if __name__ == "__main__":
    OPERATOR = "BN"
    TESTMODE = "metamorphosis"  # differential
    version = lib_version()

    shape = SHAPE
    data = generate_data(shape, DEVICE)

    source_model = SourceModel(DEVICE)
    source_model(data)

    # 保存文件到csv
    csv_path = os.path.join(MediTestRoot, "experiment/{}/{}/MetaResult_{}_{}_{}_{}.csv".
                            format(version, TESTMODE, version, FORMAT, DEVICE, OPERATOR))
    with open(file=csv_path, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Lib", "Format", "Device", "Operator", "MutaMode", "Dis", "Delta"])

        for muta_mode in range(0, 4):
            for i in range(100):
                data = generate_data(shape, DEVICE)
                res = [version, FORMAT, DEVICE, OPERATOR]

                if muta_mode == 0:
                    # 方差变异
                    follow_model, delta = FollowModel_1(source_model, DEVICE)
                    source_result = source_model(data)
                    follow_result = follow_model(data)
                    dis = norm_dis(source_result, follow_result).asnumpy()[0]
                elif muta_mode == 1:
                    # 均值变异
                    follow_model, delta = FollowModel_2(source_model, DEVICE)
                    source_result = source_model(data)
                    follow_result = follow_model(data + delta)
                    dis = norm_dis(source_result, follow_result).asnumpy()[0]
                elif muta_mode == 2:
                    # 偏置变异
                    follow_model, delta = FollowModel_3(source_model, DEVICE)
                    source_result = source_model(data) + delta
                    follow_result = follow_model(data)
                    dis = norm_dis(source_result, follow_result).asnumpy()[0]
                elif muta_mode == 3:
                    # 权重变异
                    follow_model, delta, beta = FollowModel_4(source_model, DEVICE)
                    beta = beta if FORMAT == "NHWC" else beta.reshape(-1, 1, 1)  # TF默认输出为NHWC
                    source_result = (source_model(data) - beta) * delta
                    follow_result = follow_model(data) - beta
                    dis = norm_dis(source_result, follow_result).asnumpy()[0]
                else:
                    break
                # 保存到csv
                delta = delta.asnumpy()[0]
                res.append("MutaMode" + str(muta_mode))
                res.append(dis)
                res.append(delta)
                csv_writer.writerow(res)
                # 输出显示
                print("{};{};{};{};Iter:{};MutaMode:{};Dis:{};".format(version, OPERATOR, FORMAT, DEVICE, i,
                                                                       muta_mode, dis))
    print("end")






