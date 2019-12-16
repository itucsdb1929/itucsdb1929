from functionsyusuf import 
from statements import tupleList2List
from data import sourcesDict
import CRUD
from functions3 import update_city_sources

def get_all_cities(cursor):
    cursor.execute("""select cityname from public.cities""")
    x = cursor.fetchall()
    return tupleList2List(x)

def get_buildings_of_city(cursor, cityname):
    cursor.execute("""select buildingid from public.buildings
                        where cityname=%s""", (cityname,))
    return tupleList2List(cursor.fetchall())

def get_building_level(cursor, buildingid):
    cursor.execute("""select level from public.buildings
                        where buildingid=%s""", (buildingid,))

    (level,) = cursor.fetchone()
    return level

def get_buildingname(cursor, buildingid):
    cursor.execute("""select buildingname from public.buildings
                        where buildingid=%s""", (buildingid,))
    (buildingname,) = cursor.fetchone()
    return buildingname

def get_base_building_increment(cursor, buildingid):
    buildingname = get_buildingname(cursor, buildingid)
    baseincrement = sourcesDict.copy()
    for sourceType in baseincrement:
        baseincrement[sourceType] = CRUD.get_column(cursor, "BuildingIncrementEffects",
                    "buildingname", buildingname,
                    sourceType)
    return baseincrement

def get_base_building_limit(cursor, buildingid):
    buildingname = get_buildingname(cursor, buildingid)
    baselimits = sourcesDict.copy()
    for sourceType in baselimits:
        baselimits[sourceType] = CRUD.get_column(cursor, "BuildingLimitEffects",
                    "buildingname", buildingname,
                    sourceType)
    return baselimits

def get_city_source_limits(cursor, cityname):
    limit = sourcesDict.copy()
    for sourceType in limit:
        limit[sourceType] = CRUD.get_column(cursor, "CityLimits",
                    "cityname", cityname,
                    sourceType)
    return limit

LEVEL_EFFECT = 10 #percent
def get_building_productions(cursor, buildingid):
    global LEVEL_EFFECT
    level = get_building_level(cursor, buildingid)
    effect = level * LEVEL_EFFECT
    build_name = get_buildingname(cursor, buildingid)
    productions = get_base_building_increment(cursor, build_name)

    for key in productions:
        productions[key] += (productions[key] * effect) // 100

    return productions

LEVEL_EFFECT = 10 #percent
def get_building_limits(cursor, buildingid):
    global LEVEL_EFFECT
    level = get_building_level(cursor, buildingid)
    effect = level * LEVEL_EFFECT
    build_name = get_buildingname(cursor, buildingid)
    limits = get_base_building_limit(cursor, build_name)

    for key in limits:
        limits[key] += (limits[key] * effect) // 100

    return limits



def calculate_production_of_city(cursor, cityname):

    baseproductions = sourcesDict.copy()
    for sourceType in productions:
        baseproductions[sourceType] = CRUD.get_column(cursor, "CityBaseProductions", "cityname", cityname, sourceType)
    
    buildings = get_buildings_of_city(cursor, cityname)

    productions = baseproductions

    for building in buildings:
        prods = get_building_productions(cursor, building)
        for prod in prods:
            productions[prod] += prods[prod]
        #endfor
    #endfor
    update_city_productions(cursor, cityname, productions)
    return productions

def update_all_city_sources(cursor):
    cities = get_all_cities(cursor)
    for city in cities:
        calculate_production_of_city(cursor, cityname)
        # print("update_all_sources: ", sources)


        limits = get_city_source_limits(cursor, username)
        update_city_sources(cursor, username, sources, limits)
    