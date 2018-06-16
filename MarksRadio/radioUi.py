from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import subprocess

import mainwindow # This file holds our MainWindow and all design related things
                  # it also keeps events etc that we defined in Qt Designer

class RadioApp(QtWidgets.QMainWindow, mainwindow.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)  # This is defined in design.py file automatically
        self.bluetoothBtn.clicked.connect(self.enableBluetooth)
        self.radioBtn.clicked.connect(self.enableRadio)

    def enableBluetooth(self):
        print "Bluetooth mode"
        subprocess.call(["rfkill", "block",  "wifi"])
        subprocess.call(["rfkill", "unblock", "bluetooth"])

    def enableRadio(self):
        print "Radio mode"
        subprocess.call(["rfkill", "block", "bluetooth"])
        subprocess.call(["rfkill", "unblock", "wifi"])
        subprocess.call(["/opt/script/startvnc.sh"])


def main():
    app = QtWidgets.QApplication(sys.argv)  # A new instance of QApplication
    form = RadioApp()                   # We set the form to be our ExampleApp (design)
    form.show()                         # Show the form
    app.exec_()                         # and execute the app


if __name__ == '__main__':              # if we're running file directly and not importing it
    main()                              # run the main function

