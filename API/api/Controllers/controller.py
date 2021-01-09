"""
Api Entry points
"""
from flask import Blueprint, jsonify, request
from Function.recherche_es import search_data_by_coords, search_data_by_name

controller = Blueprint("controller", __name__)

@controller.route("/find", methods=['POST'])
def req_1():
    """Entry point : find by coord and code"""

    codestr = "admin"+ str(request.json["code"]) +"_code"
    lat = float(request.json["lat"])
    lon = float(request.json["lon"])

    list_geoname, hierarchy=search_data_by_coords("geonames",lat,lon,codestr,0.001)
    if list_geoname == -1:
        return {"msg": hierarchy}
    listgeoname = []
    i = 0
    for item in list_geoname:
        if item is not None:
            i = i+1
            data = {
            "name": str(item["asciiname"]),
            "lat" : str(item["latitude"]),
            "lon" : str(item["longitude"]),
            "pop" : str(item["population"]),
            }
            listgeoname.append(data)
        if i == 10:
            break

    listhierarchy = []
    i = 0
    for item in hierarchy:
        if item is not None:
            i=i+1
            data = {
            "name": str(item["asciiname"]),
            "pop" : str(item["population"]),
            "lat" : str(item["latitude"]),
            "lon" : str(item["longitude"]),
            }
            listhierarchy.append(data)
        if i == 10:
            break


    return jsonify({"lieu":listgeoname, "hierarchy": listhierarchy})


@controller.route("/find/<string:name>/<int:code>", methods=['GET'])
def req_2(name,code):
    """ Entry point : find by name and code """

    codestr = "admin"+ str(code) +"_code"
    list_geoname, hierarchy=search_data_by_name("geonames",name,codestr)
    if list_geoname == -1:
        return {"msg": hierarchy}
    listgeoname = []
    i = 0
    for item in list_geoname:
        if item is not None:
            i = i+1
            data = {
            "name": str(item["asciiname"]),
            "lat" : str(item["latitude"]),
            "lon" : str(item["longitude"]),
            "pop" : str(item["population"]),
            }
            listgeoname.append(data)
        if i == 10:
            break

    listhierarchy = []
    i = 0
    for item in hierarchy:
        if item is not None:
            i=i+1
            data = {
            "name": str(item["asciiname"]),
            "pop" : str(item["population"]),
            "lat" : str(item["latitude"]),
            "lon" : str(item["longitude"]),
            }
            listhierarchy.append(data)
        if i == 10:
            break


    return jsonify({"lieu":listgeoname, "hierarchy": listhierarchy})
