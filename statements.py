from data import sources, sourcesDict
from functions3 import update_city_productions
from random import randint
import CRUD
NEW_STATEMENTS = {
    "createusersTable" :
        """CREATE TABLE IF NOT EXISTS public.users (
                username varchar(50) NOT NULL,
                userpassword char(32) NOT NULL,
                email varchar(50) NOT NULL,
                profile_image INT default 0,
                gold int NOT NULL DEFAULT 0,
                score int NOT NULL DEFAULT 0,
                CONSTRAINT users_pk PRIMARY KEY (username),
                isAdmin bool default false
        )""",
    "createfriendsTable" :
        """CREATE TABLE IF NOT EXISTS public.friends (
                username varchar(50) NOT NULL,
                friend varchar(50) NOT NULL,
                FOREIGN KEY (username) REFERENCES public.users(username)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE,
                FOREIGN KEY (friend) REFERENCES public.users(username)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE,
                CONSTRAINT friends_pk PRIMARY KEY (username,friend)
        )""",
    "createfriendrequestsTable" :
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
    "createmessagesTable":
        """CREATE TABLE if not EXISTS messages(
          message_id serial primary key,
          sender varchar(50) not null,
          receiver varchar(50) not null,
          message varchar(255),
          has_read boolean,
          FOREIGN KEY (sender) REFERENCES public.users(username)
              ON DELETE CASCADE
              ON UPDATE CASCADE,
          FOREIGN KEY (receiver) REFERENCES public.users(username)
              ON DELETE CASCADE
              ON UPDATE CASCADE
        )""",
    "createsourcetypesTable" :
        """CREATE TABLE IF NOT EXISTS public.sourcetypes (
                stype varchar(50) NOT NULL,
                CONSTRAINT sourcetypes_pk PRIMARY KEY (stype)
        )""",
    "createcitiesTable" :
        """CREATE TABLE IF NOT EXISTS public.cities (
                cityname varchar(50) NOT NULL,
                username varchar(50) NOT NULL,
                xcoordinate bigint NOT NULL,
                ycoordinate bigint NOT NULL,
                buildinglimit bigint NOT NULL,
                buildingcount bigint NOT NULL,
                createdAt varchar(50) NOT NULL,
                CONSTRAINT cities_pk PRIMARY KEY (cityname),
                FOREIGN KEY (username) REFERENCES public.users(username)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
        )""",
    "createcitybaseproductionsTable" :
        """CREATE TABLE IF NOT EXISTS public.citybaseproductions (
                cityname varchar(50) NOT NULL,
                wood bigint NOT NULL,
                stone bigint NOT NULL,
                food bigint NOT NULL,
                metal bigint NOT NULL,
                population bigint NOT NULL,
                CONSTRAINT citybaseproductions_pk PRIMARY KEY (cityname),
                FOREIGN KEY (cityname) REFERENCES public.cities(cityname)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
        )""",
    "createcitybaselimitsTable" :
        """CREATE TABLE IF NOT EXISTS public.citybaselimits (
                cityname varchar(50) NOT NULL,
                wood bigint NOT NULL,
                stone bigint NOT NULL,
                food bigint NOT NULL,
                metal bigint NOT NULL,
                population bigint NOT NULL,
                CONSTRAINT citybaselimits_pk PRIMARY KEY (cityname),
                FOREIGN KEY (cityname) REFERENCES public.cities(cityname)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
        )""",
    "createuserproductionsTable" :
        """CREATE TABLE IF NOT EXISTS public.userproductions (
                username varchar(50) NOT NULL,
                wood bigint NOT NULL,
                stone bigint NOT NULL,
                food bigint NOT NULL,
                metal bigint NOT NULL,
                population bigint NOT NULL,
                CONSTRAINT userproductions_pk PRIMARY KEY (username),
                FOREIGN KEY (username) REFERENCES public.users(username)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
        )""",
    "createcityproductionsTable" :
        """CREATE TABLE IF NOT EXISTS public.cityproductions (
                cityname varchar(50) NOT NULL,
                wood bigint NOT NULL,
                stone bigint NOT NULL,
                food bigint NOT NULL,
                metal bigint NOT NULL,
                population bigint NOT NULL,
                CONSTRAINT cityproductions_pk PRIMARY KEY (cityname),
                FOREIGN KEY (cityname) REFERENCES public.cities(cityname)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
        )""",
    "createcitysourcesTable" :
        """CREATE TABLE IF NOT EXISTS public.citysources (
                cityname varchar(50) NOT NULL,
                wood bigint NOT NULL,
                stone bigint NOT NULL,
                food bigint NOT NULL,
                metal bigint NOT NULL,
                population bigint NOT NULL,
                CONSTRAINT citysources_pk PRIMARY KEY (cityname),
                FOREIGN KEY (cityname) REFERENCES public.cities(cityname)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
        )""",
    "createcitylimitsTable" :
        """CREATE TABLE IF NOT EXISTS public.citylimits (
                cityname varchar(50) NOT NULL,
                wood bigint NOT NULL,
                stone bigint NOT NULL,
                food bigint NOT NULL,
                metal bigint NOT NULL,
                population bigint NOT NULL,
                CONSTRAINT citylimits_pk PRIMARY KEY (cityname),
                FOREIGN KEY (cityname) REFERENCES public.cities(cityname)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
        )""",
    "createusersourcesTable" :
        """CREATE TABLE IF NOT EXISTS public.usersources (
                username varchar(50) NOT NULL,
                wood bigint NOT NULL,
                stone bigint NOT NULL,
                food bigint NOT NULL,
                metal bigint NOT NULL,
                population bigint NOT NULL,
                CONSTRAINT usersources_pk PRIMARY KEY (username),
                FOREIGN KEY (username) REFERENCES public.users(username)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
        )""",
    "createbuildingtypesTable" :
        """CREATE TABLE IF NOT EXISTS public.buildingtypes (
                buildingname varchar(50) NOT NULL,
                buildtime bigint NOT NULL,
                CONSTRAINT buildingtypes_pk PRIMARY KEY (buildingname)
        )""",
    "createbuildingcostsTable" :
        """CREATE TABLE IF NOT EXISTS public.buildingcosts (
                buildingname varchar(50) NOT NULL,
                wood bigint NOT NULL,
                stone bigint NOT NULL,
                food bigint NOT NULL,
                metal bigint NOT NULL,
                gold bigint NOT NULL,
                CONSTRAINT buildingcosts_pk PRIMARY KEY (buildingname),
                FOREIGN KEY (buildingname) REFERENCES public.buildingtypes(buildingname)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
        )""",

    "createbuildinglimiteffectsTable" :
        """CREATE TABLE IF NOT EXISTS public.buildinglimiteffects (
                buildingname varchar(50) NOT NULL,
                wood bigint NOT NULL,
                stone bigint NOT NULL,
                food bigint NOT NULL,
                metal bigint NOT NULL,
                population bigint NOT NULL,
                CONSTRAINT BuildingLimitEffects_pk PRIMARY KEY (buildingname),
                FOREIGN KEY (buildingname) REFERENCES public.buildingtypes(buildingname)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
        )""",

    "createbuildingincrementeffectsTable" :
        """CREATE TABLE IF NOT EXISTS public.buildingincrementeffects (
                buildingname varchar(50) NOT NULL,
                wood bigint NOT NULL,
                stone bigint NOT NULL,
                food bigint NOT NULL,
                metal bigint NOT NULL,
                population bigint NOT NULL,
                CONSTRAINT BuildingIncrementEffects_pk PRIMARY KEY (buildingname),
                FOREIGN KEY (buildingname) REFERENCES public.buildingtypes(buildingname)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
        )""",
    "createbuildingsTable" :
        """CREATE TABLE IF NOT EXISTS public.buildings (
                buildingid serial primary key,
                cityname varchar(50) NOT NULL,
                buildingname varchar(50) NOT NULL,
                level bigint NOT NULL,
                FOREIGN KEY (buildingname) REFERENCES public.buildingtypes(buildingname)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE,
                FOREIGN KEY (cityname) REFERENCES public.cities(cityname)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
        )""",
    "creatependingbuildingsTable" :
        """CREATE TABLE IF NOT EXISTS public.pendingbuildings (
                buildingid int primary key,
                level bigint not null,
                remainingBuildTime bigint not null,
                FOREIGN KEY (buildingid) REFERENCES public.buildings(buildingid)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
        )""",
        "createtradecenterTable":
            """create table if not exists tradecenter(
            trade_id serial primary key,
            seller varchar(80) NOT NULL,
            source_type varchar(80),
            count bigint not null,
            price bigint not null,
            FOREIGN KEY (seller) REFERENCES public.users(username)
                ON DELETE CASCADE
                ON UPDATE CASCADE
            ) """
}

INIT_STATEMENTS_ORDER = [
    "createusersTable",
    "createfriendsTable",
    "createfriendRequestsTable",
    "createmessagesTable",
    "createsourceTypesTable",
    "createcitiesTable",
    "createcitysourcesTable",
    "createusersourcesTable",
    "createcitybaseproductionsTable",
    "createcitybaselimitsTable",
    "createuserproductionsTable",
    "createcityproductionsTable",
    "createcitylimitsTable",
    "createbuildingtypesTable",
    "createbuildinglimiteffectsTable",
    "createbuildingincrementeffectsTable",
    "createbuildingcostsTable",
    "createbuildingsTable",
    "creatependingbuildingsTable",
    "createtradecenterTable",
]

def drop_all_tables(cursor):
    for i in INIT_STATEMENTS_ORDER:
        tablename = i[6:-5]
        cursor.execute("""DROP TABLE IF EXISTS %s CASCADE;""" % tablename)



def insert_user(cursor,username, password, email):
    cursor.execute("""
    INSERT INTO users VALUES(
    %s,
    %s,
    %s,
    0,
    0,
    0
    )
    """,(username, password, email))

    CRUD.initializer(cursor, "userproductions", username)
    CRUD.initializer(cursor, "usersources", username)



def insert_city(cursor, city_name, user_name, xcoordinate, ycoordinate, buildinglimit, buildingcount):
    cursor.execute("""
    INSERT INTO cities VALUES(
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s
    )
    """,(city_name, user_name, xcoordinate, ycoordinate, buildinglimit, buildingcount, "0"))

    set_base_productions_of_city(cursor, city_name)
    set_base_limits_of_city(cursor, city_name)
    CRUD.initializer(cursor, "CityProductions", city_name)
    CRUD.initializer(cursor, "CitySources", city_name)
    CRUD.initializer(cursor, "CityLimits", city_name)



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


def your_message(cursor, sender, receiver, message):
    cursor.execute("""INSERT INTO Messages (message_id, sender, receiver, message, has_read) VALUES (DEFAULT, %s, %s, %s, %s);""",(sender, receiver, message, 'FALSE'))

def delete_message(cursor, val):
    cursor.execute("""DELETE FROM Messages WHERE (message_id=%s)""", (val, ))

def delete_friend(cursor, username, friend):
    cursor.execute("""select username,friend from friends where(username=%s and friend=%s)""",(username, friend))
    if cursor.fetchone() is None:
        return False
    cursor.execute("""delete from friends where (username=%s and friend=%s)""",(username, friend))
    cursor.execute(""" delete from friends where(username=%s and friend=%s)""",(friend, username))
    return True


def accept_friend(cursor, sender, friend): # sender = session['username'], friend = username
    cursor.execute("""select count(*) from public.friendrequests
                    WHERE sender=%s AND friend=%s""", (sender, friend))
    if cursor.fetchone() is None:
        return 0 #return render_template('logged.html', error="error") #no such request
    cursor.execute("""
                    select username from friends where(username=%s and friend=%s)
                    """,(sender,friend))
    if cursor.fetchone() is None:
         return 1 #They are not friends before
    else:
        cursor.execute("""DELETE FROM public.friendrequests
                    WHERE sender=%s AND friend=%s""",(friend, sender))
        return 2


def reject_friend(cursor, sender, friend):
    cursor.execute("""
    DELETE FROM public.friendrequests WHERE sender=%s AND friend=%s
    """,(friend, sender))


#def new_building(cursor, buildingName):
#yeni bina building tablesine 0 olarak eklenecek
#pending building tablesina level 1 olarak eklenecek
#bina masraflari dusulecek kullanicidan

#def levelup_building(cursor, buildingis):
#buildings tablesinde leveli x olan bina pending building tablesine x+1 olarak eklenecek
#bina yukselme masraflari kullanicidan dusulecek

def tupleList2List(tupleList):
    normalList = []
    for (i,) in tupleList:
        normalList.append(i)
    return normalList


def get_all_cities(cursor):
    cursor.execute("""select cityname from public.cities""")
    x = cursor.fetchall()
    return tupleList2List(x)

def get_cities_of_user(cursor, username):
    cursor.execute("""select cityname from public.cities
                        where username=%s""", (username,))
    x = cursor.fetchall()
    return tupleList2List(x)

def get_user_source_limits(cursor, username):
    cursor.execute("""select stype,value from public.limits
                        where username=%s""", (username,))

    limitsUser = cursor.fetchall()
    # print("limit user", limitsUser)

    limitsDict = sourcesDict.copy()

    for (stype, value) in limitsUser:
        limitsDict[stype] += value

    # print("limit return", limitsDict)
    return limitsDict




def update_all_sources(cursor):
    cities = get_all_cities(cursor)
    for city in cities:
        city_production = get_production_of_city(cursor, city)
        username = get_user_of_city(cursor, city)
        sources = get_sources_of_user(cursor, username)
        # print("update_all_sources: ", sources)


        for key in city_production:
            sources[key] +=city_production[key]

        limits = get_user_source_limits(cursor, username)

        update_user_sources(cursor, username, sources, limits)


def get_sources_of_user(cursor, username):
    cursor.execute("""select stype,value from public.sources
                        where username=%s""", (username,))

    sourcesUser = cursor.fetchall()
    sourcesD = sourcesDict.copy()



    for (stype, value) in sourcesUser:
        sourcesD[stype] += value

    return sourcesD


#return building ids


def get_base_productions_of_city(cursor, city):
    cursor.execute("""select stype, value from public.citybaseproductions
                        where cityname=%s""", (cityname,))
    baseproductions = cursor.fetchall()
    baseproductionsDict = { }

    for (stype, value) in productions:
        baseproductionsDict[stype] = value

    return baseproductionsDict

def set_base_productions_of_city(cursor, cityname):
        cursor.execute("""
    INSERT INTO citybaseproductions (cityname, wood, stone, metal, food, population) VALUES(
    %s,
    %s,
    %s,
    %s,
    %s,
    %s
    )
    """,(cityname, randint(50, 100), randint(50, 100), randint(50, 100), randint(50, 100) ,randint(50, 100)))

def get_base_building_productions(cursor, buildingname):
    cursor.execute("""select stype, value from public.BuildingEffects
                        where buildingname=%s and etype='inc'""", (buildingname,))
    baseproductions = cursor.fetchall()
    baseproductionsDict = sourcesDict.copy()

    for (stype, value) in baseproductions:
        baseproductionsDict[stype] = value

    return baseproductionsDict




def set_base_limits_of_city(cursor, username):
    cursor.execute("""
    INSERT INTO citybaselimits VALUES(
    %s,
    %s,
    %s,
    %s,
    %s,
    %s
    )
    """,(username, randint(1000, 1500), randint(1000, 1500), randint(1000, 1500), randint(1000, 1500) ,randint(1000, 1500)))

def change_city_major(cursor, username, cityname):
    cursor.execute("""
    UPDATE public.cities
    SET  username=%s
    WHERE(cityname=%s)
    """, (username, cityname))


def get_user_of_city(cursor, cityname):
    cursor.execute("""
    SELECT username FROM public.cities WHERE(cityname=%s)
    """, (cityname,))
    user = cursor.fetchone()
    return user[0]


def update_user_sources(cursor, username, sour, limit):
    # print("update_user_sources scr", sour)
    # print("update_user_sources lmt", limit)
    for key in sour:
        value = min(limit[key], sour[key])

        cursor.execute("""
        UPDATE sources
        SET value=%s
        WHERE (username=%s and stype=%s)
        """,(value, username, key))
