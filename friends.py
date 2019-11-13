from flask import Flask, render_template, request, redirect, url_for, session, Blueprint, flash
from hashlib import md5
import db
from statements import friend_request, insert_friend
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
        cursor.execute("""select username,friend from friends where(username=%s and friend=%s)""",
                        (session['username'], username))
        is_friend = cursor.fetchone()
        if is_friend is not None:
            return render_template('logged.html', error='Already friend')

        try:
            friend_request(cursor, session['username'], username)
        except:
            return render_template('logged.html', error='error')
        finally:
            connection.commit()
            return redirect(url_for('leaderboard.leaderboardFunction'))
            #return render_template('logged.html', error='friend request sent')


@friends.route("/friendAccept", methods = ['POST'])
def accept():
    with db.dataBaseLock:
        cursor = db.get_cursor()
        connection = db.get_connection()
        username = request.form.get('username')
        print("accept ", username)
        cursor.execute("""select count(*) from public.friendrequests
            WHERE sender=%s AND friend=%s""", (session['username'], username))

        if(cursor.fetchone() == None):
            return render_template('logged.html', error="error") #no such request

        cursor.execute("""
        select username from friends where(username=%s and friend=%s)
         """,(session['username'],username))
        if(cursor.fetchone() == None):
            if username:
                insert_friend(cursor, session['username'], username)
        else:
            cursor.execute("""DELETE FROM public.friendrequests
                    WHERE sender=%s AND friend=%s""",(username, session['username']))
        connection.commit()

        return redirect(url_for('profile.profileFuncMe'))
