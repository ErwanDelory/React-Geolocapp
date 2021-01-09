# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 15:39:28 2020

@author: Boutaina et Théo
"""

from elasticsearch import Elasticsearch
from cassandra.cqlengine import connection


connection.setup(['172.16.1.50'], "cassandra", protocol_version=3)
ES = Elasticsearch(['172.16.1.50'],port=9200)

def list_to_str(list_geonameid):
    """[summary]

    Args:
        list_geonameid ([type]): [description]

    Returns:
        [type]: [description]
    """
    separator=','
    str_geonameid=separator.join(map(str,list_geonameid))
    return str_geonameid

def search_geoname_with_admin(value_search,admin_code):
    """[summary]

    Args:
        value_searc ([type]): [description]
        admin_code  ([type]): [description]

    Returns:
        [type]: [description]
    """
    #il est possible que les admin_code soit set à None,
    #cette fonction permet de retrouver un admin_code différent de None
    count=0
    flag=False
    hit=None

    while flag is False and count < len(value_search):

        if value_search[count]["_source"][admin_code] is None:
            count=count+1
        else:
            hit=value_search[count]
            flag=True

    if flag is False:
        return -1
    return hit


def search_data_by_coords(index,latitude,longitude,admin_code,pas):
    """[summary]

    Args:
        index ([type]): [description]
        latitude ([type]): [description]
        longitude ([type]): [description]
        admin_code ([type]): [description]
        pas ([type]): [description]

    Returns:
        [type]: [description]
    """
    #pas: marge d'erreurs lors de la saisie des coordonnées
    res = ES.search(index=index, body={"query":{
    #recherche de la ville recherchée (latitude/longitude)
    "bool": {
        "must": [
            { "range": { "latitude": {"lt":latitude+pas} }},
            { "range": { "latitude": {"gte":latitude-pas} }},
            { "range": { "longitude": {"lt":longitude+pas} }},
            { "range": { "longitude": {"gte":longitude-pas} }}
        ]
        }}})
    if len(res["hits"]["hits"])==0:
        return -1,"Pas de villes ayant ses coordonnées"
    hit=search_geoname_with_admin(res["hits"]["hits"],"admin4_code")
    if hit == -1:
        return -1,"L'admin code n'est pas donnée"

    list_geoname,hierarchy=search_data_cassandra(hit,admin_code)

    return list_geoname,hierarchy
    #list_geoname: listes des geonames autour de la cible selon la zone/
    #hierarchy: ville (parfois si la cible est un hotel par ex), département,
    #région, pays et région de la cible


def search_data_by_name(index,name,admin_code):
    """[summary]

    Args:
        index ([type]): [description]
        name ([type]): [description]
        admin_code ([type]): [description]

    Returns:
        [type]: [description]
    """
    res = ES.search(index=index, body={"query":{ #recherche de la ville recherchée
    "bool": {
        "should": [
            { "match": { "asciiname": name }},
        ]
        }}})

    if len(res["hits"]["hits"])==0:
        return -1,"Pas de villes ayant ses coordonnées"
    hit=search_geoname_with_admin(res["hits"]["hits"],"admin4_code")
    if hit == -1:
        return -1,"L'admin code n'est pas donnée"

    list_geoname,hierarchy=search_data_cassandra(hit,admin_code)

    return list_geoname, hierarchy
    #list_geoname: listes des geonames autour de la cible selon la zone/
    #hierarchy: ville (parfois si la cible est un hotel par ex), département,
    #région, pays et région de la cible


def search_data_cassandra(hit,admin_code):
    """[summary]

    Args:
        hit ([type]): [description]
        admin_code ([type]): [description]

    Returns:
        [type]: [description]
    """
    #recherche des données de la liste des geonameid liée à la cible dans Cassandra

    list_geonameid=search_zone(admin_code,hit,"geonames")
    #recherche des geonames selon la zone indiquée
    list_geonameid_hierarchy=search_zone("admin4_code",hit,"geonames")
    #recuperation des geoname ayant le même CP car tous les geonames
    #ne sont pas associés à la table Hierarchie
    hierarchy=search_data_hierarchy_fr(list_geonameid_hierarchy)

    if list_geonameid==-1:
        return "L'admin_code n'existe pas"

    list_geonameid=list_to_str(list_geonameid)

    list_geoname=[]
    query = 'SELECT * FROM cassandra.geo_name WHERE geonameid IN ('+list_geonameid+')'
    rows = connection.execute(query)

    for row in rows:
        list_geoname.append(row)

    return list_geoname ,hierarchy

def search_zone(admin_code,hit,index):
    """[summary]

    Args:
        admin_code ([type]): [description]
        hit ([type]): [description]
        index ([type]): [description]

    Returns:
        [type]: [description]
    """
    #admin1_code: code pays (mais pas sûr du tout)/admin2_code:région/
    #admin3_code:département(on pense)/admin4:code postal
    list_geonameid=[]
    res=""

    if admin_code=="admin1_code":
        res=hit["_source"]['admin1_code']
    elif admin_code=="admin2_code":
        res=hit["_source"]['admin2_code']
    elif admin_code=="admin3_code":
        res=hit["_source"]['admin3_code']
    else:
        res=hit["_source"]['admin4_code']

    if res is None:
        return -1
    res_admin_code = ES.search(index=index, body={
    "size":1000,
    "query":{
        "bool": {
            "must": [
                { "match": { admin_code:  res}}
            ]
        }}})
    for hit2 in res_admin_code['hits']['hits']:
        #print( hit2["_source"]["geonameid"])
        list_geonameid.append(hit2["_source"]["geonameid"])

    return list_geonameid


def search_data_hierarchy_fr(list_geonameid):
    """[summary]

    Args:
        list_geonameid ([type]): [description]

    Returns:
        [type]: [description]
    """
    bool_h=True
    list_geonameid=list_to_str(list_geonameid)
    hierarchy=[]

    while bool_h is True: #recherche de la hiérarchie
        query = 'SELECT parentId FROM cassandra.hierarchy where childId IN '
        row_parent_id=connection.execute(query+ '('+list_geonameid+') ALLOW FILTERING')
        row_parent_id=row_parent_id.one()
        if row_parent_id is not None:
            row_parent_id=row_parent_id['parentid']
            row_parent_id=str(row_parent_id)
            list_geonameid=row_parent_id
            hierarchy.append(row_parent_id)
        else:
            bool_h=False

    liste_hierarchy = []

    #itération 1 par 1 pour que la hiérarchie soit enregitrée de la plus petite à la plus grande
    for hier in hierarchy:
        rows = connection.execute('SELECT * FROM cassandra.geo_name WHERE geonameid='+hier)
        liste_hierarchy.append(rows.one())

    return liste_hierarchy

#list_geoname, hierarchy=searchDataByCoords("geonames",49.17333,-0.45,"admin4_code",0.001)
#list_geoname,hierarchy=searchDataByName("geonames","Nice","admin4_code")
#print(list_geoname)
#print("------------------------------------------------------------------------------------")
#print(hierarchy)
