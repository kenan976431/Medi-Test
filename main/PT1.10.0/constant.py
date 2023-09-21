import argparse

LIB_NAME = "PT"
DEVICE = "cpu"
FORMAT = "NCHW"
DTYPE = "float32"   # 模型及数据均使用float32
DELTA = 10

parser = argparse.ArgumentParser()
parser.add_argument('--device', default=DEVICE, choices=["gpu", "cpu"])
parser.add_argument('--format', default=FORMAT, choices=["NCHW", "NHWC"])
parser.add_argument('--delta', default=DELTA, choices=[100, 50, 10, 1, 0.1, 0.01, 0.001], type=float)
args = parser.parse_args()
DEVICE = args.device
FORMAT = args.format
DELTA = args.delta

SHAPE = (10, 3, 32, 32)
DATA_RANGE = [-1, 1]

import os
if DEVICE == "gpu":
    # os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'
    os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
    os.environ["CUDA_VISIBLE_DEVICES"] = "1"


