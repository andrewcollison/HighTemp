import serial
import datetime
import pandas


fileName = 'test1.txt'


def writeFile(filename, data):
	file = open(filename, "a")
	file.write(data)
	file.close()

def readSerial(port, br):
	serport = '/dev/'+ port
	ser = serial.Serial(str(serport), br)
	ser_bytes = ser.readline()
	decoded_bytes = str(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
	currTime = datetime.datetime.now()
	results =  str(currTime) + ', ' + decoded_bytes + '\n'
	ser.close()
	print(results)
	return results

while(1):
	serPorts = ['ttyACM0']
	for i in serPorts:
		results = readSerial(i, 9600)
		writeFile(fileName, results)
	