# MediTest

Official implementation paper A Miss Is as Good as A Mile: Metamorphic Testing for Deep Learning Operators



## testing library




| Name | version     | 
| :-------- | :------- | 
| `Tensorflow` | `1.13.1` | 
| `Tensorflow` | `2.3.0` | 
| `Pytorch` | `1.1.0` | 
| `Pytorch` | `1.10.0` |  
| `Mindspore` | `1.6.1` | 
| `Mindspore` | `1.9.0` | 
| `MXnet` | `1.9.1` | 
| `MNN` | `2.3.0` | 

Take testing LeakyReLu in tensorflow 1.13.1 as an example you can using following commands 
#### command

```http
python main/TF1.13.1/MetaTestLeakyRelu.py --device cpu --format NHWC --delta $DELTA 
python main/TF1.13.1/MetaTestLeakyRelu.py --device cpu --format NCHW --delta $DELTA 
python main/TF1.13.1/MetaTestLeakyRelu.py --device gpu --format NHWC --delta $DELTA
python main/TF1.13.1/MetaTestLeakyRelu.py --device gpu --format NCHW --delta $DELTA
```



