from PyQt5 import QtWidgets, uic
import sys
from serial import Serial
from PyQt5.QtCore import *
import glob
import matplotlib.pyplot as plt
import datetime
import time
import pandas as pd
from pyqtgraph import PlotWidget
import pyqtgraph as pg

class serialThread(QThread): # Worker thread
    updateS1 = pyqtSignal(int)

    def __init__(self):
        QThread.__init__(self)
        self.comPort = ""
    

    def run(self):
        ser = Serial(self.comPort)   
        while True:
            ser_bytes = ser.readline()        
            decoded_bytes = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
            self.updateS1.emit(decoded_bytes)
            currTime = datetime.datetime.now()
            results =  str(currTime) + ', ' + str(decoded_bytes) + '\n'
            writeFile('test1.csv', results)
            # print(decoded_bytes)    
    

class plotThread(QThread):
    def __init__(self):
        QThread.__init__(self)    
    
    def run(self):
        df = pd.read_csv("test1.csv", header = None, parse_dates=True, index_col = [0])
        print(df)
        
        # plt.plot(df.index, df[1])
        # plt.show()
        


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('serialTest.ui', self)        
        self.currTime = []
        self.reading = []
        # Buttons
        self.button = self.findChild(QtWidgets.QPushButton, 'serial_connect_1') # Find the button
        self.button.clicked.connect(self.comThread) # Remember to pass the definition/method, not the return value!

        # Graph button
        self.graphS1button = self.findChild(QtWidgets.QPushButton, 'graph_s1')
        self.graphS1button.clicked.connect(self.visThread1)

        # Drop down
        self.comPortSelect = self.findChild(QtWidgets.QComboBox)        
        self.comPortSelect.addItems(serial_ports())
        self.comPortSelect.activated[str].connect(self.comSelect1Changed)    

        # Inputs
        self.comInput = self.findChild(QtWidgets.QLineEdit, 'serial_input_1')

        # Display Data
        self.lcdS1 = self.findChild(QtWidgets.QLabel, 's1_output')
        
        # Serial Coms
        self.comThread = serialThread()

        # Plot Data
        self.visThread1 = plotThread()
        # self.plot([1,2,3,4,5,6,7,8,9,10], [30,32,34,32,33,31,29,32,35,45])

        self.show()



    # def plot(self, hour, temperature):
    #     self.graphWidget.plot(hour, temperature)


    def comSelect1Changed(self, text):
        print(text)
        self.comInput.setText(text)

    def comThread(self):
        self.comThread.comPort = self.comInput.text()
        self.comThread.start()
        self.comThread.updateS1.connect(self.evt_updateS1)  

    def visThread1(self):
        self.visThread1.start()

    def evt_updateS1(self, val):
        self.lcdS1.setText(str(val)) 
        self.currTime.append(time.time())
        self.reading.append(val)
        self.graphWidget.plot(self.currTime[len(self.currTime)-30: len(self.currTime)], self.reading[len(self.currTime)-30: len(self.currTime)])
        # self.plot(currTime, val)


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

def writeFile(filename, data):
	    file = open(filename, "a")
	    file.write(data)
	    file.close()

def plot(self, hour, temperature):
        self.graphWidget.plot(hour, temperature)


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()