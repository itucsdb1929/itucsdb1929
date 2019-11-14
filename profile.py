from flask import Flask, render_template, request, redirect, url_for, session, Blueprint, flash
import db

profile = Blueprint('profile', __name__,
                        template_folder='templates')

@profile.route("/profile")
def profileFuncMe():
    return redirect(url_for('profile.profileFunc', userName = session['username']))

@profile.route("/profile/<userName>")
def profileFunc(userName):
    session['url'] = url_for('profile.profileFuncMe')
    cursor = db.get_cursor()
    connection = db.get_connection()
    cursor.execute("""select friend from friends
                            where (username = %s) """, (userName,))
    friends = cursor.fetchall()
    cursor.execute("""select sender from friendrequests
                            where (friend = %s) """, (userName,))    
    friendRequests = cursor.fetchall()
    print(friends)
    print(friendRequests)
    me = session['username']
    return render_template('profile.html', 
                        username = userName,
                        friends = friends,
                        friendRequests = friendRequests, viewer = me)