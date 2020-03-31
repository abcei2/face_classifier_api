import cv2
import imutils
import argparse
import numpy as np
from face_classifier.classifer_util import *
from face_classifier.register_utils import *
import os, os.path
import insightface



#loading the face recognition model. 0 means to work with GPU. -1 is for CPU.
recognizer = insightface.model_zoo.get_model('arcface_r100_v1')
recognizer.prepare(ctx_id = -1)

load_model()

def do_detect(img):
    return classify_face(recognizer,img)

def do_register(img,name,WIDTHDIVIDER=1):
    try:
        os.mkdir("dataset/"+ name)
    except:
        print("dir already created")

    img = imutils.resize(img, width=int(img.shape[1]/WIDTHDIVIDER))
    img_count=len(os.listdir("dataset/"+ name +"/"))
    print(f"{name} tiene {img_count} imagenes")
    fname = "dataset/"+ name +"/" +name + str(img_count) + ".jpg"
    cv2.imwrite( fname, img )


def do_update():
    update_model(recognizer)
    load_model()