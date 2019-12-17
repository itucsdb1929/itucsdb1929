from flask import render_template, Blueprint, session, redirect, url_for, jsonify, request
from functions3 import level_up_building

#Write this, check excel.
#from apifuncs import level_up_building_api, build_building_in_city_api

import db
import json
my_cities = Blueprint('city', __name__,
                        template_folder='templates')

@my_cities.route("/api/city/levelupbuilding", methods = ['POST'])
def api_city_levelup():
    with db.dataBaseLock:
        buildingid = request.form.get('building_id')
        cursor = db.get_cursor()
        connection = db.get_connection()
        
        #Write this, check excel.
        #level_up_building_api(buildingid)

        connection.commit()
        return jsonify({'success': True});
    return jsonify({'success': False});


@my_cities.route("/api/city/buildbuilding", methods=['POST'])
def api_city_build():
    with db.dataBaseLock:
        cityname = request.form.get('city_name')
        buildingname = request.form.get('building_name')
        cursor = db.get_cursor()
        connection = db.get_connection()
        print(cityname, buildingname)
        #Write this, check excel
        #build_building_in_city_api(cityname, buildingname)
        connection.commit()
        return jsonify({'success': True});
    return jsonify({'success': False});

@my_cities.route("/my_cities")
def cities_page():
    with db.dataBaseLock:

        username = session['username']

        cursor = db.get_cursor()
        connection = db.get_connection()

        cursor.execute(""" SELECT cityname, xcoordinate, ycoordinate FROM public.cities WHERE (username=%s) """, (username,))
        city_list = cursor.fetchall()
        cities = []
        for i in city_list:
            cities.append(i)
        for i in cities:
            cityname = i[0]
            xcoordinate = i[1]
            ycoordinate = i[2]
            


        example_city = {
            'cityname': 'Istanbul',
            'xcoordinate': 5,
            'ycoordinate': 5,
            'food': 50,
            'wood': 50,
            'stone': 50,
            'gold': 50,
            'metal': 50,
            'soldiers': 0,
            'woodlimit': 1000,
            'foodlimit': 1000,
            'stonelimit': 1000,
            'metallimit': 1000,
            'buildings': [
                {
                'buildingid': 10,
                'cityname': 'Istanbul',
                'buildingname': 'mill',
                'level': 1,
                'level_up_cost': {
                    'food': 100,
                    'wood': 50,
                    'stone': 50,
                    'gold': 50,
                    'metal': 50
                    },
                'can_level_up': True
                }
            ]
        }
        buildingnames = {'Istanbul': [("field", True), ("depository", False), ("mill", True)]}
        cities = []
        cities.append(example_city)
        cities.append(example_city)
        return render_template("cities.html", cities=cities, citycount=len(cities), buildingnames = buildingnames)
