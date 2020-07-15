import serial
import datetime
import pandas
# import numpy as np
# import matplotlib.plot as plt

sampleFrequency = 3*60

# ser1 = serial.Serial('', 9600)
# ser2 = serial.Serial('COM4', 9600)

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
	results = decoded_bytes + ', ' + str(currTime) + '\n'
	ser.close()
	print(results)
	return results



while(1):

	serPorts = ['ttyACM0']
	for i in serPorts:
		results = readSerial(i, 9600)
		writeFile('sense_data.txt', results)


	# results = readSerial('ttyACM1', 9600)

	# print(results)
	# writeFile('sense_data.txt', results )
	

	

	