# cerebro_flask
the goal of this repository is to load a service that switch between detection models and serves to send images to get response
## repository reference
### tanks to insightface and kaiser24
https://github.com/kaiser24/Face_Recognizer

Requirements and Instalation

Python >=3.5 Numpy OpenCV >=4
Apache MXNet

https://mxnet.apache.org/get_started/?version=v1.5.1&platform=linux&language=python&environ=pip&processor=gpu

        pip3 install mxnet-cuXXX

Note: the number at the end is the cuda version. if the cuda version installed is cuda 10.1 then you should use pip3 install mxnet-cu101
Insightface

https://github.com/deepinsight/insightface

        pip3 install insightface

In case that you want to install from source to triain a custom model follow the instructions on the repository.
In case of wanting to use another deep learning library as base on the repository there's a link to versions of insightface on Tensorflow, pytorch, caffe etc.
Usage
Nota: Esta implementación emplea GPU tanto para la detección como para el reconocimiento. es posible que la GPU no sea capaz de cargar ambos modelos, o que no se disponga de GPU en absoluto, para esto se debe modificar en el archivo processing_dataset.py en las líneas 111 (detección) y 115 (reconocimiento) ctx_id de 0 a -1 para que funcione con CPU solamente, y en el archivo face_recognition_v2.py en las líneas 181 y 185.