from statements import tupleList2List, get_sources_of_city, get_user_gold
from data import sourcesDict
from pazar import get_building_costs
import CRUD
from functions3 import update_city_sources, update_city_productions
def get_city(cursor, cityname):
    cursor.execute("""select cityname, username, xcoordinate, ycoordinate, buildingLimit, 
    buildingCount, createdAt from public.cities
                        where cityname=%s""", (cityname,))
    city = cursor.fetchone()
   
    cityDict = {
        "cityname": cityname,
        "username": city[1],
        "xcoordinate": city[2],
        "ycoordinate": city[3],
        "buildingLimit": city[4],
        "buildingCount": city[5],
        "createdAt": city[6],
    }
    return cityDict



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

def get_level_up_cost(cursor, buildingid):
    LEVEL_EFFECT = 10 #percent
    level = get_building_level(cursor, buildingid)
    effect = (level + 1) * LEVEL_EFFECT
    buildingname = get_buildingname(cursor, buildingid)
    costs = get_building_costs(cursor, buildingname)
    print("costs", costs)
    for key in costs:
        costs[key] += (costs[key] * effect) // 100

    return costs

def get_buildingname(cursor, buildingid):
    cursor.execute("""select buildingname from public.buildings
                        where buildingid=%s""", (buildingid,))
    (buildingname,) = cursor.fetchone()
    return buildingname

def get_base_building_increment(cursor, buildingname):
    baseincrement = sourcesDict.copy()
    for sourceType in baseincrement:
        baseincrement[sourceType] = CRUD.get_column(cursor, "BuildingIncrementEffects",
                    "buildingname", buildingname,
                    sourceType)
    return baseincrement

def get_base_building_limits(cursor, buildingname):
    baselimits = sourcesDict.copy()
    print("baselimits", baselimits)
    for sourceType in baselimits:
        baselimits[sourceType] = CRUD.get_column(cursor, "BuildingLimitEffects",
                    "buildingname", buildingname, sourceType)
    print("returning limits", baselimits)               
    return baselimits

def get_city_source_limits(cursor, cityname):
    limit = sourcesDict.copy()
    for sourceType in limit:
        limit[sourceType] = CRUD.get_column(cursor, "CityLimits",
                    "cityname", cityname,
                    sourceType)
    return limit

def get_building_productions(cursor, buildingid):
    LEVEL_EFFECT = 10 #percent
    level = get_building_level(cursor, buildingid)
    effect = level * LEVEL_EFFECT
    build_name = get_buildingname(cursor, buildingid)
    productions = get_base_building_increment(cursor, build_name)

    for key in productions:
        productions[key] += (productions[key] * effect) // 100

    return productions

def get_building_limits(cursor, buildingid):
    LEVEL_EFFECT = 10 #percent
    level = get_building_level(cursor, buildingid)
    effect = level * LEVEL_EFFECT
    build_name = get_buildingname(cursor, buildingid)
    limits = get_base_building_limits(cursor, build_name)
    print("limits", limits)
    for key in limits:
        limits[key] += (limits[key] * effect) // 100

    return limits



def update_all_city_productions(cursor):

    all_cities = get_all_cities(cursor)
    for cityname in all_cities:
        baseproductions = sourcesDict.copy()
        for sourceType in baseproductions:
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


def get_productions_of_city(cursor, cityname):

    productions = sourcesDict.copy()
    for sourceType in productions:
        productions[sourceType] = CRUD.get_column(cursor, "CityProductions", "cityname", cityname, sourceType)

    return productions

def update_all_city_sources(cursor):
    cities = get_all_cities(cursor)
    for city in cities:

        productions = get_productions_of_city(cursor, city)

        sources = get_sources_of_city(cursor, city)

        for i in sources:
            sources[i] += productions[i]
        # print("update_all_sources: ", sources)

        limits = get_city_source_limits(cursor, city)
        update_city_sources(cursor, city, sources, limits)
