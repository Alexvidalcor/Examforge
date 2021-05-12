import sqlite3
from sqlite3 import Error



def SqlConnection(routeDB):
    try:
        con = sqlite3.connect(routeDB)
        cur = con.cursor()
        cur.execute("SELECT * from MainExam WHERE ID=1")
        print("Conexión establecida")
        return cur

    except:
        print("Conexión NO establecida")
        return False
     



