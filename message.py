from flask import Flask, render_template, request, redirect, url_for, session, Blueprint, flash

import db
from statements import new_message

message = = Blueprint('message', __name__,
                        template_folder='templates')

@message.route(/new_message, methods=['POST'])
def message():
    sender = session['username']
    receiver = request.form.get('receiver')
    message = request.form.get('message')
    with db.dataBaseLock:
        cursor = db.get_cursor()
        connection = db.get_connection()
        new_message(cursor, sender, receiver, message)
        connection.commit()
        return redirect(session['url'])
