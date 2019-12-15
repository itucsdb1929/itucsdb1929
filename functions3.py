
LEVEL_EFFECT = 10



def new_building(cursor, cityname, buildingname):
    cursor.execute("""
    INSERT INTO buildings (cityname, buildingname, level) values (
    %s,
    %s,
    %s
    )
    """,(cityname, buildingname, 1))

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
    select buildtime from buildingtypes where(buildingname=%s)""", (buildingname, ))

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
