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
import time
from multiprocessing.pool import ThreadPool
import base64
# from sklearn.preprocessing import normalize

st = time.time()

def cosine_similarity(ratings):
    sim = ratings.dot(ratings.T)
    if not isinstance(sim, np.ndarray):
        sim = sim.toarray()
    norms = np.array([np.sqrt(np.diagonal(sim))])
    return (sim / norms / norms.T)

def get_all_features_from_elastic():
     curMethodst = time.time()
     # TODO :  once the skeletpn is complete come back here and find out if
     # changing datatype of features from float to short makes any impact.

     elasticIndex = 'image-index'
     doc_type = 'image'
     elasticResp = client.search(index = elasticIndex, doc_type = doc_type, body = {"_source" : ["id","features"]})
     idAndFeatures = [doc for doc in elasticResp['hits']['hits']]
     print('feature fetch time  '+ repr(time.time() - curMethodst ) )
     return idAndFeatures

def predict_received_image_features(x):
     curMethodst = time.time()
     featurePredictor = VGG16(weights='imagenet', include_top=False, pooling = 'max')
     featuresReceivedImage = featurePredictor.predict(x)
     print('modeling time  '+ repr(time.time() - curMethodst) )
     return featuresReceivedImage

def persist_raw_image_as_string_in_elastic(imagePath):
     curMethodst = time.time()
     with open(imagePath, "rb") as imageFile:
          rawImage = base64.b64encode(imageFile.read())

     elasticIndex = 'raw-image-index'
     doc_type = 'raw-image'
     rawImageModel = {'id': idForReceivedImage, 'raw': str(rawImage)}
     elasticResp = client.index(index = elasticIndex, doc_type = doc_type, id = idForReceivedImage, body = rawImageModel)

     print('Image Persisting time   '+ repr(time.time() - curMethodst ) )
     return 'asdad'

def get_3_similar_images():
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
     return [o['id'] for o in respArray]
 
    
def get_3_similar_images_from_elastic(features):
     curMethodst = time.time()

     elasticIndex = 'image-index'
     doc_type = 'image'
     body = {
       "_source": [
          "id",
          "features"
       ],
       "query": {
          "function_score": {
             "query": {
                "match_all": {}
             },
             "functions": [{
                 "script_score": {
                    "script": {
                        "lang": "groovy",
                        "file": "cosine-similarity",
                        "params": {
                            "left_vector":features,
                            "right_vector":"doc['features']"
                        }
                    }
                 }
             }]
          }
       }
    }
     elasticResp = client.search(index = elasticIndex, doc_type = doc_type, body = body)
     idAndFeatures = [doc for doc in elasticResp['hits']['hits']]
     print('feature fetch time  '+ repr(time.time() - curMethodst ) )
     return idAndFeatures

pool = ThreadPool(processes=5)

imagesize = 300
img_path = 'test_images/image_20.png'
# Should get the image from API
img = kimage.load_img(img_path, target_size=(imagesize, imagesize))

x = kimage.img_to_array(img)
x = np.expand_dims(x, axis=0)
x = preprocess_input(x)


receivedImageName = 'image_20.png'
idForReceivedImage = uuid.uuid4().hex

client = Elasticsearch([{'host': 'localhost', 'port':9200}])

index_assync = pool.apply_async(persist_raw_image_as_string_in_elastic, args = (img_path,))
get_assync = pool.apply_async(get_all_features_from_elastic, args = ())
predict_assync = pool.apply_async(predict_received_image_features, args = (x,))


idAndFeatures = get_assync.get()
featuresReceivedImage = predict_assync.get()
status = index_assync.get()



imageModel = {'id': idForReceivedImage, 'name' : receivedImageName,'features' : featuresReceivedImage.tolist()}


#smililarImageIds = get_3_similar_images()
get_3_similar_async = pool.apply_async(get_3_similar_images_from_elastic, args = (imageModel['features'],))

similarImages = get_3_similar_async.get()

print(similarImages)

# Give Proper API URL
apiURL = 'http://localhost'
#result = requests.post(apiURL, data = {'id':[o['id'] for o in respArray]})

client.index(index = 'image-index', doc_type = 'image', id = idForReceivedImage, body = imageModel)

# Find a proper way of saving actual images into elasticsearch

ed = time.time()

print('Total Time   '+ repr((ed- st)) )

