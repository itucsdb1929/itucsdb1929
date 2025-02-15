from statements import tupleList2List
from functions4 import get_all_cities, get_buildings_of_city, get_building_limits
import CRUD
def get_all_usernames(cursor):
    cursor.execute("""select username from public.users""")
    x = cursor.fetchall()
    return tupleList2List(x)


def update_all_user_sources(cursor):
    usernames = get_all_usernames(cursor)
    sources = ["wood", "stone", "food", "metal", "population"]
    for user in usernames:
        sdict = {}
        for source in sources:
            cursor.execute("""
            select sum("""+source+""") from citysources join cities on (citysources.cityname=cities.cityname)
            where(cities.username=%s) group by username""",(user,))
            total_source = cursor.fetchone()
            if total_source == None:
                return False
            total_source = total_source[0]
            cursor.execute("""
            Update usersources
            set """+source+ """ = %s
            where(username = %s)
            """, (total_source, user))

            sdict[source] = total_source




def update_all_user_productions(cursor):
    usernames = get_all_usernames(cursor)
    prods = ["wood", "stone", "food", "metal", "population"]
    for user in usernames:
        for prod in prods:
            cursor.execute("""
            select sum("""+prod+""") from cityproductions join cities on (cityproductions.cityname=cities.cityname)
            where(cities.username=%s) group by username""",(user,))
            total_prod = cursor.fetchone()
            if total_prod == None:
                return False
            total_prod = total_prod[0]
            cursor.execute("""
            Update userproductions
            set """+prod+ """ = %s
            where(username = %s)
            """, (total_prod, user))


def get_base_limits_of_city(cursor, cityname):
    cursor.execute("""select wood, stone, metal, food, population from public.citybaselimits
                        where cityname=%s""", (cityname,))
    res = cursor.fetchone()
    lmts = {
        "wood": res[0],
        "stone": res[1],
        "metal": res[2],
        "food": res[3],
        "population": res[4]
    }

    return lmts


def update_all_city_limits(cursor):
    cities = get_all_cities(cursor)
    for city in cities:
        bases = get_base_limits_of_city(cursor, city)
        builds = get_buildings_of_city(cursor, city)
        for buildid in builds:
            buildlims = get_building_limits(cursor, buildid)
            for key in buildlims:
                bases[key] += buildlims[key]
        for key in bases:
            CRUD.update_column(cursor, "citylimits","cityname", city ,key , bases[key])
