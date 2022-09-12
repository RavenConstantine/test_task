import os
from threading import Thread
from ast import For
import socket
import sqlite3

conn = sqlite3.connect('nordvpnTest.db', check_same_thread=False)
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS nordip(nnnn INT PRIMARY KEY, ip TEXT);")
conn.commit()

def d(startPoint):
    newConn = sqlite3.connect('nordvpnTest' + str(startPoint) + '.db', check_same_thread=False)
    newCur = newConn.cursor()
    newCur.execute("CREATE TABLE IF NOT EXISTS nordip" + str(startPoint) + "(nnnn INT PRIMARY KEY, ip TEXT);")
    newConn.commit()
    for i in range(2500):
        ipStr = 'Нет'
        try:
            ipStr = socket.gethostbyname("us" + str(i + 1 + startPoint) + ".nordvpn.com")
            print(ipStr)
        except:
            print('Ошибка' + str(i + 1 + startPoint))
        newCur.execute("INSERT INTO nordip" + str(startPoint) + "(nnnn, ip) VALUES('" + str(i + 1 + startPoint) + "', '" + ipStr +"');")
    newConn.commit()
    



t1 = Thread(target=d, args=(0,))
t2 = Thread(target=d, args=(2500,))
t3 = Thread(target=d, args=(5000,))
t4 = Thread(target=d, args=(7500,))

t1.start()
t2.start()
t3.start()
t4.start()

t1.join()
t2.join()
t3.join()
t4.join()
for i in range(4):
    cur.execute("ATTACH 'nordvpnTest" + str(i*2500) + ".db' as db" + str(i*2500) + ";")
    cur.execute("INSERT INTO nordip (nnnn, ip) SELECT nnnn, ip FROM nordip" + str(i*2500) + "")
    #cur.execute("SELECT* FROM nordip LEFT JOIN nordip" + str(i*2500) + " ON nordip.nnnn = nordip" + str(i*2500) + ".nnnn;")
    conn.commit()
    cur.execute("DETACH db" + str(i*2500) + ";")
    os.remove("nordvpnTest" + str(i*2500) + ".db")