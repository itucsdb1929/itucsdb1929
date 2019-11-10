from flask import Flask, render_template, Blueprint

login = Blueprint('login', __name__,
                        template_folder='templates')


@login.route("/login", methods = ['GET', 'POST'])
def login_page():
    return render_template('login_form.html')