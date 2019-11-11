import os
import sys

import psycopg2 as dbapi2

LOCAL = False

INIT_STATEMENTS = [
    "CREATE TABLE IF NOT EXISTS DUMMY (NUM INTEGER)",
    "INSERT INTO DUMMY VALUES (50)",

    """CREATE TABLE if not exists public.users (
	username varchar(50) NOT NULL,
	password char(32) NOT NULL,
	email varchar(50) not NULL,
	CONSTRAINT users_pk PRIMARY KEY (username),
    isAdmin bool default false
    )""",

    """CREATE TABLE if not exists public.friends (
        username varchar(50) not null,
        friend varchar(50) not null,
        accepted bool default false not null,
        foreign key (username) references public.users(username)
        on delete cascade
        on update cascade,
        FOREIGN key (friend) references public.users(username)
        on delete cascade
        on update cascade,
        CONSTRAINT friends_pk PRIMARY KEY (username, friend)
    )""",
]


def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            try:
                cursor.execute(statement)
            except Exception as e: print(e) #TODO I know, I know I should not have do this
        cursor.close()


if __name__ == "__main__":
    
    if LOCAL:
        url = connect_str = "dbname='testpython' user='matt' host='localhost' " + \
                  "password='test1234'"
    else:
        url = os.getenv("DATABASE_URL")

    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    initialize(url)
