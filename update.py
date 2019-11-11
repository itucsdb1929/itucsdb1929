import db
import threading

POOL_TIME = 5 #Seconds




def update():
    print('someGameStuffDone\n')
    with db.dataBaseLock:
        cursor = db.get_cursor()
        connection = db.get_connection()

        cursor.execute("""INSERT INTO DUMMY VALUES (%s)""", (db.val,))

        connection.commit()

    db.val = db.val + 1
    gameThread = threading.Timer(POOL_TIME, update, ())
    gameThread.start() 

