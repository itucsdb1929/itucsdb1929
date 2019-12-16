from flask import Flask, render_template, request, redirect, url_for, session, Blueprint, flash
from statements import insert_city, insert_user
from functions3 import new_building, level_up_building
from dbinit import initialize
from statements import INIT_STATEMENTS_ORDER, NEW_STATEMENTS, drop_all_tables
import db, os
import data
import CRUD
adminpanel = Blueprint('adminpanel', __name__,
                        template_folder='templates')

@adminpanel.route("/adminpanel", methods = ['GET'])
def adminpanel_func():
    return render_template('adminpanel.html')

@adminpanel.route("/adminpanel/citybaseproductions", methods=['POST'])
def adminpanel_citybaseproductions():
    with db.dataBaseLock:
        cursor = db.get_cursor()
        connection = db.get_connection()
        cityname = request.form.get('cityname')
        wood = request.form.get('wood')         
        stone = request.form.get('stone')
        food = request.form.get('food')
        metal = request.form.get('metal')
        population = request.form.get('population')
        dct = {
            "wood":wood,
            "stone":stone,
            "food":food,
            "metal":metal,
            "population":population,
        }
        for key in dct:
            CRUD.update(cursor, "citybaseproductions", 
                            "cityname", cityname,
                            key, dct[key])
        connection.commit()
    return redirect(url_for('adminpanel.adminpanel_func'))

@adminpanel.route("/adminpanel/citybaselimits", methods=['POST'])
def adminpanel_citybaselimits():
    with db.dataBaseLock:
        cursor = db.get_cursor()
        connection = db.get_connection()
        cityname = request.form.get('cityname')
        wood = request.form.get('wood')
        stone = request.form.get('stone')
        food = request.form.get('food')
        metal = request.form.get('metal')
        population = request.form.get('population')
        dct = {
            "wood":wood,
            "stone":stone,
            "food":food,
            "metal":metal,
            "population":population,
        }
        for key in dct:
            CRUD.update(cursor, "citybaselimits", 
                            "cityname", cityname,
                            key, dct[key])
        connection.commit()
    return redirect(url_for('adminpanel.adminpanel_func'))

@adminpanel.route("/adminpanel/buildingcosts", methods=['POST'])
def adminpanel_buildingcosts():
    with db.dataBaseLock:
        cursor = db.get_cursor()
        connection = db.get_connection()
        buildingname = request.form.get('buildingname')
        wood = request.form.get('wood')
        stone = request.form.get('stone')
        food = request.form.get('food')
        metal = request.form.get('metal')
        gold = request.form.get('gold')
        dct = {
            "wood":wood,
            "stone":stone,
            "food":food,
            "metal":metal,
            "gold":gold,
        }
        for key in dct:
            CRUD.update(cursor, "buildingcosts", 
                            "buildingname", buildingname,
                            key, dct[key])
        connection.commit()
    return redirect(url_for('adminpanel.adminpanel_func'))


@adminpanel.route("/adminpanel/buildinglimiteffects", methods=['POST'])
def adminpanel_buildinglimiteffects():
    with db.dataBaseLock:
        cursor = db.get_cursor()
        connection = db.get_connection()
        buildingname = request.form.get('buildingname')
        wood = request.form.get('wood')
        stone = request.form.get('stone')
        food = request.form.get('food')
        metal = request.form.get('metal')
        population = request.form.get('population')
        dct = {
            "wood":wood,
            "stone":stone,
            "food":food,
            "metal":metal,
            "population":population,
        }
        for key in dct:
            CRUD.update(cursor, "buildinglimiteffects", 
                            "buildingname", buildingname,
                            key, dct[key])
        connection.commit()
    return redirect(url_for('adminpanel.adminpanel_func'))

@adminpanel.route("/adminpanel/buildingincrementeffects", methods=['POST'])
def adminpanel_buildingincrementeffects():
    with db.dataBaseLock:
        cursor = db.get_cursor()
        connection = db.get_connection()
        buildingname = request.form.get('buildingname')
        wood = request.form.get('wood')
        food = request.form.get('food')
        stone = request.form.get('stone')
        metal = request.form.get('metal')
        population = request.form.get('population')
        dct = {
            "wood":wood,
            "stone":stone,
            "food":food,
            "metal":metal,
            "population":population,
        }
        for key in dct:
            CRUD.update(cursor, "buildingincrementeffects", 
                            "buildingname", buildingname,
                            key, dct[key])
        connection.commit()
    return redirect(url_for('adminpanel.adminpanel_func'))

@adminpanel.route("/adminpanel/buildingtypes", methods=['POST'])
def adminpanel_buildingtypes():
    with db.dataBaseLock:
        cursor = db.get_cursor()
        connection = db.get_connection()
        buildingname = request.form.get('buildingname')
        buildtime = request.form.get('buildtime')
        dct = {
            "buildingname":buildingname,
            "buildtime":buildtime,
        }
        for key in dct:
            CRUD.update(cursor, "buildingtypes", 
                            "buildingname", buildingname,
                            key, dct[key])
        connection.commit()
    return redirect(url_for('adminpanel.adminpanel_func'))




@adminpanel.route("/adminpanel/addcity", methods=['POST'])
def adminpanel_add_city():
    with db.dataBaseLock:
        cursor = db.get_cursor()
        connection = db.get_connection()
        cityname = request.form.get('cityname')
        username = request.form.get('username')
        xcoordinate = request.form.get('xcoordinate')
        ycoordinate = request.form.get('ycoordinate')
        buildinglimit = request.form.get('buildinglimit')
        buildingcount = request.form.get('buildingcount')
        insert_city(cursor, cityname, username, xcoordinate, ycoordinate, buildinglimit, buildingcount)
        connection.commit()
    return redirect(url_for('adminpanel.adminpanel_func')) 


@adminpanel.route("/adminpanel/addbuilding", methods=['POST'])
def adminpanel_add_building():
    with db.dataBaseLock:
        cursor = db.get_cursor()
        connection = db.get_connection()
        cityname = request.form.get('cityname')
        buildingname = request.form.get('buildingname')
        new_building(cursor, cityname, buildingname)
        connection.commit()
    return redirect(url_for('adminpanel.adminpanel_func'))

@adminpanel.route("/adminpanel/levelup", methods=['POST'])
def adminpanel_levelup_building():
    with db.dataBaseLock:
        cursor = db.get_cursor()
        connection = db.get_connection()
        buildingid = request.form.get('buildingid')
        level_up_building(cursor, buildingid)
        connection.commit()
    return redirect(url_for('adminpanel.adminpanel_func'))  

@adminpanel.route("/adminpanel/addsql", methods=['POST'])
def adminpanel_insert_sql():
    with db.dataBaseLock:
        cursor = db.get_cursor()
        connection = db.get_connection()
        sqlcommand = request.form.get('sqlstatement')
        print(sqlcommand)
        cursor.execute(sqlcommand)
        connection.commit()
    return redirect(url_for('adminpanel.adminpanel_func'))

@adminpanel.route("/adminpanel/dbinit", methods=['GET'])
def adminpanel_db_init():
    with db.dataBaseLock:
        cursor = db.get_cursor()
        connection = db.get_connection()
        for statement in INIT_STATEMENTS_ORDER:
            print(statement)
            cursor.execute(NEW_STATEMENTS[statement])
        
        data.dataCreaterAndUpdater(cursor)
        insert_user(cursor, "admin", "0192023a7bbd73250516f069df18b500", "admin@admin")
        connection.commit()
    return redirect(url_for('adminpanel.adminpanel_func'))

@adminpanel.route("/adminpanel/dbdelete", methods=['GET'])
def adminpanel_db_delete():
    with db.dataBaseLock:
        cursor = db.get_cursor()
        connection = db.get_connection()
        drop_all_tables(cursor)
        connection.commit()
    return redirect(url_for('adminpanel.adminpanel_func'))