import mxnet as mx
from mxnet import nd            # Tensor模块
from mxnet.gluon import nn      # 神经网络基本结构
from mxnet.gluon.nn import Conv2D

import os
os.environ['DMLC_LOG_STACK_TRACE_DEPTH'] = "100"

def Model():
    net = nn.Sequential()
    net.add(Conv2D(channels=32, kernel_size=(5, 5), layout="NHWC"))
    net.initialize(ctx=mx.cpu())
    return net


shape = (10,32,32,3)
model = Model()
data = nd.random.uniform(-1, 1, shape, ctx=mx.cpu())
result = model(data)
print(result)
