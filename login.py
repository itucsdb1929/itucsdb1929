from flask import Flask, render_template, request, redirect, url_for, session, Blueprint
from hashlib import md5
import db
loginB = Blueprint('loginB', __name__,
                        template_folder='templates')

@loginB.route("/logged", methods = ['GET'])
def logged_func():
    if not session.get('logged_in'):
        return redirect(url_for('loginB.login_func'))
    return render_template('logged.html', username = session['username'], password = session['password'])

@loginB.route("/login", methods = ['GET', 'POST'])
def login_func():
    if session.get('logged_in'):
        return redirect(url_for('loginB.logged_func'))

    if request.method == 'POST':
        username = request.form.get('username')
        phash = md5(request.form.get('password').encode('utf-8')).hexdigest()
        cursor = db.get_cursor()
        cursor.execute("""select password from users
                            where (username = %s or email = %s)""", (username, username))
        passTuple= cursor.fetchone()
        if passTuple == None:
            return redirect(url_for('loginB.login_func')) #TODO username wrong
        passwdHash = passTuple[0]
        print("paswd = ", passwdHash)
        print("entered = ", phash)
        if passwdHash != phash:
            return redirect(url_for('loginB.login_func')) #TODO password wrong
        
        session['username'] = request.form.get('username')
        session['password'] = phash
        session['logged_in'] = True
        return redirect(url_for('loginB.logged_func'))

    return render_template('login_form.html')


@loginB.route("/logout", methods = ['GET'])
def logout_func():
    session['logged_in'] = False
    return redirect(url_for('loginB.login_func'))
