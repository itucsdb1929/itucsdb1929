from flask import render_template, Blueprint, session, redirect, url_for
import db
my_cities = Blueprint('city', __name__,
                        template_folder='templates')



@my_cities.route("/my_cities")
def cities_page():
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
        'metallimit': 1000
    }
    cities = []
    cities.append(example_city)
    return render_template("cities.html", cities=cities, citycount=len(cities))
