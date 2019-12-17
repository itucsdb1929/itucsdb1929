import db
import threading
import statements
from functionsyusuf import update_all_city_limits, update_all_user_sources, update_all_user_productions
from functionsosman import update_all_city_sources, update_all_city_productions
from functions3 import updateBuildings
POOL_TIME = 5 #Seconds




def update():
    print('someGameStuffDone\n')
    with db.dataBaseLock:
        cursor = db.get_cursor()
        connection = db.get_connection()

        # all_users = statements.get_all_usernames(cursor)

        # for a_user in all_users:
        #     user_cities = statements.get_all_cities_of_user(cursor)
        # updateBuildings(cursor)
        print("deneme val", db.val)
        updateBuildings(cursor)
        update_all_city_limits(cursor)
        update_all_city_productions(cursor)
        update_all_user_productions(cursor)
        update_all_city_sources(cursor)
        update_all_user_sources(cursor)


        connection.commit()

    db.val = db.val + 1


