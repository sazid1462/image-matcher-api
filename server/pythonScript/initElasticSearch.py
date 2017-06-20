# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 19:19:58 2017

@author: tamji
"""

from elasticsearch import Elasticsearch

def init_feature_index(host, port):
     client = Elasticsearch([{'host': host, 'port':port}])
     request_body = {
     	    'settings' : {
     	        'number_of_shards': 5,
     	        'number_of_replicas': 2
     	    },

     	    'mappings': {
     	        'feature': {
     	            'properties': {
     	                'id': {'index': 'not_analyzed', 'type': 'string'},
     	                'name': {'index': 'not_analyzed', 'type': 'string'},
     	                'features': {'index': 'not_analyzed', 'type': 'float'}
     	            }
                  }
               }
     	}

     client.indices.create(index = 'feature-index', body = request_body, ignore=400)


def init_image_index(host,port):
     client = Elasticsearch([{'host': host, 'port':port}])
     request_body = {
     	    'settings' : {
     	        'number_of_shards': 5,
     	        'number_of_replicas': 2
     	    },

     	    'mappings': {
     	        'image': {
     	            'properties': {
     	                'id': {'index': 'not_analyzed', 'type': 'string'},
     	                'raw': {'index': 'not_analyzed', 'type': 'binary'}
     	            }
                  }
               }
     	}

     client.indices.create(index = 'image-index', body = request_body, ignore= 400)