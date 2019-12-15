from flask import Flask, render_template, request, redirect, url_for, session, Blueprint, flash
from statements import insert_city
from dbinit import initialize
from statements import INIT_STATEMENTS_ORDER, NEW_STATEMENTS
import db, os


adminpanel = Blueprint('adminpanel', __name__,
                        template_folder='templates')

@adminpanel.route("/adminpanel", methods = ['GET'])
def adminpanel_func():
    return render_template('adminpanel.html')

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
            cursor.execute(NEW_STATEMENTS[statement])
        connection.commit()
    return redirect(url_for('adminpanel.adminpanel_func'))