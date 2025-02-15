import os
import sys
from statements import INIT_STATEMENTS_ORDER, insert_user
from statements import NEW_STATEMENTS
import psycopg2 as dbapi2

from data import dataCreaterAndUpdater

LOCAL = False



def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS_ORDER:
            try:
                print("statement", statement)
                cursor.execute(NEW_STATEMENTS[statement])
            except Exception as e: print(e) #TODO I know, I know I should not have do this

        dataCreaterAndUpdater(cursor)
        insert_user(cursor, "admin", "0192023a7bbd73250516f069df18b500", "admin@admin")

        cursor.close()
        connection.commit()


if __name__ == "__main__":

    if LOCAL:
        url = connect_str = "dbname='testpython' user='test' host='localhost' " + \
                  "password='test1234'"
    else:
        url = os.getenv("DATABASE_URL")

    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    initialize(url)
