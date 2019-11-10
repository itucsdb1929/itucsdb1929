from flask import Flask, render_template, request, redirect, url_for, session
from tables import tables
from home import home
import os
import sys

import psycopg2 as dbapi2


app = Flask(__name__)
app.register_blueprint(tables)
app.register_blueprint(home)

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



@app.route("/logged", methods = ['GET'])
def logged():
    return render_template('logged.html', username = session['username'], password = session['password'])

@app.route("/login", methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form.get('username')
        session['password'] = request.form.get('password')
        return redirect(url_for('logged'))
    return render_template('login_form.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
