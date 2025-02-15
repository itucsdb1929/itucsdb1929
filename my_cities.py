from flask import render_template, Blueprint, session, redirect, url_for, jsonify, request
from functions3 import level_up_building
from statements import get_cities_of_user
from apifuncs import get_cities_of_user_api
from pazar import get_user_building_build, build_building_in_city_api
#Write this, check excel.
from apifuncs import level_up_building_api

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
        print("LEVELUP", buildingid)
        level_up_building_api(cursor, buildingid)

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
        build_building_in_city_api(cursor, cityname, buildingname)

        connection.commit()
        return jsonify({'success': True});
    return jsonify({'success': False});

@my_cities.route("/my_cities")
def cities_page():
    with db.dataBaseLock:
        cursor = db.get_cursor()
        connection = db.get_connection()
        username = session['username']
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
        buildingnames = get_user_building_build(cursor, username)
        cities = get_cities_of_user_api(cursor, username)
        # cities.append(example_city)
    return render_template("cities.html", cities=cities, citycount=len(cities), buildingnames = buildingnames)
