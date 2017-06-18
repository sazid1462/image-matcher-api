# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 23:46:27 2017

@author: tamji
"""

from elasticsearch import Elasticsearch
import uuid
from keras.applications.vgg16 import VGG16
from keras.preprocessing import image as kimage
from keras.applications.vgg16 import preprocess_input
import numpy as np
from multiprocessing.pool import ThreadPool
import base64
import os
import sys
# from sklearn.preprocessing import normalize

def cosine_similarity(ratings):
    sim = ratings.dot(ratings.T)
    if not isinstance(sim, np.ndarray):
        sim = sim.toarray()
    norms = np.array([np.sqrt(np.diagonal(sim))])
    return (sim / norms / norms.T)

def get_all_features_from_elastic():
     elasticResp = client.search(index = 'image-index', doc_type = 'image', body = {"_source" : ["id","features"]})
     prevImageIdAndFeatures = [doc for doc in elasticResp['hits']['hits']]
     return prevImageIdAndFeatures

def predict_received_image_features(imgArr):
     featurePredictor = VGG16(weights='imagenet', include_top=False, pooling = 'max')
     featuresReceivedImage = featurePredictor.predict(imgArr)
     return featuresReceivedImage

def persist_raw_image_as_string_in_elastic(imagePath):
     with open(imagePath, "rb") as imageFile:
          rawImage = base64.b64encode(imageFile.read())

     rawImageModel = {'id': idForReceivedImage, 'raw': str(rawImage)}
     elasticResp = client.index(index = 'raw-image-index', doc_type = 'raw-image', id = idForReceivedImage, body = rawImageModel)
     return 'asdad'

def get_3_similar_images(prevImageIdAndFeatures,featuresReceivedImage):
     respModel1 = {'id':'BalaMar1', 'similarity':-100}
     respModel2 = {'id':'BalaMar2', 'similarity':-100}
     respModel3 = {'id':'BalaMar3', 'similarity':-100}
     respArray = [respModel1, respModel2, respModel3]

     for x in prevImageIdAndFeatures:
          curId = x['_source']['id']
          curFeatures = x['_source']['features']
          combined = np.vstack((featuresReceivedImage, curFeatures))
          sim = cosine_similarity(combined)
          for idx in range(3):
               if respArray[idx]['similarity'] < sim[0][1]:
                    for i in range(2, idx, -1):
                         respArray[i]['id'] = respArray[i-1]['id']
                         respArray[i]['similarity'] = respArray[i-1]['similarity']

                    respArray[idx]['id'] = curId
                    respArray[idx]['similarity'] = sim[0][1]
                    break
     return [o['id'] for o in respArray]


"""
GLOBAL SCOPE VARIABLES Start
"""
pool = ThreadPool(processes=5)
client = Elasticsearch([{'host': 'localhost', 'port':9200}])
idForReceivedImage = uuid.uuid4().hex
#img_path = 'F:/ABABAB/test_images/Car/image_22.png'
"""
GLOBAL SCOPE VARIABLES End
"""

def main():

     imagesize = 300
     img = kimage.load_img(img_path, target_size=(imagesize, imagesize))
     imgArr = kimage.img_to_array(img)
     imgArr = np.expand_dims(imgArr, axis=0)
     imgArr = preprocess_input(imgArr)

     receivedImageName = os.path.basename(img_path)

     predict_assync = pool.apply_async(predict_received_image_features, args = (imgArr,))
     index_assync = pool.apply_async(persist_raw_image_as_string_in_elastic, args = (img_path,))
     get_assync = pool.apply_async(get_all_features_from_elastic, args = ())


     prevImageIdAndFeatures = get_assync.get()
     status = index_assync.get()
     featuresReceivedImage = predict_assync.get()

     smililarImageIds = get_3_similar_images(prevImageIdAndFeatures,featuresReceivedImage)
     receivedImageFeatureModel = {'id': idForReceivedImage, 'name' : receivedImageName,'features' : featuresReceivedImage.tolist()}
     client.index(index = 'image-index', doc_type = 'image', id = idForReceivedImage, body = receivedImageFeatureModel)

     for ids in smililarImageIds:
          print(ids)


if __name__ == "__main__":

     global img_path
     img_path = sys.argv[1]
     main()

# TODO elastic exception handling
# TODO get es creds from environment variable
