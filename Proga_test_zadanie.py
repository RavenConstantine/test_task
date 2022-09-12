import os
#from threading import Thread
from ast import For
import socket
import sqlite3
from multiprocessing import Process

# Создание главной таблицы с IP
conn = sqlite3.connect('nordvpnTest.db', check_same_thread=False)
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS nordip(nnnn INT PRIMARY KEY, ip TEXT);")
conn.commit()
# Функция для проверки нескольких значений "usNNNN.nordvpn.com"
def d(startPoint):
    # Создание временной таблицы с IP
    newConn = sqlite3.connect('nordvpnTest' + str(startPoint) + '.db', check_same_thread=False)
    newCur = newConn.cursor()
    newCur.execute("CREATE TABLE IF NOT EXISTS nordip" + str(startPoint) + "(nnnn INT PRIMARY KEY, ip TEXT);")
    newConn.commit()
    # Цикл, который выполняет проверку сайтов, а так же создает записи
    for i in range(2500):
        ipStr = 'Нет'
        try:
            ipStr = socket.gethostbyname("us" + str(i + 1 + startPoint) + ".nordvpn.com")
            print(ipStr)
        except:
            print('Ошибка' + str(i + 1 + startPoint))
        newCur.execute("INSERT INTO nordip" + str(startPoint) + "(nnnn, ip) VALUES('" + str(i + 1 + startPoint) + "', '" + ipStr +"');")
    newConn.commit()



#    multiprocessing
if __name__ == '__main__':
    # Создание нескольких процессов и их запуск (работает быстрее)
    p1 = Process(target=d, args=(0,))
    p2 = Process(target=d, args=(2500,))
    p3 = Process(target=d, args=(5000,))
    p4 = Process(target=d, args=(7500,))

    p1.start()
    p2.start()
    p3.start()
    p4.start()

    p1.join()
    p2.join()
    p3.join()
    p4.join()

#   threading
# Создание нескольких потоков и их запуск
#t1 = Thread(target=d, args=(0,))
#t2 = Thread(target=d, args=(2500,))
#t3 = Thread(target=d, args=(5000,))
#t4 = Thread(target=d, args=(7500,))
#
#t1.start()
#t2.start()
#t3.start()
#t4.start()
#
#t1.join()
#t2.join()
#t3.join()
#t4.join()
    # Перенос данных в главную таблицу и удаление временных
    for i in range(4):
        cur.execute("ATTACH 'nordvpnTest" + str(i*2500) + ".db' as db" + str(i*2500) + ";")
        cur.execute("INSERT INTO nordip (nnnn, ip) SELECT nnnn, ip FROM nordip" + str(i*2500) + "")
        #cur.execute("SELECT* FROM nordip LEFT JOIN nordip" + str(i*2500) + " ON nordip.nnnn = nordip" + str(i*2500) + ".nnnn;")
        conn.commit()
        cur.execute("DETACH db" + str(i*2500) + ";")
        os.remove("nordvpnTest" + str(i*2500) + ".db")