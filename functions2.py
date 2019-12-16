import statements
import functions3
import data
import db

def get_total_user_productions(cursor, username):
    cursor.execute("""select productions.stype, sum(productions.value) from productions join cities on cities.cityname=productions.cityname  
	            where cities.username=%s  group by stype""",(username,))

    prd = cursor.fetchall()
    prdDict = data.sourcesDict
    for key in prd:
        prdDict[key] = prd[key]
    
    return prdD


def user_inform(username):
    with db.dataBaseLock:
        cursor = db.get_cursor()
        connection = db.get_connection()
        
        limitsDct = statements.get_user_source_limits(cursor, username)
        userSources = statements.get_sources_of_user(cursor, username)
        cities = statements.get_cities_of_user(cursor, username)
        total_production = 
            # for (stype, value)        

#####NOT FINISHED FUNCTION 

