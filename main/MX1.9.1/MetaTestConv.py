import sys
sys.path.append(".")
from main.CONSTANT import *

import csv
import mxnet as mx
from mxnet import nd            # Tensor模块
from mxnet import init          # 初始化
from mxnet.gluon import nn      # 神经网络基本结构
from mxnet.gluon.nn import Conv2D
from mxnet.initializer import Constant

from constant import *
from utils import *


def SourceModel(device):
    net = nn.Sequential()
    if FORMAT == "NCHW":
        net.add(Conv2D(channels=32, kernel_size=(5, 5), layout="NCHW"))
    elif FORMAT == "NHWC":
        net.add(Conv2D(channels=32, kernel_size=(5, 5), layout="NHWC"))
    if device == "gpu":
        net.initialize(ctx=mx.gpu())
    elif device == "cpu":
        net.initialize(ctx=mx.cpu())
    return net


def FollowModel_1(source_model, device):
    follow_model = nn.Sequential()
    # 读取模型参数
    weight = source_model[0].weight.data().copy()
    bias = source_model[0].bias.data().copy()
    # 扰动
    if device == "gpu":
        delta = 1 + nd.random.uniform(-DELTA, DELTA, 1, ctx=mx.gpu())[0].astype(DTYPE)
    elif device == "cpu":
        delta = 1 + nd.random.uniform(-DELTA, DELTA, 1, ctx=mx.cpu())[0].astype(DTYPE)
    # 变异模型
    follow_model.add(Conv2D(channels=32, kernel_size=(5, 5), layout=FORMAT,
                            weight_initializer=Constant(weight),
                            bias_initializer=Constant(bias))
            )
    # 选择设备
    if device == "gpu":
        follow_model.initialize(ctx=mx.gpu())
    elif device == "cpu":
        follow_model.initialize(ctx=mx.cpu())
    return follow_model, bias, delta


def FollowModel_2(source_model, device):
    follow_model = nn.Sequential()
    # 读取模型参数
    weight = source_model[0].weight.data().copy()
    bias = source_model[0].bias.data().copy()
    # 扰动
    if device == "gpu":
        delta = 1 + nd.random.uniform(-DELTA, DELTA, 1, ctx=mx.gpu())[0].astype(DTYPE)
    elif device == "cpu":
        delta = 1 + nd.random.uniform(-DELTA, DELTA, 1, ctx=mx.cpu())[0].astype(DTYPE)
    # 变异模型
    follow_model.add(Conv2D(channels=32, kernel_size=(5, 5), layout=FORMAT,
                            weight_initializer=Constant(weight*delta),
                            bias_initializer=Constant(bias))
            )
    # 选择设备
    if device == "gpu":
        follow_model.initialize(ctx=mx.gpu())
    elif device == "cpu":
        follow_model.initialize(ctx=mx.cpu())
    return follow_model, bias, delta


def FollowModel_3(source_model, device):
    follow_model = nn.Sequential()
    # 读取模型参数
    weight = source_model[0].weight.data().copy()
    bias = source_model[0].bias.data().copy()
    # 转置
    if FORMAT == "NCHW":
        weight = nd.transpose(weight, (0, 1, 3, 2))
    elif FORMAT =="NHWC":
        weight = nd.transpose(weight, (0, 2, 1, 3))
    # 变异模型
    follow_model.add(Conv2D(channels=32, kernel_size=(5, 5), layout=FORMAT,
                            weight_initializer=Constant(weight),
                            bias_initializer=Constant(bias))
                     )
    # 选择设备
    if device == "gpu":
        follow_model.initialize(ctx=mx.gpu())
    elif device == "cpu":
        follow_model.initialize(ctx=mx.cpu())
    return follow_model, bias


def FollowModel_4(source_model, device):
    follow_model = nn.Sequential()
    # 读取模型参数
    weight = source_model[0].weight.data().copy()
    bias = source_model[0].bias.data().copy()
    # 扰动
    if device == "gpu":
        delta = nd.random.uniform(-DELTA, DELTA, 1, ctx=mx.gpu())[0].astype(DTYPE)
    elif device == "cpu":
        delta = nd.random.uniform(-DELTA, DELTA, 1, ctx=mx.cpu())[0].astype(DTYPE)
    # 变异模型
    follow_model.add(Conv2D(channels=32, kernel_size=(5, 5), layout=FORMAT,
                            weight_initializer=Constant(weight),
                            bias_initializer=Constant(bias+delta))
                     )
    # 选择设备
    if device == "gpu":
        follow_model.initialize(ctx=mx.gpu())
    elif device == "cpu":
        follow_model.initialize(ctx=mx.cpu())
    return follow_model, delta


if __name__ == "__main__":
    OPERATOR = "Conv"
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
                    # 输入线性变异
                    follow_model, bias, delta = FollowModel_1(source_model, DEVICE)
                    bias = bias if FORMAT == "NHWC" else bias.reshape(-1, 1, 1)
                    source_result = (source_model(data) - bias) * delta
                    follow_result = follow_model(data * delta) - bias
                    dis = norm_dis(source_result, follow_result).asnumpy()[0]
                elif muta_mode == 1:
                    # 权重线性变异
                    follow_model, bias, delta = FollowModel_2(source_model, DEVICE)
                    bias = bias if FORMAT == "NHWC" else bias.reshape(-1, 1, 1)
                    source_result = (source_model(data) - bias) * delta
                    follow_result = follow_model(data) - bias
                    dis = norm_dis(source_result, follow_result).asnumpy()[0]
                elif muta_mode == 2:
                    # 转置变异
                    follow_model, bias = FollowModel_3(source_model, DEVICE)
                    bias = bias if FORMAT == "NHWC" else bias.reshape(-1, 1, 1)
                    delta = nd.array([0])
                    if FORMAT == "NHWC":
                        source_result = nd.transpose(source_model(data) - bias, (0, 2, 1, 3))
                        follow_result = follow_model(data.transpose((0, 2, 1, 3))) - bias
                    elif FORMAT == "NCHW":
                        source_result = nd.transpose(source_model(data) - bias, (0, 1, 3, 2))
                        follow_result = follow_model(data.transpose((0, 1, 3, 2))) - bias
                    dis = norm_dis(source_result, follow_result).asnumpy()[0]
                elif muta_mode == 3:
                    # 偏置变异
                    follow_model, delta = FollowModel_4(source_model, DEVICE)
                    source_result = source_model(data) + delta
                    follow_result = follow_model(data)
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
                print("{};{};{};{};Iter:{};MutaMode:{};Dis:{};".format(version, OPERATOR, FORMAT, DEVICE, i, muta_mode,
                                                                       dis))

    print("end")



