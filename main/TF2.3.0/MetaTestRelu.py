import sys
sys.path.append(".")
from main.CONSTANT import *

import tensorflow as tf
import tensorflow.keras as K
from tensorflow.keras.layers import Input, ReLU
from tensorflow.keras.models import Model, clone_model

import numpy as np
import h5py
import csv
import re
import constant
from utils import *


def SourceModel(shape):
    x = Input(shape=shape[1:])
    y = ReLU()(x)
    model = Model(x, y)
    return model


def maintest():
    OPERATOR = "Relu"
    TESTMODE = "metamorphosis"  # differential
    version = lib_version()

    shape = SHAPE
    # np.random.seed(0)
    data = generate_data(shape)
    source_model = SourceModel(shape)

    csv_path = os.path.join(MediTestRoot, "experiment/{}/{}/MetaResult_{}_{}_{}_{}.csv".
                            format(version, TESTMODE, version, FORMAT, DEVICE, OPERATOR))
    with open(file=csv_path, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Lib", "Format", "Device", "Operator", "MutaMode", "Dis", "Delta"])

        for muta_mode in range(4):
            for i in range(100):
                data = generate_data(shape)

                res = [version, FORMAT, DEVICE, OPERATOR]
                if muta_mode == 0:
                    delta = 0
                    # 输入蜕变
                    source_result = np.abs(data)
                    follow_result = source_model(data) + source_model(-data)
                    dis = norm_dis(source_result, follow_result)
                elif muta_mode == 1:
                    delta = np.random.uniform(0, DELTA, 1)[0]
                    source_result = source_model(delta * data)
                    follow_result = delta * source_model(data)
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
    maintest()
    print("end")


