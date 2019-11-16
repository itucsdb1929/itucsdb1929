from flask import Flask, render_template, request, redirect, url_for, session, Blueprint, flash

import db
from statements import your_message

new_message = Blueprint('new_message', __name__,
                        template_folder='templates')

@new_message.route("/new_message", methods=['POST'])
def message():
    sender = session['username']
    receiver = request.form.get('receiver')
    _message = request.form.get('message')
    with db.dataBaseLock:
        cursor = db.get_cursor()
        connection = db.get_connection()
        your_message(cursor, sender, receiver, _message)
        connection.commit()
        return redirect(session['url'])
