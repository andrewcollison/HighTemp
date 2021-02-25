from serial import Serial
import datetime
import pandas 
import time
import sys
from threading import Thread
import glob

def writeFile(filename, data):
	file = open(filename, "a")
	file.write(data)
	file.close()

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
			ser = Serial(str(serport))
			ser_bytes = ser.readline()
			decoded_bytes = str(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
			currTime = datetime.datetime.now()
			results =  str(currTime) + ', ' + decoded_bytes + '\n'
			ser.close()
			fileName = "Data_"+port+".txt"
			writeFile(fileName, results)
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
	# comList = ["COM6", "COM5", "COM7"]
	comList = serial_ports()
	print(comList)
	# print(comList[0])
	for i in range(len(comList)):
		t = Thread(target = runA, args=[comList[i]])
		t.setDaemon(True)
		t.start()
		threads.append(t)
	while True:
		pass