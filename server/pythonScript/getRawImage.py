# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 19:47:45 2017

@author: tamji
"""

from elasticsearch import Elasticsearch
import sys


def getRawImage(rawImageId):
     client = Elasticsearch([{'host': 'es', 'port':9200}])

     searchBody = {
          '_source' : ['raw'],
          'query': {
               'match': {
               'id': rawImageId
               }
          }
     }
     rawImage = client.search(index = 'image-index', doc_type = 'image', body = searchBody)
     xxx =  rawImage['hits']['hits'][0]['_source']['raw']
     print(xxx)


if __name__ == "__main__":

     global rawImageId

     rawImageId = str(sys.argv[1])
     #rawImageId = str('77b77b3142514c71b1ee684c020d51bd')
     getRawImage(rawImageId)
