# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 10:17:58 2017

@author: tamjid.ahmed
"""

from keras.applications.vgg16 import VGG16
from keras.preprocessing import image as kimage
from keras.applications.vgg16 import preprocess_input
import numpy as np
import time


def cosine_similarity(ratings):
    sim = ratings.dot(ratings.T)
    if not isinstance(sim, np.ndarray):
        sim = sim.toarray()
    norms = np.array([np.sqrt(np.diagonal(sim))])
    return (sim / norms / norms.T)



st = time.time()
model = VGG16(weights='imagenet', include_top=False, pooling = 'max')
ed = time.time()
print(ed - st)

imagesize = 100

# Index 0
img_path = 'test_images/Food/image_1.png'
img = kimage.load_img(img_path, target_size=(imagesize, imagesize))

x = kimage.img_to_array(img)
x = np.expand_dims(x, axis=0)
x = preprocess_input(x)

features = model.predict(x)
flist1 = features.flatten()
flist1.shape
flist1.ndim

# Index 1
img_path = 'test_images/Food/image_3.png'
img = kimage.load_img(img_path, target_size=(imagesize, imagesize))

x = kimage.img_to_array(img)
x = np.expand_dims(x, axis=0)
x = preprocess_input(x)

features2 = model.predict(x)
flist2 = features2.flatten()

# Index 2
img_path = 'test_images/Car/image_19.png'
img = kimage.load_img(img_path, target_size=(imagesize, imagesize))

x = kimage.img_to_array(img)
x = np.expand_dims(x, axis=0)
x = preprocess_input(x)

features3 = model.predict(x)
flist3 = features3.flatten()

# Index 3
img_path = 'test_images/Car/image_21.png'
img = kimage.load_img(img_path, target_size=(imagesize, imagesize))

x = kimage.img_to_array(img)
x = np.expand_dims(x, axis=0)
x = preprocess_input(x)

features4 = model.predict(x)
flist4 = features4.flatten()

# Index 4
img_path = 'test_images/Food/image_5.png'
img = kimage.load_img(img_path, target_size=(imagesize, imagesize))

x = kimage.img_to_array(img)
x = np.expand_dims(x, axis=0)
x = preprocess_input(x)

features5 = model.predict(x)
flist5 = features5.flatten()

# Index 5
img_path = 'test_images/Food/rotate.png'
img = kimage.load_img(img_path, target_size=(imagesize, imagesize))

x = kimage.img_to_array(img)
x = np.expand_dims(x, axis=0)
x = preprocess_input(x)

features6 = model.predict(x)
flist6 = features6.flatten()

# Index 6
img_path = 'test_images/Car/rotate.png'
img = kimage.load_img(img_path, target_size=(imagesize, imagesize))

x = kimage.img_to_array(img)
x = np.expand_dims(x, axis=0)
x = preprocess_input(x)

features7 = model.predict(x)
flist7 = features7.flatten()

# Index 7
img_path = 'test_images/Car/crop.png'
img = kimage.load_img(img_path, target_size=(imagesize, imagesize))

x = kimage.img_to_array(img)
x = np.expand_dims(x, axis=0)
x = preprocess_input(x)

features8 = model.predict(x)
flist8 = features8.flatten()


combined = np.vstack((flist1, flist2, flist3, flist4, flist5, flist6, flist7,
                      flist8))

combined.shape

sim = cosine_similarity(combined)