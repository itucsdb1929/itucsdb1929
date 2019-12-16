sources = [
    "wood",
    "stone",
    "food",
    "metal",
    "population",
]


sourcesDict= {
    "wood":0,
    "stone":0,
    "food":0,
    "metal":0,
    "population":0,
}

effects = [
    "limit", #maximum limiliti # kadar artirir
    "inc", #uretimi # kadar arttirir
]

buildings = [   
    {
        "buildingname": "field",
        "buildTime": 20,
        "costs": {
            "wood":20,
            "stone":20,
            "food":0,
            "metal":0,
            "population":0,
            "gold": 0,
        },
        "effects": {
            "inc": {
                "wood":0,
                "stone":0,
                "food":5,
                "metal":0,
                "population":0,
            },
        },
    },
    {
        "buildingname": "depository",
        "buildTime": 66,
        "costs": {
            "wood": 30,
            "stone": 30,
            "food":0,
            "metal": 10,
            "population":0,
            "gold": 0,
        },
        "effects": {
            "limit": {
                "wood": 400,
                "stone": 400,
                "food":0,
                "metal": 400,
                "population":0,
            },
        },
    },
    {
        "buildingname": "mill",
        "buildTime": 20,
        "costs": {
            "wood": 40,
            "stone": 20,
            "food":0,
            "metal": 10,
            "population":0,
            "gold": 0,
        },
        "effects": {
            "inc": {
                "wood":0,
                "metal": 0,
                "stone": 0,
                "food" : 100,
                "population":0,
            },
        },
    },
    {
        "buildingname": "experimental",
        "buildTime": 99,
        "costs": {
            "wood": 99,
            "stone": 99,
            "metal": 99,
            "food": 99,
            "population":0,
            "gold": 0,
        },
        "effects": {
            "limit": {
                "food" : 9,
                "metal" : 9,
                "stone" : 9,
                "wood" : 9,
                "population":0,
            },
            "inc": {
                "food" : 9,
                "metal" : 9,
                "stone" : 9,
                "wood" : 9,
                "population":0,
            },
        },
    },

]




def dataCreaterAndUpdater(cursor):

    for source in sources:
        cursor.execute("""insert into sourceTypes(stype) values(%s) 
            ON CONFLICT ON CONSTRAINT sourceTypes_pk DO UPDATE SET stype = %s""", (source,source))

    for building in buildings:
        cursor.execute("""insert into buildingTypes(buildingName,buildTime) values(%s,%s)
            ON CONFLICT ON CONSTRAINT buildingTypes_pk DO UPDATE SET 
            buildingName = %s, buildTime = %s""", 
            (building["buildingname"], building["buildTime"],
            building["buildingname"], building["buildTime"]))

        
        wood = building["costs"]["wood"]
        stone = building["costs"]["stone"]
        metal = building["costs"]["metal"]
        food = building["costs"]["food"]
        gold = building["costs"]["gold"]

        cursor.execute("""insert into buildingCosts(buildingName,wood, stone, food, metal ,gold) 
                values(%s, %s, %s, %s ,%s,%s) ON CONFLICT ON CONSTRAINT buildingCosts_pk DO UPDATE
                SET buildingName = %s, wood = %s,  stone = %s,  food = %s,  metal = %s, gold = %s""", 
                    (building["buildingname"], wood, stone, metal, food, gold, 
                    building["buildingname"], wood, stone, metal, food, gold ))
        
        for effect in building["effects"]:
            if effect == "inc":
                for source in building["effects"][effect]:
                    print(building)
                    wood = building["effects"][effect]["wood"]
                    print("after")
                    stone = building["effects"][effect]["stone"]
                    metal = building["effects"][effect]["metal"]
                    food = building["effects"][effect]["food"]
                    gold = building["effects"][effect]["population"]
                    cursor.execute("""insert into buildingIncrementEffects(buildingName,wood, stone, food, metal, population) 
                    values(%s,%s,%s,%s, %s, %s) ON CONFLICT ON CONSTRAINT buildingIncrementEffects_pk DO UPDATE
                    SET buildingName = %s, wood = %s, stone = %s, food = %s,metal = %s,population = %s""", 
                    (building["buildingname"], wood, stone, metal, food, gold ,
                        building["buildingname"], wood, stone, metal, food, gold ))
            elif effect == "limit":
                for source in building["effects"][effect]:
                    wood = building["effects"][effect]["wood"]
                    stone = building["effects"][effect]["stone"]
                    metal = building["effects"][effect]["metal"]
                    food = building["effects"][effect]["food"]
                    gold = building["effects"][effect]["population"]
                    cursor.execute("""insert into buildingLimitEffects(buildingName,wood, stone, food, metal, population) 
                    values(%s,%s,%s,%s, %s, %s) ON CONFLICT ON CONSTRAINT buildingLimitEffects_pk DO UPDATE
                    SET buildingName = %s, wood = %s, stone = %s, food = %s,metal = %s,population = %s""", 
                    (building["buildingname"], wood, stone, metal, food, gold ,
                        building["buildingname"], wood, stone, metal, food, gold ))
        


    pass