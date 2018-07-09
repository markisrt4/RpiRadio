from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot

import sys
import subprocess

import mainwindow # This file holds our MainWindow and all design related things
import bluetoothplayer

# For Bluetooth Metadata
#sys.path.append('/opt/bin')
from bluetoothmetadata import BluetoothMetadata


from threading import Thread
from time import sleep

class RadioApp(QtWidgets.QMainWindow, mainwindow.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.showFullScreen()
        self.setupUi(self)  # This is defined in design.py file automatically
        self.bluetoothBtn.clicked.connect(self.enableBluetooth)
        self.radioBtn.clicked.connect(self.enableRadio)

    def enableBluetooth(self):
        print "Bluetooth mode"
        subprocess.call(["sudo", "systemctl", "stop", "radiostream"])
        subprocess.call(["sudo", "systemctl", "stop", "radioctrl"])
        #subprocess.call(["sudo", "rfkill", "block",  "wifi"])
        subprocess.call(["sudo", "rfkill", "unblock", "bluetooth"])
        self.hide()
        self.bluetoothmusic = BluetoothMusic(self)
        self.bluetoothmusic.show()
        self.bluetoothmusic.raise_()

    def enableRadio(self):
        print "Radio mode"
        subprocess.call(["sudo", "rfkill", "unblock", "wifi"])
        subprocess.call(["sudo", "rfkill", "block", "bluetooth"])
        subprocess.call(["sudo", "systemctl", "start", "radiostream"])
        subprocess.call(["sudo", "systemctl", "start", "radioctrl"])
        subprocess.call(["/opt/script/startvnc.sh"])

class BluetoothMusic(QtWidgets.QMainWindow, bluetoothplayer.Ui_bluetoothplayer):
    def __init__(self, parent):
        super(self.__class__, self).__init__(parent)
        self.showFullScreen()
        self.setupUi(self)
        self.backBtn.clicked.connect(self.closeAndReturn)
		self.btmd = BluetoothMetadata()
		self.btThread = BluetoothThread(btmd)
	    self.btconnected = self.btmd.initialize()
		if self.btconnected != True:
			print "Error connecting!!"
		else:
			btThread.start()
			

    def closeAndReturn(self):
			# Figure out how to stop thread
            self.close()
            self.parent().show()

    def updateAlbumText(self, text):
            self.albumLabel.setText(text)

    def updateArtistText(self, text):
            self.artistLabel.setText(text)

    def updateTitleText(self, text):
            self.songLabel.setText(text)

class BluetoothThread(Qthread):
	def __init__(self, BluetoothMetadata):
		QThread.__init__(self)
		self.btmd = BluetoothMetadata

	def __del__(self):
		self.wait()

	def run(self):
		btmd.tick()
	    artist   = btmd.getTrackArtist()
		title      = btmd.getTrackTitle()
		album = btmd.getTrackAlbum()
		elapsedTime   = btmd.getTrackElapsedSeconds()
		percComplete = btmd.getTrackPercentageComplete()
		print "Artist = "+artist
		print "Title = "+title
		print "Album = "+album
		print "Elapsed time = "+ str(elapsedTime)
		print "Percentage complete = " + str(percComplete)
		self.emit(SIGNAL('updateAlbumText(QString)'), album)
		self.emit(SIGNAL('updateTitleText(QString)'), title)
		self.emit(SIGNAL('updateArtistText(QString)'), artist)
		sleep (.5)

def main():
    app = QtWidgets.QApplication(sys.argv)  # A new instance of QApplication
    form = RadioApp()                   # We set the form to be our ExampleApp (design)
    form.show()                         # Show the form
    app.exec_()                         # and execute the app


if __name__ == '__main__':              # if we're running file directly and not importing it
    main()                              # run the main function

