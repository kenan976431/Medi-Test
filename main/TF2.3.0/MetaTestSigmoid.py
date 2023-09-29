import sys
sys.path.append(".")
from main.CONSTANT import *

import tensorflow as tf
import tensorflow.keras as K
from tensorflow.keras.layers import Input, Softmax
from tensorflow.keras.models import Model, clone_model

import numpy as np
import h5py
import csv
import re
import constant
from utils import *

def maintest():
    OPERATOR = "Sigmoid"
    TESTMODE = "metamorphosis"  # differential
    version = lib_version()
    tf.device("/cpu:0") if DEVICE == "cpu" else tf.device(DEVICE)
    shape = SHAPE
    # np.random.seed(0)
    data = generate_data(shape)


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
                    # 输入蜕变
                    delta = np.random.uniform(-DELTA, DELTA, 1)[0]
                    input=data*delta
                    if FORMAT=="NHWC":
                        source_result=tf.nn.sigmoid(tf.convert_to_tensor(input)).numpy().transpose(0,2,1,3)
                        follow_result=tf.nn.sigmoid(tf.convert_to_tensor(input.transpose(0,2,1,3))).numpy()
                        dis = norm_dis(source_result, follow_result)
                    elif FORMAT=="NCHW":
                        source_result = tf.nn.sigmoid(tf.convert_to_tensor(input)).numpy().transpose(0, 1, 3, 2)
                        follow_result = tf.nn.sigmoid(tf.convert_to_tensor(input.transpose(0, 1, 3, 2))).numpy()
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