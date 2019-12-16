
LEVEL_EFFECT = 10

def update_city_production(cursor, cityname, production):
    wood = production["wood"]
    stone = production["stone"]
    food = production["food"]
    metal = production["metal"]
    population = production["population"]
    cursor.execute("""
        UPDATE productions
        SET
        wood=%s,
        stone=%s,
        food=%s,
        metal=%s,
        population=%s
        WHERE (cityname=%s)
        """,(wood, stone, food, metal, population, cityname))


def new_building(cursor, cityname, buildingname):
    cursor.execute("""
    INSERT INTO buildings values(cityname, buildingname, level)(
    %s,
    %s,
    %s
    )
    """,(cityname, buildingname, 1))

    cursor.execute("""
    UPDATE cities
    Set buildingcount = buildingcount+1
    where(cityname=%s)
    """, (cityname, ))

    cursor.execute("""select (wood, stone, food, metal,population) from buildinglimiteffects
                      where(buildingname=%s) """,(buildingname,))
    limit_inc_dic = cursor.fetchone()
    lim_wood = limit_inc_dic[0]
    lim_stone = limit_inc_dic[1]
    lim_food = limit_inc_dic[2]
    lim_metal = limit_inc_dic[3]
    lim_population = limit_inc_dic[4]
    cursor.execute("""Update citylimits
                      set
                      wood = wood + %s,
                      stone = stone + %s,
                      food = food + %s,
                      metal = metal + %s,
                      population = population + %s
                      where(cityname=%s)
                    """, (lim_wood, lim_stone, lim_food, lim_metal, lim_population, cityname))

def level_up_building(cursor, buildingid):
    global LEVEL_EFFECT
    cursor.execute("""
    select * from buildings where(buildingid=%s)
     """,(buildingid))
    building = cursor.fetchone()
    city_name = building[1]
    buildingname = building[2]
    level = building[3]
    cursor.execute("""
    select buildtime from buildingtypes where(buildingname=%s)
    """, (buildingname))

    base_time = cursor.fetchone()
    base_time = base_time[0]

    new_level = int(level)+1
    remaining_time = base_time + (base_time * (new_level)*LEVEL_EFFECT) // 100
    cursor.execute("""
                     INSERT INTO PendingBuildings values(
                     %s,
                     %s,
                     %s,
                     %s,
                     %s
                     )
                     """,(buildingid, city_name, buildingname, new_level, remaining_time))

def updateBuildings(cursor):
    cursor.execute("""Select * from PendingBuildings """)
    tups = cursor.fetchall()
    for i in tups:
        buildingid = i[0]
        level = i[1]
        if(i[2] == 0):
            cursor.execute("""DElete from PendingBuildings where(buildingid=%s) """,(buildingid,))
            cursor.execute("""update  buildings
                              Set level=level+1
                              where(buildingid=%s)""",(buildingid))
    cursor.execute("""Update PendingBuildings
                      SET remainingbuildtime = remainingbuildtime-1""")





def update_city_sources(cursor, cityname, sour, limit):
    wood_count = min(sour["wood"], limit["wood"])
    stone_count = min(sour["stone"], limit["stone"])
    food_count = min(sour["food"], limit["food"])
    metal_count = min(sour["metal"], limit["metal"])
    population_count = min(sour["population"], limit["population"])
    cursor.execute("""
                Update CitySources
                SET
                wood=%s,
                stone=%s,
                food=%s,
                metal=%s,
                population=%s
                where(cityname=%s)
                """,(wood_count, stone_count, food_count, metal_count, population_count, cityname))

def update_user_sources(cursor, username, sour):
    wood_count = sour["wood"]
    stone_count = sour["stone"]
    food_count = sour["food"]
    metal_count = sour["metal"]
    population_count = sour["population"]
    cursor.execute("""
    Update UserSources
    SET
    wood=%s,
    stone=%s,
    food=%s,
    metal=%s,
    population=%s
    where(username=%s)
    """,(wood_count, stone_count, food_count, metal_count, population_count, username))
