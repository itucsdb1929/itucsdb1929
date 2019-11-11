import db
import threading

POOL_TIME = 5 #Seconds

val = 1


def update():
    # print('someGameStuffDone\n')
    with db.dataBaseLock:
        cursor = db.get_cursor()
        connection = db.get_connection()

        cursor.execute("""INSERT INTO DUMMY VALUES (%s)""", (val,))

        connection.commit()

    global val
    val = val + 1
    gameThread = threading.Timer(POOL_TIME, update, ())
    gameThread.start() 

