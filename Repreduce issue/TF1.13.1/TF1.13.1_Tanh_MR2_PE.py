import tensorflow._api.v1.keras as K
from tensorflow._api.v1.keras.layers import Input, Activation
from tensorflow._api.v1.keras.activations import tanh
from tensorflow._api.v1.keras.models import Model, clone_model
import numpy as np
import os

def SourceModel(shape):
    x = Input(shape=shape[1:])
    y = Activation("tanh")(x)

    return Model(x, y)

DEVICE = "cpu"
if DEVICE == "cpu":
    os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
    import tensorflow as tf
    tf.device("\cpu:0")
elif DEVICE == "gpu":
    import tensorflow as tf
    os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'
    os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
    os.environ["CUDA_VISIBLE_DEVICES"] = "1"
    gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.1)
    sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options))

shape = (10, 32, 32, 3)
data = np.random.uniform(-1, 1, shape)
source_model = SourceModel(shape)

# delta = np.random.uniform(-10, 10, 1)[0]
delta = -3.9105
source_result = source_model.predict(data + delta)
follow_result = (source_model.predict(data) + source_model.predict(np.zeros(shape) + delta)) \
                                    / (1 + source_model.predict(data) * source_model.predict(np.zeros(shape) + delta))
dis = np.sum(abs(source_result-follow_result))
max_dis = np.max(abs(source_result-follow_result))
print("device:{}; delta:{}; dis:{}; max:{}".format(DEVICE, delta, dis, max_dis))


