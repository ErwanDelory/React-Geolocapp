# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 12:06:19 2020

@author: Théo
"""


import uuid
from cassandra.cqlengine import columns
from cassandra.cqlengine import connection
from datetime import datetime
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine.models import Model
from cassandra.cluster import Cluster

def test():
    return True


def clean_row(row):
    newrow = dict()

    for key in row.keys():
        if row[key]:
            newrow[key]=row[key]

    return newrow


class Hierarchy(Model):
    parentId = columns.Integer(primary_key=True)
    childId = columns.Integer(primary_key=True, clustering_order="DESC")
    type = columns.Text()

    

connection.setup(['172.16.1.50'], "cassandra", protocol_version=3)

sync_table(Hierarchy)

import csv

with open('hierarchy.txt') as csvfile:
    reader = csv.DictReader(csvfile, fieldnames=["parentId","childId","type"], delimiter = "\t")
    for i in reader:
        row = clean_row(i)
        print(row)
        Hierarchy.create(**row)