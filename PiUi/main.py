from PyQt5 import QtWidgets, uic
import sys
from serial import Serial
from PyQt5.QtCore import *
import glob

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
            # print(decoded_bytes)


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('serialTest.ui', self)        

        # Buttons
        self.button = self.findChild(QtWidgets.QPushButton, 'serial_connect_1') # Find the button
        self.button.clicked.connect(self.comThread) # Remember to pass the definition/method, not the return value!

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


        self.show()

    def comSelect1Changed(self, text):
        print(text)
        self.comInput.setText(text)

    def comThread(self):
        self.comThread.comPort = self.comInput.text()
        self.comThread.start()
        self.comThread.updateS1.connect(self.evt_updateS1)    

    def evt_updateS1(self, val):
        self.lcdS1.setText(str(val))  


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



app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()