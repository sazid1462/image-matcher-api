# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 19:19:58 2017

@author: tamji
"""

from elasticsearch import Elasticsearch

client = Elasticsearch()


request_body = {
	    "settings" : {
	        "number_of_shards": 5,
	        "number_of_replicas": 1
	    },

	    'mappings': {
	        'image': {
	            'properties': {
	                'id': {'index': 'not_analyzed', 'type': 'string'},
	                'name': {'index': 'not_analyzed', 'type': 'string'},
	                'features': {'index': 'not_analyzed', 'type': 'float'}
	            }
             }
          }
	}

client.indices.create(index = 'image-index', body = request_body, ignore=400)

request_body = {
	    "settings" : {
	        "number_of_shards": 5,
	        "number_of_replicas": 1
	    },

	    'mappings': {
	        'image': {
	            'properties': {
	                'id': {'index': 'not_analyzed', 'type': 'string'},
	                'raw': {'index': 'not_analyzed', 'type': 'string'}
	            }
             }
          }
	}

client.indices.create(index = 'raw-image-index', body = request_body, ignore= 400)