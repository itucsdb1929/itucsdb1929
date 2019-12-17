from statements import get_cities_of_user, get_user_of_city
from functions4 import get_city, get_sources_of_city, get_user_gold, get_city_source_limits
from functions4 import get_buildingname, get_building_level, get_buildings_of_city
from functions4 import get_level_up_cost
from functions3 import level_up_building
import db
def get_cities_of_user_api(cursor, username):
    cities = get_cities_of_user(cursor, username)
    apiCities = [ ]
    for cityname in cities:
        gold = get_user_gold(cursor, username)
        city = get_city(cursor, cityname)
        city_sources = get_sources_of_city(cursor, cityname)
        city_source_limits = get_city_source_limits(cursor, cityname)
        buildings = get_buildings_of_city(cursor, cityname)
        apicity = {
            "cityname": city["cityname"],
            "xcoordinate": city["xcoordinate"],
            "ycoordinate": city["ycoordinate"],
            "createdAt": city["createdAt"],
            "food": city_sources["food"],
            "wood": city_sources["wood"],
            "metal": city_sources["metal"],
            "stone": city_sources["stone"],
            "population": city_sources["population"],
            "gold": gold,
            "foodlimit": city_source_limits["food"],
            "woodlimit": city_source_limits["wood"],
            "metallimit": city_source_limits["metal"],
            "stonelimit": city_source_limits["stone"],
            "populationlimit": city_source_limits["population"],      

            "soldiers": 0,
            'buildings': []
        }
        for buildingid in buildings:
            {
            'buildingid': 10,
            'cityname': 'Istanbul',
            'buildingname': 'mill',
            'level': 1,
            'level_up_cost': {
                'food': 100,
                'wood': 50,
                'stone': 50,
                'gold': 50,
                'metal': 50
                },
            'can_level_up': True
            }
            buildingname = get_buildingname(cursor, buildingid)
            level = get_building_level(cursor, buildingid)
            level_up_cost = get_level_up_cost(cursor, buildingid)
            can_level_up = True
            
            for key in level_up_cost:
                if key=="gold":
                    if level_up_cost["gold"] > gold:
                        can_level_up = False

                elif level_up_cost[key] > city_sources[key]:
                    can_level_up = False
            cursor.execute("""select * from pendingbuildings where buildingid=%s""", (buildingid,))
            x = cursor.fetchone()
            if x != None:
                can_level_up = False
            apibuilding = {
                "buildingid": buildingid,
                "cityname": cityname,
                "buildingname": buildingname,
                "level": level,
                "level_up_cost": level_up_cost,  
                "can_level_up": can_level_up,
            }
            apicity["buildings"].append(apibuilding)
        #end building for
        apiCities.append(apicity)
    #end cityname for
    print("apiCities: ", apiCities)
    return apiCities

def get_city_of_building(cursor, buildingid):
    cursor.execute("""select cityname from buildings where buildingid=%s""", (buildingid,))
    city = cursor.fetchone()
    city = city[0]
    return city

def level_up_building_api(cursor, buildingid):

    costs = get_level_up_cost(cursor, buildingid)
    cityname = get_city_of_building(cursor, buildingid)
    username = get_user_of_city(cursor, cityname)
    cursor.execute(""" Update citysources
                        set wood = wood -%s,
                            stone = stone -%s,
                            food = food -%s,
                            metal = metal -%s
                            where (cityname=%s)""",(costs["wood"],costs["stone"],costs["food"],
                            costs["metal"],cityname))
    cursor.execute(""" Update users
                        set gold = gold -%s
                            where (username=%s)""",(costs["gold"],cityname))

    level_up_building(cursor, buildingid)