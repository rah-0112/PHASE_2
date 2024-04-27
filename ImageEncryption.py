import math

import cv2
import matplotlib.pyplot as plt
import numpy as np
# from IPython.display import display, Markdown
# from glob2 import glob

PATH = '../input/full-size-sample-macro-photos/Data'
def OutputFuzzySet(x, f, M, thres):
    x = np.array(x)
    result = f(x, M)
    result[result > thres] = thres
    return result

def AggregateFuzzySets(fuzzy_sets):
    return np.max(np.stack(fuzzy_sets), axis=0)

    # Calculate AggregatedFuzzySet:
    fuzzy_output = AggregateFuzzySets(Inferences)
    
    # Calculate crisp value of centroid
    if get_fuzzy_set:
        return np.average(x, weights=fuzzy_output), fuzzy_output
    return np.average(x, weights=fuzzy_output)

    x = list(range(-50,306))
    FuzzyTransform = dict(zip(x,[Infer(np.array([i]), M) for i in x]))
    
    # Apply the transform to l channel
    u, inv = np.unique(l, return_inverse = True)
    l = np.array([FuzzyTransform[i] for i in u])[inv].reshape(l.shape)
    
    # Min-max scale the output L channel to fit (0, 255):
    Min = np.min(l)
    Max = np.max(l)
    lab[:, :, 0] = (l - Min)/(Max - Min) * 255
    
    # Convert LAB to RGB
    return cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)
    
try:
    # take path of image as a input
    path = r"C:\Users\USER\Desktop\Screenshot 2022-11-05 135808.png"
     
    # taking encryption key as input
    key = 28
     
    # print path of image file and encryption key that
    # we are using
    # print('The path of file : ', path)
    # print('Key for encryption : ', key)
     
    # open file for reading purpose
    fin = open(path, 'rb')
     
    # storing image data in variable "image"
    image = fin.read()
    fin.close()
     
    # converting image into byte array to
    # perform encryption easily on numeric data
    image = bytearray(image)
 
    # performing XOR operation on each value of bytearray
    for index, values in enumerate(image):
        image[index] = values ^ key
 
    # opening file for writing purpose
    fin = open(path, 'wb')
     
    # writing encrypted data in image
    fin.write(image)
    fin.close()
    print('Encryption Done...')
 
     
except Exception:
    print('Error caught : ', Exception.__name__)
