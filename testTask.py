import os
from ast import For
import socket
import sqlite3
from multiprocessing import Process

# Функция для проверки нескольких значений "us[server].nordvpn.com"
def scan_nordvpn(startPoint, interRange):
    # Создание временной таблицы с IP
    tempConn = sqlite3.connect('tempNordScan' + str(startPoint) + '.db')
    tempCur = tempConn.cursor()
    tempCur.execute("CREATE TABLE IF NOT EXISTS nordip" + str(startPoint) + "(server INT PRIMARY KEY, ip TEXT);")
    tempConn.commit()

    # Цикл, который выполняет проверку сайтов, а так же создает записи
    for i in range(interRange):
        ipStr = 'Нет ответа'
        try:
            ipStr = socket.gethostbyname("us" + str(i + 1 + startPoint) + ".nordvpn.com")
            print(ipStr + str(i + 1 + startPoint))
        except:
            print('Ошибка ' + str(i + 1 + startPoint))
        tempCur.execute("INSERT INTO nordip" + str(startPoint) + "(server, ip) VALUES('" + str(i + 1 + startPoint) + "', '" + ipStr +"');")
    tempConn.commit()

# multiprocessing
if __name__ == '__main__':
    # Создание главной таблицы с IP
    mainBDConn = sqlite3.connect('nordVPNScan.db')
    mainBDCur = mainBDConn.cursor()
    mainBDCur.execute("CREATE TABLE IF NOT EXISTS nordip(server INT PRIMARY KEY, ip TEXT);")
    mainBDCur.execute("DELETE FROM nordip;")
    mainBDConn.commit()

    # Ввод interationRange, который отвечает за дительность и стартовые точки в функции
    print('Ввдите по сколько доменов вы хотите сканировать в одном потоке из 4')
    interationRange = int(input())

    # Создание нескольких процессов и их запуск (работает быстрее)
    proc1 = Process(target=scan_nordvpn, args=(0, interationRange,))
    proc2 = Process(target=scan_nordvpn, args=(interationRange, interationRange))
    proc3 = Process(target=scan_nordvpn, args=(interationRange*2, interationRange))
    proc4 = Process(target=scan_nordvpn, args=(interationRange*3, interationRange))
    
    proc1.start()
    proc2.start()
    proc3.start()
    proc4.start()

    proc1.join()
    proc2.join()
    proc3.join()
    proc4.join()

    # Перенос данных в главную таблицу и удаление временных
    for i in range(4):
        mainBDCur.execute("ATTACH 'tempNordScan" + str(i*interationRange) + ".db' as db" + str(i*interationRange) + ";")
        mainBDCur.execute("INSERT INTO nordip (server, ip) SELECT server, ip FROM nordip" + str(i*interationRange))
        mainBDConn.commit()
        mainBDCur.execute("DETACH db" + str(i*interationRange) + ";")
        os.remove("tempNordScan" + str(i*interationRange) + ".db")