import sys
sys.path.append(".")
from main.CONSTANT import *
import numpy as np
import copy
import csv
import mindspore as ms
from mindspore import Tensor, Parameter, ops, Model
from mindspore.ops import BatchNorm
from mindspore.nn import BatchNorm2d
from mindspore import dtype as mstype
from constant import *
from utils import *


def SourceModel(feature):
    bn = BatchNorm2d(feature, eps=1e-3, gamma_init=1, beta_init=0, moving_mean_init=0, moving_var_init=1,
                     data_format=FORMAT)
    return bn


def FollowModel_1(source_model):
    # 变质参数
    delta = np.random.uniform(-1e-3, 1e-3, 1)[0].astype(DTYPE)
    # 变异模型
    follow_model = BatchNorm2d(num_features=source_model.num_features,
                               eps=source_model.eps+delta,
                               gamma_init=source_model.parameters_dict()["gamma"],
                               beta_init=source_model.parameters_dict()["beta"],
                               moving_mean_init=source_model.parameters_dict()['mean'],
                               moving_var_init=source_model.parameters_dict()["variance"]-Tensor(delta),
                               data_format=source_model.format)
    return follow_model, delta


def FollowModel_2(source_model):
    # 变质参数
    delta = np.random.uniform(-DELTA, DELTA, 1)[0].astype(DTYPE)
    # 变异模型
    follow_model = BatchNorm2d(num_features=source_model.num_features,
                               eps=source_model.eps,
                               gamma_init=source_model.parameters_dict()["gamma"],
                               beta_init=source_model.parameters_dict()["beta"],
                               moving_mean_init=source_model.parameters_dict()['mean'] + Tensor(delta),
                               moving_var_init=source_model.parameters_dict()["variance"],
                               data_format=source_model.format)
    return follow_model, delta


def FollowModel_3(source_model):
    # 变质参数
    delta = np.random.uniform(-DELTA, DELTA, 1)[0].astype(DTYPE)
    # 变质模型
    follow_model = BatchNorm2d(num_features=source_model.num_features,
                               eps=source_model.eps,
                               gamma_init=source_model.parameters_dict()["gamma"],
                               beta_init=source_model.parameters_dict()["beta"] + Tensor(delta),
                               moving_mean_init=source_model.parameters_dict()['mean'],
                               moving_var_init=source_model.parameters_dict()["variance"],
                               data_format=source_model.format)
    return follow_model, delta


def FollowModel_4(source_model):
    # 变质参数
    delta = 1+np.random.uniform(-DELTA, DELTA, 1)[0].astype(DTYPE)
    # 变质模型
    follow_model = BatchNorm2d(num_features=source_model.num_features,
                               eps=source_model.eps,
                               gamma_init=source_model.parameters_dict()["gamma"] * Parameter(delta),
                               beta_init=source_model.parameters_dict()["beta"],
                               moving_mean_init=source_model.parameters_dict()['mean'],
                               moving_var_init=source_model.parameters_dict()["variance"],
                               data_format=source_model.format)
    # beta = copy.deepcopy(source_model.parameters_dict()["beta"])
    beta = source_model.parameters_dict()["beta"]
    return follow_model, beta, delta


def maintest():
    OPERATOR = "BN"
    TESTMODE = "metamorphosis"  # differential
    version = lib_version()
    ms.context.set_context(device_target=DEVICE.upper())  # 设置设备

    shape = SHAPE
    feature_num = shape[1] if FORMAT == "NCHW" else shape[-1]
    data = generate_data(shape)

    # 保存文件到csv
    csv_path = os.path.join(MediTestRoot, "experiment/{}/{}/MetaResult_{}_{}_{}_{}.csv".
                            format(version, TESTMODE, version, FORMAT, DEVICE, OPERATOR))
    with open(file=csv_path, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Lib", "Format", "Device", "Operator", "MutaMode", "Dis", "Delta"])

        # 初始化source模型
        source_model = SourceModel(feature=feature_num)
        source_result = source_model(data)

        for muta_mode in range(0, 4):
            for i in range(100):
                data = generate_data(shape)
                res = [version, FORMAT, DEVICE, OPERATOR]
                if muta_mode == 0:
                    # 方差蜕变
                    follow_model, delta = FollowModel_1(source_model)
                    source_result = source_model(data)
                    follow_result = follow_model(data)
                    dis = norm_dis(source_result, follow_result).asnumpy()[()]
                elif muta_mode == 1:
                    # 输入+模型蜕变
                    follow_model, delta = FollowModel_2(source_model)
                    source_result = source_model(data)
                    follow_result = follow_model(data + Tensor(delta))
                    dis = norm_dis(source_result, follow_result).asnumpy()[()]
                elif muta_mode == 2:
                    # bias蜕变
                    follow_model, delta = FollowModel_3(source_model)
                    source_result = source_model(data) + Tensor(delta)
                    follow_result = follow_model(data)
                    dis = norm_dis(source_result, follow_result).asnumpy()[()]
                elif muta_mode == 3:
                    follow_model, beta, delta = FollowModel_4(source_model)
                    beta = beta.reshape(-1, 1, 1) if FORMAT == "NCHW" else beta
                    source_result = (source_model(data) - beta) * Tensor(delta)
                    follow_result = follow_model(data) - beta
                    dis = norm_dis(source_result, follow_result).asnumpy()[()]
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







