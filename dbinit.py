import os
import sys

import psycopg2 as dbapi2


INIT_STATEMENTS = [
    "CREATE TABLE IF NOT EXISTS DUMMY (NUM INTEGER)",
    "INSERT INTO DUMMY VALUES (50)",

    """CREATE TABLE IF NOT EXISTS users(
        username varchar (50) primary key not null,
        password char (32) not null,
        email varchar (50) null
    )""",
    """insert into users values ('admin', 'c93ccd78b2076528346216b3b2f701e6')""",
]


def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()


if __name__ == "__main__":
    url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    initialize(url)
