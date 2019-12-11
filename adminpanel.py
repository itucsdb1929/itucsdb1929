from flask import Flask, render_template, request, redirect, url_for, session, Blueprint, flash

adminpanel = Blueprint('adminpanel', __name__,
                        template_folder='templates')

@adminpanel.route("/adminpanel", methods = ['GET'])
def adminpanel_func():
    return render_template('adminpanel.html')

@adminpanel.route("/adminpanel/addcity", methods=['POST'])
def adminpanel_add_city():
    cityname = request.form.get('cityname')
    username = request.form.get('username')
    xcoordinate = request.form.get('xcoordinate')
    ycoordinate = request.form.get('ycoordinate')
    buildinglimit = request.form.get('buildinglimit')
    buildingcount = request.form.get('buildingcount')

@adminpanel.route("/adminpanel/addbuilding", methods=['POST'])
def adminpanel_add_building():
    pass