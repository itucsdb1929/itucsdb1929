from flask import Flask, render_template, request, redirect, url_for, session, Blueprint, flash
from hashlib import md5
import db

friends = Blueprint('friends', __name__,
                        template_folder='templates')


@friends.route("/friendAdd", methods = ['POST'])
def add():
    if not session.get('logged_in'):
        return redirect(url_for('loginB.login_func'))


    cursor = db.get_cursor()
    connection = db.get_connection()
    username = request.form.get('username')
    print("username", username)
    if len(username) < 5:
        return render_template('logged.html', error='username is too short (min 5 char)')


    cursor.execute("""select password from users
                        where (username = %s) """, (username,))

    passTuple= cursor.fetchone()
    if passTuple == None:
        return render_template('logged.html', error='user not found') 

    try:
        cursor.execute("""insert into friends 
                        (username, friend) values 
                        (%s, %s)""", (session['username'], username))
    except:
        return render_template('logged.html', error='error') 
    finally:
        return render_template('logged.html', error='friend request sent')

    phash = md5(request.form.get('password').encode('utf-8')).hexdigest()

    return redirect(url_for('loginB.logged_func'))


