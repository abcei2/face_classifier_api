import insightface
import cv2
import numpy as np
import time
import imutils
from ast import literal_eval
import pickle
import os


def find_match(data, stored_data, thresh = 0.5):
    ldata = np.linalg.norm(data, axis=1)[None].T
    lstored = np.linalg.norm(stored_data, axis=1)[None].T
    num = np.dot(data, stored_data.T)
    den = np.dot(ldata, lstored.T)
    similarity = num/den
    #thresh_vec = np.zeros( (similarity.shape[0],1) ) + thresh
    #similarity = np.column_stack(( thresh_vec,similarity ))
    #matches = np.argmax(similarity, axis = 1)
    #--V2--
    matches = np.where(similarity>thresh, True, False)

    return matches

def true_match(data, stored_data,nnames, unames, thresh = 0.4):
    
    names = nnames.copy()
    print(nnames)
    names.remove('Uknown')
    matches_t = find_match(data, stored_data, thresh)

    names = np.asarray(names)
    #unique_names = np.unique(names)
    unique_names = unames
    t_match = np.ones( (matches_t.shape[0], 1) )

    for name in unique_names:
        un_ind = np.where(names == name)[0]
        nmax,nmin = np.max(un_ind),np.min(un_ind)
        name_matches = matches_t[:,nmin:nmax + 1]
        t_match = np.column_stack(( t_match,np.sum(name_matches,axis=1)[:,None]))
    
    r_match = np.argmax(t_match, axis= 1)

    return r_match


def scaller_conc(img):
    oheight,owidth,_ = img.shape
    if(oheight >= owidth):
        height = 112
        p = (height/oheight)
        width = owidth*p
        dim = (int(width), int(height) )
        # resize image
        resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        nl = int((112 - resized.shape[1] )/2)
        lines = np.zeros( (resized.shape[0],nl,3), np.uint8  )
        resized = np.column_stack(( lines,np.column_stack(( resized, lines )) ))
        if( ((112 - resized.shape[1])/2) != 0):
            resized = np.column_stack(( np.zeros((resized.shape[0],1,3),np.uint8 ), resized ) )
        return resized

    elif(owidth > oheight):
        width = 112
        p = (width/owidth)
        height = oheight*p
        dim = (int(width), int(height) )
        # resize image
        resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        nl = int((112 - resized.shape[0] )/2)
        lines = np.zeros( (nl,resized.shape[1],3),np.uint8  )

        resized = np.row_stack(( lines,np.row_stack(( resized, lines )) ))
        if( ((112 - resized.shape[0])/2) != 0 ):

            resized = np.row_stack(( np.zeros((1,resized.shape[1],3) ,np.uint8), resized ) )
        return resized

    else:
        return img



#data_saved = np.loadtxt('data.txt')
global data_saved,names,unames,idx,labels
data_saved=[]
names=[]
unames=[]
idx=[]
labels=[]
def load_model():

    global data_saved,names,unames,idx,labels
    data_saved=[]
    names=[]
    unames=[]
    idx=[]
    labels=[]
    with open('database/embeddings.pickle', 'rb') as f:
        data_saved = pickle.load(f)
        if(data_saved is not None):
            print('input loaded')
        else:
            print('problem with saved embeddings')
    with open('database/names.pickle', 'rb') as f:
        names = pickle.load(f)
        if(names is not None):
            print('output loaded')
        else:
            print('problem with output')
    with open('database/unames.pickle', 'rb') as f:
        unames = pickle.load(f)
        if(unames is not None):
            print('output loaded')
        else:
            print('problem with output')
    names = ['Uknown'] + names
    _,idx = np.unique(np.asarray(names), return_index=True)
    labels = np.asarray(names)[np.sort(idx)]
    print("\nLOADED MODEL!\n")

    
with open('database/embeddings.pickle', 'rb') as f:
    data_saved = pickle.load(f)
    if(data_saved is not None):
        print('input loaded')
    else:
        print('problem with saved embeddings')
with open('database/names.pickle', 'rb') as f:
    names = pickle.load(f)
    if(names is not None):
        print('output loaded')
    else:
        print('problem with output')
with open('database/unames.pickle', 'rb') as f:
    unames = pickle.load(f)
    if(unames is not None):
        print('output loaded')
    else:
        print('problem with output')
names = ['Uknown'] + names
_,idx = np.unique(np.asarray(names), return_index=True)
labels = np.asarray(names)[np.sort(idx)]
print("\nLOADED MODEL!\n")

def classify_face(recognizer,face_image):


    embeddings = np.zeros( (1,512) )
    detections={
        "face_detect":"unknown"
    }
    if face_image is not None:
        face_image = scaller_conc( face_image)
        embeddings = np.row_stack(( embeddings,recognizer.get_embedding(face_image)  ))
        #embeddings = np.delete(embeddings, 0, 0)
        
        if embeddings is not None:
            matches = true_match(embeddings,data_saved, names, unames, 0.3)  #0.5
            print(labels, matches)
            
            detections["face_detect"]=labels[matches[1]]

    return detections

