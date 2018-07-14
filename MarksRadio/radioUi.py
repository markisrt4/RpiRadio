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
        #self.showFullScreen()
        self.setupUi(self)  # This is defined in design.py file automatically
        self.bluetoothBtn.clicked.connect(self.enableBluetooth)
        self.radioBtn.clicked.connect(self.enableRadio)

    def enableBluetooth(self):
        print "Bluetooth mode"
        subprocess.call(["sudo", "systemctl", "stop", "radiostream"])
        subprocess.call(["sudo", "systemctl", "stop", "radioctrl"])
        subprocess.call(["sudo", "rfkill", "block",  "wifi"])
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
        # self.showFullScreen()
        self.setupUi(self)
        self.backBtn.clicked.connect(self.closeAndReturn)
	self.btmd = BluetoothMetadata()
	self.btThread = BluetoothThread(self.btmd)
	self.btconnected = self.btmd.initialize()
	if self.btconnected != True:
	    print "Error connecting!!"
	else:
	    self.btThread.start()
            self.btThread.updateArtistText.connect(self.updateArtistText)
            self.btThread.updateTitleText.connect(self.updateTitleText)
            self.btThread.updateAlbumText.connect(self.updateAlbumText)
            self.btThread.updateTrackProgress.connect(self.updateTrackProgress)
			

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

    def updateTrackProgress(self, percent):
        self.progressBar.setProperty("value", percent)

class BluetoothThread(QThread):

        updateArtistText = pyqtSignal(str)        
        updateAlbumText  = pyqtSignal(str)        
        updateTitleText  = pyqtSignal(str)        
        updateTrackProgress = pyqtSignal(int)        

	def __init__(self, BluetoothMetadata):
		QThread.__init__(self)
		self.btmd = BluetoothMetadata
                self.isRunning = True

	def __del__(self):
		self.wait()

	def run(self):
		while self.isRunning:
		    self.btmd.tick()
    	            artist = self.btmd.getTrackArtist()
		    title  = self.btmd.getTrackTitle()
		    album  = self.btmd.getTrackAlbum()
		    elapsedTime   = self.btmd.getTrackElapsedSeconds()
		    percComplete = self.btmd.getTrackPercentageComplete() * 100
		    #print "Artist = "+artist
		    #print "Title = "+title
		    #print "Album = "+album
		    #print "Elapsed time = "+ str(elapsedTime)
		    #print "Percentage complete = " + str(percComplete)
		    self.updateAlbumText.emit(album)
		    self.updateTitleText.emit(title)
		    self.updateArtistText.emit(artist)
                    self.updateTrackProgress.emit(percComplete)
		    sleep (1)


def main():
    app = QtWidgets.QApplication(sys.argv)  # A new instance of QApplication
    form = RadioApp()                   # We set the form to be our ExampleApp (design)
    form.show()                         # Show the form
    app.exec_()                         # and execute the app


if __name__ == '__main__':              # if we're running file directly and not importing it
    main()                              # run the main function

