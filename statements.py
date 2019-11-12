NEW_STATEMENTS = {
    "createUserTable" : 
        """CREATE TABLE IF NOT EXISTS public.users (
                username varchar(50) NOT NULL,
                userpassword char(32) NOT NULL,
                email varchar(50) NOT NULL,
                gold int NOT NULL DEFAULT 0,
                score int NOT NULL DEFAULT 0,
                CONSTRAINT users_pk PRIMARY KEY (username)
        )""",
    "createFriendsTable" : 
        """CREATE TABLE IF NOT EXISTS public.friends (
                username varchar(50) NOT NULL,
                friend varchar(50) NOT NULL,
                CONSTRAINT friends_pk PRIMARY KEY (username,friend),
                FOREIGN KEY (username) REFERENCES public.users(username) 
                    ON DELETE CASCADE 
                    ON UPDATE CASCADE,
                FOREIGN KEY (friend) REFERENCES public.users(username) 
                    ON DELETE CASCADE 
                    ON UPDATE CASCADE
        )""",
    "createFriendRequestsTable" : 
        """CREATE TABLE IF NOT EXISTS public.friendrequests (
                sender varchar(50) NOT NULL,
                friend varchar(50) NOT NULL,
                CONSTRAINT friendrequests_pk PRIMARY KEY (sender,friend),
                FOREIGN KEY (sender) REFERENCES public.users(username) 
                    ON DELETE CASCADE 
                    ON UPDATE CASCADE,
                FOREIGN KEY (friend) REFERENCES public.users(username) 
                    ON DELETE CASCADE 
                    ON UPDATE CASCADE
        )""",
    "createSourceTypesTable" : 
        """CREATE TABLE IF NOT EXISTS public.sourcetypes (
                stype varchar(50) NOT NULL,
                CONSTRAINT sourcetypes_pk PRIMARY KEY (stype)
        )""",
    "createCitiesTable" : 
        """CREATE TABLE IF NOT EXISTS public.cities (
                cityname varchar(50) NOT NULL,
                username varchar(50) NOT NULL,
                xcoordiante bigint NOT NULL,
                ycoordiante bigint NOT NULL,
                buildinglimit bigint NOT NULL,
                buildingcount bigint NOT NULL,
                CONSTRAINT cities_pk PRIMARY KEY (cityname),
                FOREIGN KEY (username) REFERENCES public.users(username) 
                    ON DELETE CASCADE 
                    ON UPDATE CASCADE
        )""",
    "createSourcesTable" :
        """CREATE TABLE IF NOT EXISTS public.sources (
                cityname varchar(50) NOT NULL,
                stype varchar(50) NOT NULL,
                count bigint NOT NULL,
                CONSTRAINT sources_pk PRIMARY KEY (cityname,stype),
                FOREIGN KEY (cityname) REFERENCES public.cities(cityname) 
                    ON DELETE CASCADE 
                    ON UPDATE CASCADE,
                FOREIGN KEY (stype) REFERENCES public.sourcetypes(stype) 
                    ON DELETE CASCADE 
                    ON UPDATE CASCADE
        )""",
    "createBaseProductionsTable" :
        """CREATE TABLE IF NOT EXISTS public.baseproductions (
                cityname varchar(50) NOT NULL,
                stype varchar(50) NOT NULL,
                baseproduction bigint NOT NULL,
                CONSTRAINT baseproductions_pk PRIMARY KEY (cityname,stype),
                FOREIGN KEY (cityname) REFERENCES public.cities(cityname) 
                    ON DELETE CASCADE 
                    ON UPDATE CASCADE,
                FOREIGN KEY (stype) REFERENCES public.sourcetypes(stype) 
                    ON DELETE CASCADE 
                    ON UPDATE CASCADE
        )""",
    "createBaseLimitsTable" :
        """CREATE TABLE IF NOT EXISTS public.baselimits (
                cityname varchar(50) NOT NULL,
                stype varchar(50) NOT NULL,
                baselimit bigint NOT NULL,
                CONSTRAINT baselimits_pk PRIMARY KEY (cityname,stype),
                FOREIGN KEY (cityname) REFERENCES public.cities(cityname) 
                    ON DELETE CASCADE 
                    ON UPDATE CASCADE,
                FOREIGN KEY (stype) REFERENCES public.sourcetypes(stype) 
                    ON DELETE CASCADE 
                    ON UPDATE CASCADE
        )""",
    "createProductionsTable" :
        """CREATE TABLE IF NOT EXISTS public.productions (
                cityname varchar(50) NOT NULL,
                stype varchar(50) NOT NULL,
                production bigint NOT NULL,
                CONSTRAINT productions_pk PRIMARY KEY (cityname,stype),
                FOREIGN KEY (cityname) REFERENCES public.cities(cityname) 
                    ON DELETE CASCADE 
                    ON UPDATE CASCADE,
                FOREIGN KEY (stype) REFERENCES public.sourcetypes(stype) 
                    ON DELETE CASCADE 
                    ON UPDATE CASCADE
        )""",
    "createLimitsTable" :
        """CREATE TABLE IF NOT EXISTS public.limits (
                cityname varchar(50) NOT NULL,
                stype varchar(50) NOT NULL,
                sourcelimit bigint NOT NULL,
                CONSTRAINT limits_pk PRIMARY KEY (cityname,stype),
                FOREIGN KEY (cityname) REFERENCES public.cities(cityname) 
                    ON DELETE CASCADE 
                    ON UPDATE CASCADE,
                FOREIGN KEY (stype) REFERENCES public.sourcetypes(stype) 
                    ON DELETE CASCADE 
                    ON UPDATE CASCADE
        )""",
    "createEffectTypesTable" : 
        """CREATE TABLE IF NOT EXISTS public.effecttypes (
                etype varchar(50) NOT NULL,
                CONSTRAINT effecttypes_pk PRIMARY KEY (etype)
        )""",
    "createBuildingTypesTable" : 
        """CREATE TABLE IF NOT EXISTS public.buildingtypes (
                buildingname varchar(50) NOT NULL,
                buildtime bigint NOT NULL,
                CONSTRAINT buildingtypes_pk PRIMARY KEY (buildingname)
        )""",
    "createBuildingEffectsTable" :
        """CREATE TABLE IF NOT EXISTS public.buildingeffects (
                buildingname varchar(50) NOT NULL,
                stype varchar(50) NOT NULL,
                etype varchar(50) NOT NULL,
                value bigint NOT NULL,
                CONSTRAINT buildingeffects_pk PRIMARY KEY (buildingname,stype,etype),
                FOREIGN KEY (buildingname) REFERENCES public.buildingtypes(buildingname) 
                    ON DELETE CASCADE 
                    ON UPDATE CASCADE,
                FOREIGN KEY (stype) REFERENCES public.sourcetypes(stype) 
                    ON DELETE CASCADE 
                    ON UPDATE CASCADE,
                FOREIGN KEY (etype) REFERENCES public.effecttypes(etype) 
                    ON DELETE CASCADE 
                    ON UPDATE CASCADE
        )""",
    "createBuildingCostsTable" :
        """CREATE TABLE IF NOT EXISTS public.buildingcosts (
                buildingname varchar(50) NOT NULL,
                costsource varchar(50) NOT NULL,
                cost bigint NOT NULL,
                CONSTRAINT buildingcosts_pk PRIMARY KEY (buildingname,costsource),
                FOREIGN KEY (buildingname) REFERENCES public.buildingtypes(buildingname) 
                    ON DELETE CASCADE 
                    ON UPDATE CASCADE,
                FOREIGN KEY (costsource) REFERENCES public.sourcetypes(stype) 
                    ON DELETE CASCADE 
                    ON UPDATE CASCADE
        )""",
}

INIT_STATEMENTS_ORDER = [
    "createUserTable",
    "createFriendsTable",
    "createFriendRequestsTable",
    "createSourceTypesTable",
    "createCitiesTable",
    "createSourcesTable",
    "createBaseProductionsTable",
    "createBaseLimitsTable",
    "createProductionsTable",
    "createLimitsTable",
    "createEffectTypesTable",
    "createBuildingTypesTable",
    "createBuildingEffectsTable",
    "createBuildingCostsTable",
]

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


def insert_friend(cursor, user1, user2):
    cursor.execute(
    """DELETE FROM public.friendrequests
            WHERE sender=%s AND friend=%s""",(user2, user1)
    )
    cursor.execute(
    """insert into friends
            (username, friend) values (%s, %s)""", (user1, user2))

    cursor.execute(
    """insert into friends
            (username, friend) values (%s, %s)""", (user2, user1))
        
