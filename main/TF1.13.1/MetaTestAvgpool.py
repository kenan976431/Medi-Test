import sys
sys.path.append(".")
from main.CONSTANT import *

from constant import *
from utils import *
import tensorflow as tf
# from keras.layers import BatchNormalization, Input
# from keras.models import Model
import tensorflow._api.v1.keras as K
from tensorflow._api.v1.keras.layers import Input, AvgPool2D
from tensorflow._api.v1.keras.models import Model, clone_model
import numpy as np
import h5py
import csv
import re


def SourceModel(shape):
    pool_size = np.random.randint(1, 5)
    strides = np.random.randint(1, 5)
    data_format = "channels_last" if FORMAT=="NHWC" else "channels_first"
    x = Input(shape=shape[1:])
    y = AvgPool2D(pool_size=(pool_size, pool_size), strides=(strides, strides),
                  padding="valid", data_format=data_format)(x)
    model = Model(x, y)
    return model


def maintest():
    OPERATOR = "Avgpool"
    TESTMODE = "metamorphosis"  # differential
    version = lib_version()
    tf.device("/cpu:0") if DEVICE == "cpu" else tf.device(DEVICE)
    # K.backend.set_floatx(DTYPE)  # 设置框架的精度位数

    shape = SHAPE
    data = generate_data(shape)

    # 保存文件到csv
    csv_path = os.path.join(MediTestRoot, "experiment/{}/{}/MetaResult_{}_{}_{}_{}.csv".
                            format(version, TESTMODE, version, FORMAT, DEVICE, OPERATOR))
    with open(file=csv_path, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Lib", "Format", "Device", "Operator", "MutaMode", "Dis", "Delta"])

        for muta_mode in range(0, 4):
            for i in range(100):
                source_model = SourceModel(shape)
                data = generate_data(shape)

                res = [version, FORMAT, DEVICE, OPERATOR]
                if muta_mode == 0:
                    # 输入系数
                    delta = np.random.uniform(-DELTA, DELTA, 1)[0]
                    source_result = source_model.predict(data) * delta
                    follow_result = source_model.predict(data * delta)
                    dis = norm_dis(source_result, follow_result)
                elif muta_mode == 1:
                    # 输入偏置
                    delta = np.random.uniform(-DELTA, DELTA, 1)[0]
                    source_result = source_model.predict(data) + delta
                    follow_result = source_model.predict(data + delta)
                    dis = norm_dis(source_result, follow_result)
                elif muta_mode == 2:
                    delta = 0
                    # 转置
                    if FORMAT == "NHWC":
                        source_result = np.transpose(source_model.predict(data), (0, 2, 1, 3))
                        follow_result = source_model.predict(data.transpose(0, 2, 1, 3))
                    elif FORMAT == "NCHW":
                        source_result = np.transpose(source_model.predict(data), (0, 1, 3, 2))
                        follow_result = source_model.predict(data.transpose(0, 1, 3, 2))
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








