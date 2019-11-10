import psycopg2 as dbapi2
import os
import sys


# def connectDb():
#     url = os.getenv("DATABASE_URL")
#     if url is None:
#        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
#        sys.exit(1)

#     return initialize(url)


_connection = None

def get_connection():
    url = os.getenv("DATABASE_URL")
    global _connection
    if not _connection:
        _connection = dbapi2.connect(url)
    return _connection

def get_cursor():
    return get_connection().cursor()