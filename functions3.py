
LEVEL_EFFECT = 10

def update_city_productions(cursor, cityname, production):
    wood = production["wood"]
    stone = production["stone"]
    food = production["food"]
    metal = production["metal"]
    population = production["population"]
    cursor.execute("""
        UPDATE cityproductions
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
    INSERT INTO buildings (cityname, buildingname, level) values(
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



def level_up_building(cursor, buildingid):
    global LEVEL_EFFECT
    cursor.execute("""
    select * from buildings where(buildingid=%s)
     """,(buildingid, ))
    building = cursor.fetchone()
    city_name = building[1]
    buildingname = building[2]
    level = building[3]
    cursor.execute("""
    select buildtime from buildingtypes where(buildingname=%s)
    """, (buildingname,))

    base_time = cursor.fetchone()
    base_time = base_time[0]

    new_level = int(level)+1
    remaining_time = base_time + (base_time * (new_level)*LEVEL_EFFECT) // 100
    cursor.execute("""
                     INSERT INTO PendingBuildings values(
                     %s,
                     %s,
                     %s
                     )
                     """,(buildingid, new_level, remaining_time))

def updateBuildings(cursor):
    cursor.execute("""Select * from PendingBuildings """)
    tups = cursor.fetchall()
    for i in tups:
        buildingid = i[0]
        level = i[1]
        if(i[2] <= 1):
            cursor.execute("""DElete from PendingBuildings where(buildingid=%s) """,(buildingid,))
            cursor.execute("""update  buildings
                              Set level=level+1
                              where(buildingid=%s)""",(buildingid,))
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
