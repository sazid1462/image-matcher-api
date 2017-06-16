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
import requests
# from sklearn.preprocessing import normalize

def cosine_similarity(ratings):
    sim = ratings.dot(ratings.T)
    if not isinstance(sim, np.ndarray):
        sim = sim.toarray()
    norms = np.array([np.sqrt(np.diagonal(sim))])
    return (sim / norms / norms.T)


imagesize = 300
img_path = 'test_images/Car/image_22.png'
# Should get the image from API
img = kimage.load_img(img_path, target_size=(imagesize, imagesize))

x = kimage.img_to_array(img)
x = np.expand_dims(x, axis=0)
x = preprocess_input(x)

featurePredictor = VGG16(weights='imagenet', include_top=False, pooling = 'max')
featuresReceivedImage = featurePredictor.predict(x)

# TODO :  once the skeletpn is complete come back here and find out if
# changing datatype of features from float to short makes any impact.

receivedImageName = 'image_22.png'
idForReceivedImage = str(uuid.uuid4())
elasticIndex = 'image-index'
doc_type = 'image'

imageModel = {'id': idForReceivedImage, 'name' : receivedImageName,'features' : featuresReceivedImage.tolist()}

esClient = Elasticsearch([{'host': 'localhost', 'port':9200}])

elasticResp = esClient.search(index = elasticIndex, doc_type = doc_type, body = {"_source" : ["id","features"]})
idAndFeatures = [doc for doc in elasticResp['hits']['hits']]

respModel1 = {'id':'BalaMar1', 'similarity':-100}
respModel2 = {'id':'BalaMar2', 'similarity':-100}
respModel3 = {'id':'BalaMar3', 'similarity':-100}
respArray = [respModel1, respModel2, respModel3]

for x in idAndFeatures:
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


# Give Proper API URL
apiURL = ''
result = requests.post(apiURL, data = {'id':[o['id'] for o in respArray]})

esClient.index(index = elasticIndex, doc_type = doc_type, id = idForReceivedImage, body = imageModel)

# Find a proper way of saving actual images into elasticsearch

"""
Make sure your elasticsearch has the following mapping
{
   "image-index": {
      "mappings": {
         "image": {
            "properties": {
               "features": {
                  "type": "float"
               },
               "id": {
                  "type": "text"
               },
               "name": {
                  "type": "text"
               }
            }
         }
      }
   }
}
"""

"""
If don't please run this script on curl or http protocol

PUT image-index
{
    "settings": {
        "index": {
            "number_of_replicas": 1,
            "number_of_shards" : 1
        }
    },
    "mappings" : {
        "image" : {
            "properties" : {
                "id" : { "type" : "string" },
                "name" : { "type": "string"},
                "features" : {"type": "float"}
            }
        }
    }
}
"""