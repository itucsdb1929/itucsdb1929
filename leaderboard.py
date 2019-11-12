from flask import Flask, render_template, request, redirect, url_for, session, Blueprint, flash
import db

leaderboard = Blueprint('leaderboard', __name__,
                        template_folder='templates')

@leaderboard.route("/leaderboard")
def leaderboardFunction():
    with db.dataBaseLock:
        cursor = db.get_cursor()
        connection = db.get_connection()
        cursor.execute("""select username, email from users""")
        lst = cursor.fetchall()
        usr = session['username']
        cursor.execute("""select friend from friends
                            where (username = %s) """, (session['username'],))
        tmp = cursor.fetchall()
        friends = []
        requested = []
        for it in tmp:
            friends.append(it[0])
        cursor.execute("""select friend from friendrequests
                            where (sender = %s) """, (session['username'],))

        friendRequests = cursor.fetchall()
        for it in friendRequests:
            requested.append(it[0])
        return render_template('leaderboard.html', lst=lst, len = len(lst),
                                usr = usr, friends=friends, requested=requested)
