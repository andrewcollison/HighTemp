from serial import Serial
import datetime
import pandas 
import time
import sys
from threading import Thread
import glob
import sqlite3

def writeFile(filename, data):
	try:
		file = open(filename, "a")
		file.write(data)
		file.close()
	except:
		currTime = str(datetime.datetime.now())
		err_str = currTime + ": Error writing to file: " + filename + ", " + data 
		writeFile("ErrorLog.txt", err_str)
		print(err_str)

def writeDatabase(db_name, db_table, date_time, data_string, com_port):
	try:
		conn = sqlite3.connect(db_name)
		c = conn.cursor()
		sql_command = "INSERT INTO {db_table}(date_time, level_data, com_port) VALUES( '{date_time}', '{data_string}', '{port}' )"\
			.format(db_table = db_table, date_time = date_time, data_string = data_string, port = com_port) 
		print(sql_command)
		c.execute(sql_command)
		conn.commit()
		conn.close()
	except:
		err_str = date_time + ": Error writing to database: " + db_name + ", " + db_table 
		writeFile("ErrorLog.txt", err_str)
		print(err_str)

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = Serial(port)
            s.close()
            result.append(port)
        except (OSError):
            pass
    return result

def runA(port):
	while True:
		try:
			serport = port
			ser = Serial(serport)
			ser_bytes = ser.readline()
			decoded_bytes = str(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
			currTime = datetime.datetime.now()
			results =  str(currTime) + ', ' + decoded_bytes + ', ' + port +'\n'
			ser.close()
			fileName = "Data_"+port+".txt"
			writeFile(fileName, results)
			writeDatabase('CentralDataBase.db', 'SenseData', str(currTime), decoded_bytes, port)
			print(results)
			time.sleep(1)
		
		except:
			currTime = datetime.datetime.now()
			err_str = str(currTime)+ ": Error opening: " + port + "\n" 
			writeFile("ErrorLog.txt", err_str)
			print(err_str)
			time.sleep(5)

if __name__ == "__main__":
	
	threads = []
	comList = serial_ports()
	print(comList)

	for i in range(len(comList)):
		t = Thread(target = runA, args=[comList[i]])
		t.setDaemon(True)
		t.start()
		threads.append(t)

	while True:
		pass