import sqlite3
from sqlite3 import Error


def SqlConnection(routeDB):
  
    try:
        con = sqlite3.connect(routeDB)
        cur = con.cursor()      
        cur.execute("SELECT * from MainTest WHERE ID=1")
        print("Conexión establecida")
        return con, cur

    except:
        print("Conexión NO establecida")
        return False
    

def GetThings(cur, idQuestion, option="Question"):
        cur.execute(f"SELECT ID,{option} FROM MainTest WHERE ID ={idQuestion}")
        thingExtract = cur.fetchall()[0][1]
        return thingExtract





