import cv2
import numpy as np
import pickle
import os

def compare_embeddings(emb1t, emb2t):
    emb1 = emb1t.flatten()
    emb2 = emb2t.flatten()
    from numpy.linalg import norm
    sim = np.dot(emb1, emb2)/(norm(emb1)*norm(emb2))
    return sim

#def compare_faces(data_emb, emb):


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

def update_model_face(recognizer,WIDTHDIVIDER = 4):


   
    path = "dataset/"

    embeddings = np.zeros( (1,512) )
    names = []
    unames = []

    for folder in os.listdir(path):
        unames.append(folder)
        faces = []
        for img_name in os.listdir(path + folder + '/'):

            face = cv2.imread(path + folder + '/' + img_name)           
            
            face = scaller_conc(face)
            faces.append(face)

        if(faces):
            for face in faces:
                if(face is not None):
                    embeddings = np.row_stack(( embeddings,recognizer.get_embedding(face)  ))
                    names.append(folder)
                    print('File Coded: ', folder)

            


    #embeddings = np.delete(embeddings , 0, 0)

    print(embeddings.shape)

    with open('database/'+ 'embeddings.pickle', 'wb') as f:
        pickle.dump(embeddings, f)
    with open('database/'+ 'names.pickle', 'wb') as f:
        pickle.dump(names, f)
    with open('database/'+ 'unames.pickle', 'wb') as f:
        pickle.dump(unames, f)
