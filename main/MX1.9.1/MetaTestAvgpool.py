import sys
sys.path.append(".")
from main.CONSTANT import *

import csv
import mxnet as mx
from mxnet import nd            # Tensor模块
from mxnet import init          # 初始化
from mxnet.gluon import nn      # 神经网络基本结构
from mxnet.gluon.nn import AvgPool2D
from mxnet.initializer import Constant

from constant import *
from utils import *


def SourceModel(device):
    pool_size = np.random.randint(1, 5)
    strides = np.random.randint(1, 5)

    net = nn.Sequential()
    net.add(AvgPool2D(pool_size=(pool_size,pool_size), strides=(strides, strides),
                      padding=0, layout=FORMAT))
    if device == "gpu":
        net.initialize(ctx=mx.gpu())
    elif device == "cpu":
        net.initialize(ctx=mx.cpu())
    return net


if __name__ == "__main__":
    OPERATOR = "Avgpool"
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

        for muta_mode in range(0, 3):
            for i in range(100):
                source_model = SourceModel(DEVICE)
                data = generate_data(shape, DEVICE)

                res = [version, FORMAT, DEVICE, OPERATOR]
                if muta_mode == 0:
                    # 输入变异
                    # 扰动
                    if DEVICE == "gpu":
                        delta = nd.random.uniform(-DELTA, DELTA, 1, ctx=mx.gpu())[0].astype(DTYPE)
                    elif DEVICE == "cpu":
                        delta = nd.random.uniform(-DELTA, DELTA, 1, ctx=mx.cpu())[0].astype(DTYPE)
                    source_result = source_model(data) * delta
                    follow_result = source_model(data * delta)
                    dis = norm_dis(source_result, follow_result).asnumpy()[0]
                elif muta_mode == 1:
                    # 偏置变异
                    # 扰动
                    if DEVICE == "gpu":
                        delta = nd.random.uniform(-DELTA, DELTA, 1, ctx=mx.gpu())[0].astype(DTYPE)
                    elif DEVICE == "cpu":
                        delta = nd.random.uniform(-DELTA, DELTA, 1, ctx=mx.cpu())[0].astype(DTYPE)
                    source_result = source_model(data) + delta
                    follow_result = source_model(data + delta)
                    dis = norm_dis(source_result, follow_result).asnumpy()[0]
                elif muta_mode == 2:
                    delta = nd.array([0])
                    # 转置
                    if FORMAT == "NHWC":
                        source_result = nd.transpose(source_model(data), (0, 2, 1, 3))
                        follow_result = source_model(data.transpose((0, 2, 1, 3)))
                    elif FORMAT == "NCHW":
                        source_result = nd.transpose(source_model(data), (0, 1, 3, 2))
                        follow_result = source_model(data.transpose((0, 1, 3, 2)))
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
