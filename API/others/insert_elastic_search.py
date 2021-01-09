# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 22:29:18 2020

@author: Théo
"""


import uuid
from elasticsearch import Elasticsearch
from cassandra.cqlengine import columns
from cassandra.cqlengine import connection
from datetime import datetime
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine.models import Model
from cassandra.cluster import Cluster
    
def insert_Geoname_ES(index):

    connection.setup(['172.16.1.50'], "cassandra", protocol_version=3)
    rows = connection.execute('SELECT geonameid,longitude,latitude,asciiname,admin1_code,admin2_code,admin3_code,admin4_code FROM cassandra.geo_name')
    
    es = Elasticsearch(['172.16.1.50'],
        port=9200)
       
    for row in rows:
        
        doc = {
            'geonameid': row['geonameid'],
            'longitude': row['longitude'],
            'latitude': row['latitude'],
            'asciiname': row['asciiname'],
            'admin1_code': row['admin1_code'],
            'admin2_code': row['admin2_code'],
            'admin3_code': row['admin3_code'],
            'admin4_code': row['admin4_code'],
        }
    
        res = es.index(index=index, id=row['geonameid'], body=doc)
        
        print(row)
        
        
insert_Geoname_ES("geonames")
