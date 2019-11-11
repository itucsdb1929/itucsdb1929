import db
import threading

POOL_TIME = 5 #Seconds




def update():
    print('someGameStuffDone\n')
    gameThread = threading.Timer(POOL_TIME, update, ())
    gameThread.start() 

