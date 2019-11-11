from flask import Flask, render_template, request, redirect, url_for, session
from tables import tables
from home import home
from login import loginB
from signup import signup
from friends import friends
import os
import sys

import psycopg2 as dbapi2


app = Flask(__name__)
app.register_blueprint(tables)
app.register_blueprint(home)
app.register_blueprint(loginB)
app.register_blueprint(signup)
app.register_blueprint(friends)
app.secret_key = b'_383#y2L"F4Q8z]/'
# cok gizli

# @app.route("/")
# def home_page():
#     connection, cursor = testFonk()
#     cursor.execute("select * from dummy")
#     a = cursor.fetchall()    
#     returnStr = "deneme<br>"
#     for x in a:
#         for i in x:
#             returnStr += str(i)
#         returnStr +="<br>"
#     connection.close()
#     cursor.close()
#     return returnStr
#     #return render_template('base.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
