from flask import Flask, render_template, request, redirect, url_for, session, Blueprint, flash
import db

leaderboard = Blueprint('leaderboard', __name__,
                        template_folder='templates')

@leaderboard.route("/leaderboard")
def test():
    with db.dataBaseLock:
        cursor = db.get_cursor()
        connection = db.get_connection()
        cursor.execute("""select username, email from users""")
        lst = cursor.fetchall()
        return render_template('leaderboard.html', lst=lst, len = len(lst))