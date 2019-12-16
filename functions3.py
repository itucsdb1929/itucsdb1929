
LEVEL_EFFECT = 10

def update_city_production(cursor, cityname, production):
    for key, values in productions:
        cursor.execute("""
        UPDATE productions
        SET value=%s
        WHERE (cityname=%s and stype=%s)
        """,(value, cityname, key))


def new_building(cursor, cityname, buildingname):
    cursor.execute("""
    INSERT INTO buildings values(cityname, buildingname, level)(
    %s,
    %s,
    %s
    )
    """,(cityname, buildingname, 1))

    cursor.execute("""select * from buildingeffects where(buildingname=%s and etype=limit) """,(buildingname,))
    eff = cursor.fetchall()
    cursor.execute("""Update limits
                      set value = value + %s
                      where(stype=%s)
                    """, (eff[3], eff[1]))

def level_up_building(cursor, buildingid):
    global LEVEL_EFFECT
    cursor.execute("""
    select * from buildings where(buildingid=%s)""",(buildingid,))
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
