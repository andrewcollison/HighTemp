from PyQt5 import QtWidgets, uic
import sys
import serial
from PyQt5.QtCore import *

class serialThread(QThread): # Worker thread
    updateS1 = pyqtSignal(int)

    def __init__(self):
        QThread.__init__(self)
        self.comPort = ""
        
    def run(self):
        ser = serial.Serial(self.comPort)   
        while True:
            ser_bytes = ser.readline()        
            decoded_bytes = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
            self.updateS1.emit(decoded_bytes)
            print(decoded_bytes)


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('serialTest.ui', self)        

        # Buttons
        self.button = self.findChild(QtWidgets.QPushButton, 'serialConnect') # Find the button
        self.button.clicked.connect(self.comThread) # Remember to pass the definition/method, not the return value!

        # Inputs
        self.comInput = self.findChild(QtWidgets.QLineEdit, 'comInput')
        self.sBaudRate = self.findChild(QtWidgets.QLineEdit, 'sBaudRate')

        # LCD display
        self.lcdS1 = self.findChild(QtWidgets.QLCDNumber, 's1Readout')
        self.lcdS2 = self.findChild(QtWidgets.QLCDNumber, 's2Readout')
        
        # Serial Coms
        self.comThread = serialThread()


        self.show()

    def comThread(self):
        self.comThread.comPort = self.comInput.text()
        self.comThread.start()
        self.comThread.updateS1.connect(self.evt_updateS1)    

    def evt_updateS1(self, val):
        self.lcdS1.display(val)  



app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()