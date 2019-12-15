import db
import threading
import statements
POOL_TIME = 5 #Seconds




def update():
    print('someGameStuffDone\n')
    with db.dataBaseLock:
        cursor = db.get_cursor()
        connection = db.get_connection()

        # all_users = statements.get_all_usernames(cursor)

        # for a_user in all_users:
        #     user_cities = statements.get_all_cities_of_user(cursor)
        update_all_sources(cursor)


        connection.commit()

    db.val = db.val + 1
    gameThread = threading.Timer(POOL_TIME, update, ())
    gameThread.start() 



