import statements
import functions3
import db
def user_inform(cusername):
    with db.dataBaseLock:
        cursor = db.get_cursor()
        connection = db.get_connection()
        
        limitsDct = statements.get_user_source_limits(cursor, username)
        userSources = statements.get_sources_of_user(cursor, username)
        cities = statements.get_cities_of_user(cursor, username)
        total_production = {}
        for city in cities:
            prod = get_production_of_city(cursor, city)
            # for (stype, value)        

#####NOT FINISHED FUNCTION 

