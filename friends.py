from flask import Flask, render_template, request, redirect, url_for, session, Blueprint, flash
from hashlib import md5
import db

friends = Blueprint('friends', __name__,
                        template_folder='templates')


@friends.route("/friendAdd", methods = ['POST'])
def add():
    if not session.get('logged_in'):
        return redirect(url_for('loginB.login_func'))

    with db.dataBaseLock:
        cursor = db.get_cursor()
        connection = db.get_connection()
        username = request.form.get('username')
        if username == session['username']:
            return render_template('logged.html', error='it is you')
        print("username", username)
        if len(username) < 5:
            return render_template('logged.html', error='username is too short (min 5 char)')


        cursor.execute("""select password from users
                            where (username = %s) """, (username,))

        passTuple= cursor.fetchone()
        if passTuple == None:
            return render_template('logged.html', error='user not found') 

        try:
            cursor.execute("""insert into friendrequests
                            (sender, friend) values 
                            (%s, %s)""", (session['username'], username))
        except:
            return render_template('logged.html', error='error') 
        finally:   
            connection.commit()
            return render_template('logged.html', error='friend request sent')


@friends.route("/friendAdd/", methods = ['GET'])
def accept():
    with db.dataBaseLock:
        cursor = db.get_cursor()
        connection = db.get_connection()
        username = request.args.get('username')
        print("accept ", username)

        cursor.execute("""select count(*) from public.friendrequests
            WHERE sender=%s AND friend=%s""", (session['username'], username))
        
        if(cursor.fetchone() == None):
            return render_template('logged.html', error="error") #no such request


        cursor.execute("""DELETE FROM public.friendrequests
                WHERE sender=%s AND friend=%s""",(username, session['username']))
                
        cursor.execute("""insert into friends 
                (username, friend) values (%s, %s)""", (session['username'], username))
        cursor.execute("""insert into friends
                    (username, friend) values 
                    (%s, %s)""", (username, session['username']))

        connection.commit()

        return redirect(url_for('loginB.logged_func'))
