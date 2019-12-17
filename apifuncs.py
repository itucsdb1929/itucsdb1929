from statements import get_cities_of_user
from functionsosman import get_city, get_sources_of_city, get_user_gold, get_city_source_limits
from functionsosman import get_buildingname, get_building_level
import db
def get_cities_of_user_api(username):
    with db.dataBaseLock:
        cursor = db.get_cursor()
        connection = db.get_connection()
        cities = get_cities_of_user(cursor, username)
        apiCities = [ ]
        for cityname in cities:
            example_city = {
            'cityname': 'Istanbul',
            'xcoordinate': 5,
            'ycoordinate': 5,
            'food': 50,
            'wood': 50,
            'stone': 50,
            'gold': 50,
            'metal': 50,
            'soldiers': 0,
            'woodlimit': 1000,
            'foodlimit': 1000,
            'stonelimit': 1000,
            'metallimit': 1000,
            'buildings': [
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
            ]
            }
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
                "foodlimit": city_sources_limits["food"],
                "woodlimit": city_sources_limits["wood"],
                "metallimit": city_sources_limits["metal"],
                "stonelimit": city_sources_limits["stone"],
                "populationlimit": city_sources_limits["population"],      

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
                    if key==gold:
                        if level_up_cost[gold] > gold:
                            can_level_up = False

                    elif level_up_cost[key] > city_sources[key]:
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
        connection.commit()
    #end db lock
    return apiCities
