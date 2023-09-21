import sys
sys.path.append(".")
from main.CONSTANT import *
import numpy as np
import copy
import csv
import mindspore as ms
from mindspore import Tensor, Parameter, ops, Model, context
from mindspore.nn import Conv2d
from mindspore import dtype as mstype
from constant import *
from utils import *


def SourceModel(in_channels):
    conv = Conv2d(in_channels=in_channels, out_channels=32, kernel_size=(5, 5), pad_mode="valid", has_bias=True)
    return conv


def FollowModel_1(source_model):
    # 变质参数
    delta = 1 + np.random.uniform(-DELTA, DELTA, 1)[0].astype(DTYPE)
    # 变质模型
    follow_model = DepthwiseConv2d(in_channels=source_model.in_channels, out_channels=source_model.out_channels,
                          kernel_size=source_model.kernel_size, pad_mode=source_model.pad_mode,
                          has_bias=source_model.has_bias,
                          weight_init=Tensor(source_model.weight),
                          bias_init=Tensor(source_model.bias))
    bias = source_model.parameters_dict()["bias"]
    return follow_model, bias, delta


def FollowModel_2(source_model):
    # 变质参数
    delta = 1 + np.random.uniform(-DELTA, DELTA, 1)[0].astype(DTYPE)
    # 变质模型
    follow_model = DepthwiseConv2d(in_channels=source_model.in_channels, out_channels=source_model.out_channels,
                          kernel_size=source_model.kernel_size, pad_mode=source_model.pad_mode,
                          has_bias=source_model.has_bias,
                          weight_init=Tensor(source_model.weight)*delta,
                          bias_init=Tensor(source_model.bias))
    bias = source_model.parameters_dict()["bias"]
    return follow_model, bias, delta


def FollowModel_3(source_model):
    # 变质模型
    follow_model = DepthwiseConv2d(in_channels=source_model.in_channels, out_channels=source_model.out_channels,
                          kernel_size=source_model.kernel_size, pad_mode=source_model.pad_mode,
                          has_bias=source_model.has_bias,
                          weight_init=Tensor(source_model.weight.asnumpy().transpose(0,1,3,2)) if FORMAT=="NCHW"
                          else Tensor(source_model.weight.asnumpy().transpose(0,2,1,3)),
                          bias_init=Tensor(source_model.bias))
    bias = source_model.parameters_dict()["bias"]
    return follow_model, bias


def FollowModel_4(source_model):
    # 变质参数
    delta = np.random.uniform(-DELTA, DELTA, 1)[0].astype(DTYPE)
    # 变质模型
    follow_model = DepthwiseConv2d(in_channels=source_model.in_channels, out_channels=source_model.out_channels,
                          kernel_size=source_model.kernel_size, pad_mode=source_model.pad_mode,
                          has_bias=source_model.has_bias,
                          weight_init=Tensor(source_model.weight),
                          bias_init=Tensor(source_model.bias)+Tensor(delta))
    return follow_model, delta


def maintest():
    OPERATOR = "Conv"
    TESTMODE = "metamorphosis"  # differential
    version = lib_version()
    context.set_context(device_target=DEVICE.upper())  # 设置设备

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
        source_model = SourceModel(in_channels=feature_num)
        source_result = source_model(data)

        for muta_mode in range(0, 4):
            for i in range(100):
                data = generate_data(shape)
                res = [version, FORMAT, DEVICE, OPERATOR]
                if muta_mode == 0:
                    # 输入蜕变
                    follow_model, bias, delta = FollowModel_1(source_model)
                    bias = Tensor(bias.asnumpy().reshape(-1, 1, 1)) if FORMAT == "NCHW" else bias
                    # bias = bias.reshape(-1, 1, 1) if FORMAT == "NCHW" else bias
                    source_result = (source_model(data) - bias) * delta
                    follow_result = follow_model(data * delta) - bias
                    dis = norm_dis(Tensor(source_result), Tensor(follow_result))
                elif muta_mode == 1:
                    # 模型蜕变 斜率
                    follow_model, bias, delta = FollowModel_2(source_model)
                    bias = Tensor(bias.asnumpy().reshape(-1, 1, 1)) if FORMAT == "NCHW" else bias
                    # bias = bias.reshape(-1, 1, 1) if FORMAT == "NCHW" else bias
                    source_result = (source_model(data) - bias) * delta
                    follow_result = follow_model(data) - bias
                    dis = norm_dis(Tensor(source_result), Tensor(follow_result))
                elif muta_mode == 2:
                    # 输入+模型蜕变 转置
                    follow_model, bias = FollowModel_3(source_model)
                    delta = 0
                    bias = Tensor(bias.asnumpy().reshape(-1, 1, 1)) if FORMAT == "NCHW" else bias
                    # bias = bias.reshape(-1, 1, 1) if FORMAT == "NCHW" else bias
                    if FORMAT == "NCHW":
                        source_result = (source_model(data) - bias).asnumpy().transpose(0, 1, 3, 2)
                        follow_result = follow_model(Tensor(data.asnumpy().transpose(0, 1, 3, 2))) - bias
                    elif FORMAT == "NHWC":
                        source_result = (source_model(data) - bias).transpose(0, 2, 1, 3)
                        follow_result = follow_model(Tensor(data.asnumpy().transpose(0, 2, 1, 3))) - bias
                    dis = norm_dis(Tensor(source_result), Tensor(follow_result))
                elif muta_mode == 3:
                    # 偏移蜕变
                    follow_model, delta = FollowModel_4(source_model)
                    source_result = source_model(data) + Tensor(delta)
                    follow_result = follow_model(data)
                    dis = norm_dis(Tensor(source_result), Tensor(follow_result))
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


