from PyQt5 import QtWidgets, uic
import sys

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('serialTest.ui', self)

        # Buttons
        self.button = self.findChild(QtWidgets.QPushButton, 'serialConnect') # Find the button
        self.button.clicked.connect(self.connectSerialBP) # Remember to pass the definition/method, not the return value!

        # Inputs
        self.comInput = self.findChild(QtWidgets.QLineEdit, 'comInput')
        self.sBaudRate = self.findChild(QtWidgets.QLineEdit, 'sBaudRate')

        # LCD display
        self.lcdS1 = self.findChild(QtWidgets.QLCDNumber, 's1Readout')
        self.lcdS2 = self.findChild(QtWidgets.QLCDNumber, 's2Readout')

        self.show()

    def connectSerialBP(self):
        # This is executed when the button is pressed
        print('Connecting to com port:' + self.comInput.text() + ' Baud Rate ' + self.sBaudRate.text())
        self.lcdS1.display(10)

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()