
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
        foreign key (username) references public.users(username)
        on delete cascade
        on update cascade,
        FOREIGN key (friend) references public.users(username)
        on delete cascade
        on update cascade,
        CONSTRAINT friends_pk PRIMARY KEY (username, friend)
    )""",

    """CREATE TABLE if not exists public.friendrequests (
        sender varchar(50) not null,
        friend varchar(50) not null,
        foreign key (sender) references public.users(username)
        on delete cascade
        on update cascade,
        FOREIGN key (friend) references public.users(username)
        on delete cascade
        on update cascade,
        CONSTRAINT frequest_pk PRIMARY KEY (sender, friend)
    )""",

    """
    CREATE TABLE if not exists CITY(
    city_major varchar(50) NOT NULL,
    CITY_NAME varchar(50) PRIMARY KEY,
    CITY_LOCATION varchar(50) NOT NULL UNIQUE
    )
    """,
]

def insert_user(cursor,username, password, email):
    cursor.execute("""
    INSERT INTO users VALUES(
    %s,
    %s,
    %s
    )
    """,(username, password, email))


def insert_city(cursor,city_major, city_name, city_location):
    cursor.execute("""
    INSERT INTO CITY VALUES(
    %s,
    %s,
    %s
    )
    """,(city_major, city_name, city_location))


def friend_request(cursor, sender, receiver):
    cursor.execute("""insert into friendrequests
                    (sender, friend) values
                    (%s, %s)""", (sender, receiver))
