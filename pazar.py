def new_trade(cursor, seller, source_type, count, price):
    cursor.execute("""
    INSERT INTO table(seller, source_type,count, price) values(
    %s,
    %s,
    %s
    )
    """,(seller, source_type,count, price))


def buy_something(cursor, trade_id, buyer, source_type, price):
    cursor.execute("""
    SELECT (source_type, price) from tradeTable where trade_id=%s
    """,(trade_id, ))

def get_all_building_types(cursor):#return type = [(buildingname, False)] for all buildings
    cursor.execute("""select buildingname from buildingtypes""")
    build_types = cursor.fetchall()
    lst = []
    for i in build_types:
        buildname = i[0]
        lst.append((buildname, False))
    return lst

#{buildname:{"wood":wood, "stone":stone, "food":food, "metal":metal, "population":population}}
# for all buildnames.
def get_all_building_costs(cursor):
    cursor.execute(""" select (buildingname, wood, stone, food, metal, population) from buildingcosts""")
    build_costs = cursor.fetchall()
    ret_dict = {}
    for i in build_costs:
        buildname = i[0]
        wood = i[1]
        stone = i[2]
        food = i[3]
        metal = i[4]
        population = i[5]
        dct = {"wood":wood, "stone":stone, "food":food, "metal":metal, "population":population}
        ret_dict[buildname] = dct
    return ret_dict

def get_user_building_build(cursor, username):
    init = get_all_building_types(cursor)
    build_costs = get_all_building_costs(cursor)
    cursor.execute("""
    select (cityname,buildinglimit, buildingcount) from cities where username=%s
    """,(username, ))
    cities = cursor.fetchall()
    ret_dict = {}
    for i in cities:
        city_name = i[0]
        buildinglimit = i[1]
        buildingcount = i[2]
        if(int(i[1]) <= int(i[2])):
            ret_dict[city_name] = init
            continue
        city_list = []
        city_sources = get_sources_of_city(cursor, city_name)
        for buildname in build_costs:
            is_buildable = True
            for source in build_costs[buildname]:
                if(city_sources[source] < build_costs[source]):
                    city_list.append((buildname, False))
                    is_buildable = False
                    break
            if is_buildable:
                city_list.append((buildname, True))
        ret_dict[city_name] = city_list
    print(ret_dict)
    return ret_dict



def get_building_costs(cursor, buildingname):
    cursor.execute(""" select (wood, stone, food, metal, population) from buildingcosts
    where(buildingname =%s) """,(buildingname))
    costs = cursor.fetcone()
    ret_dict = {"wood":costs[0], "stone":costs[1], "food": costs[2], "metal": costs[3]:"population":costs[4]}
    return ret_dict
def build_building_in_city_api(cursor, cityname, buildingname):
    new_building(cursor, cityname, buildingname)
    costs = get_building_costs(cursor, buildingname)
    cursor.execute(""" Update citysources
                        set wood = wood -%s,
                            stone = stone -%s,
                            food = food -%s,
                            metal = metal -%s,
                            population = population -%s
                            where (cityname=%s)""",(costs["wood"],costs["stone"],costs["food"],
                            costs["metal"],costs["population"],cityname))
