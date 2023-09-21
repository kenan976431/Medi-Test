import sys
sys.path.append(".")
from main.CONSTANT import *

import csv
import mxnet as mx
from mxnet import nd            # Tensor模块
from mxnet import init          # 初始化
from mxnet.gluon import nn      # 神经网络基本结构
from mxnet.ndarray.op import softmax

from constant import *
from utils import *


if __name__ == "__main__":
    OPERATOR = "Softmax"
    TESTMODE = "metamorphosis"  # differential
    version = lib_version()

    shape = SHAPE
    data = generate_data(shape, DEVICE)

    csv_path = os.path.join(MediTestRoot, "experiment/{}/{}/MetaResult_{}_{}_{}_{}.csv".
                            format(version, TESTMODE, version, FORMAT, DEVICE, OPERATOR))
    with open(file=csv_path, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Lib", "Format", "Device", "Operator", "MutaMode", "Dis", "Delta"])

        for muta_mode in range(1):
            for i in range(100):
                data = generate_data(shape, DEVICE)

                res = [version, FORMAT, DEVICE, OPERATOR]
                if muta_mode == 0:
                    # 输入蜕变
                    if DEVICE == "gpu":
                        delta = nd.random.uniform(-DELTA, DELTA, 1, ctx=mx.gpu())[0].astype(DTYPE)
                    elif DEVICE == "cpu":
                        delta = nd.random.uniform(-DELTA, DELTA, 1, ctx=mx.cpu())[0].astype(DTYPE)
                    if FORMAT == "NCHW":
                        axis = 1
                    else:
                        axis = -1
                    source_result = softmax(data, axis=axis)
                    follow_result = softmax(data + delta, axis=axis)
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




