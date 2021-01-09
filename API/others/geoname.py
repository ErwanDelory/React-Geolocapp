import uuid
from cassandra.cqlengine import columns
from cassandra.cqlengine import connection
from datetime import datetime
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine.models import Model
from cassandra.cluster import Cluster


def clean_row(row):
    newrow = dict()

    for key in row.keys():
        if row[key]:
            newrow[key]=row[key]

    return newrow


class GeoName(Model):
    geonameid = columns.Integer(primary_key=True)
    name = columns.Text()
    asciiname = columns.Text()
    alternatenames = columns.Text()
    latitude = columns.Decimal()
    longitude = columns.Decimal()
    feature_class = columns.Text()
    feature_code = columns.Text()
    country_code = columns.Text()
    cc2 = columns.Text()
    admin1_code = columns.Text()
    admin2_code = columns.Text()
    admin3_code = columns.Text()
    admin4_code = columns.Text()
    population = columns.BigInt()
    elevation = columns.Integer()
    dem = columns.Integer()
    timezone = columns.Text()
    modification_date = columns.Date()

connection.setup(['172.16.1.50'], "cassandra", protocol_version=3)

sync_table(GeoName)

import csv

with open('FR.txt') as csvfile:
    reader = csv.DictReader(csvfile, fieldnames=["geonameid","name","asciiname","alternatenames","latitude","longitude","feature_class","feature_code","country_code","cc2","admin1_code","admin2_code","admin3_code","admin4_code","population", "elevation","dem","timezone","modification_date"], delimiter = "\t")
    
    for i in reader:
        row = clean_row(i)
        print(row)
        GeoName.create(**row)