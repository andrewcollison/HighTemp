
from serial import Serial
import datetime
import pandas 
import time
import sys
from threading import Thread
import glob

def writeDatabase(db_name, db_table, date_time, data_string):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    sql_command = "INSERT INTO {db_table}(dateTime, levelData) VALUES( '{date_time}', '{data_string}' )"\
        .format(db_table = db_table, date_time = date_time, data_string = data_string) 
    print(sql_command)
    c.execute(sql_command)
    conn.commit()
    conn.close()


def main():
    db_name = 'CentralDataBase.db'
    db_table = "LevelData"
    date_time = str(datetime.datetime.now())
    data_string = "hello world"

    writeDatabase(db_name, db_table, date_time, data_string)
    
		

if __name__ == "__main__":
    main()