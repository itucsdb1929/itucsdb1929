from flask import Flask, render_template
from tables import tables
from home import home
from login import login
import os
import sys

import psycopg2 as dbapi2


app = Flask(__name__)
app.register_blueprint(tables)
app.register_blueprint(home)
app.register_blueprint(login)

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

@app.route("/login")
def login_page():
    return render_template('login_form.html')


if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 5000)
