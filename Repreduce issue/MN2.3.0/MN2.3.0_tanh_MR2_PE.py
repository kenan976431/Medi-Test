import MNN.expr as _F
from MNN.expr import tanh, sinh, cosh
import numpy
# import numpy as np
# from numpy import tanh, sinh, cosh
import MNN.numpy as np

if __name__ == "__main__":
    shape = (10, 3, 32, 32)
    R=1
    for i in range(100):
        # data = np.array(numpy.random.uniform(-1, 1, shape).tolist(), dtype=_F.float)
        # delta = np.array(numpy.random.uniform(-R, R, 1).tolist(), dtype=_F.float)
        data = np.random.uniform(-1, 1, shape).astype("float32")
        delta = np.random.uniform(-R, R, 1).astype("float32")

        source_result = tanh(data + delta)
        follow_result = (tanh(data) + tanh(delta)) \
                        / (1 + tanh(data) * tanh(delta))
        error = np.sum(abs(source_result-follow_result))
        # flag = numpy.allclose(source_result.read(), follow_result.read())
        flag = numpy.allclose(follow_result, source_result)
        print(i, error, flag)



