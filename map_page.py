from flask import Flask, render_template, request, redirect, url_for, session, Blueprint, flash
import db

map_page = Blueprint('map_page', __name__,
                        template_folder='templates')

@map_page.route("/map", methods = ['GET'])
def map_func():
    cursor = db.get_cursor()
    connection = db.get_connection()
    # ('cityname', 'citylevel', username')
    cities = [ [ ('empty', -1, -1, -1) for i in range(0, 12) ] for j in range(0, 12) ]
    cursor.execute("""SELECT xcoordinate, ycoordinate, cityname, username FROM public.cities""")
    x = cursor.fetchall()
    for i in x:
        cities[i[0]][i[1]] = (i[2], 1, i[3])
    return render_template('map_page.html', cities=cities)