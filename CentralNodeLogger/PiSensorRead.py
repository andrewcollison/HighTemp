import serial
import datetime
import pandas 
import time
from threading import Thread

def writeFile(filename, data):
	file = open(filename, "a")
	file.write(data)
	file.close()

def runA(port):
	while True:
		try:
			serport = port
			ser = serial.Serial(str(serport))
			ser_bytes = ser.readline()
			decoded_bytes = str(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
			currTime = datetime.datetime.now()
			results =  str(currTime) + ', ' + decoded_bytes + '\n'
			ser.close()
			fileName = "Data_"+port+".txt"
			writeFile(fileName, results)
			# with open('leve.txt', 'a') as f:
			# 	f.write(results)
			print(results)
			time.sleep(3)
		
		except:
			currTime = datetime.datetime.now()
			err_str = str(currTime)+ ": Error opening: " + port + "\n" 
			writeFile("ErrorLog.txt", err_str)
			print(err_str)
			time.sleep(5)
			
        

def runB():
	while True:
		print("Thread 2")
		time.sleep(2)

def runC():
	while True:
		print("Thread 3")
		time.sleep(5)

if __name__ == "__main__":
	t1 = Thread(target = runA, args= ['COM3'])
	t2 = Thread(target = runB)
	t3 = Thread(target = runC)
	t1.setDaemon(True)
	t2.setDaemon(True)
	t3.setDaemon(True)
	t1.start()
	t2.start()
	t3.start()
	while True:
		pass