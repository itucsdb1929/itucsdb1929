from flask import Flask, render_template

import os
import sys

import psycopg2 as dbapi2


def initialize(url):
    connection =  dbapi2.connect(url)
    cursor = connection.cursor()
    return (connection, cursor)
    


def testFonk():
    url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    return initialize(url)




app = Flask(__name__)


@app.route("/")
def home_page():
    connection, cursor = testFonk()
    cursor.execute("select * from dummy")
    a = cursor.fetchall()    
    returnStr = "deneme<br>"
    for x in a:
        for i in x:
            returnStr += str(i)
        returnStr +="<br>"
    connection.close()
    cursor.close()
    return returnStr
    #return render_template('base.html')

if __name__ == "__main__":
    app.run()
