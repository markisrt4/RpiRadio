# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'bluetoothplayer.ui'
#
# Created: Fri Jul  6 01:31:47 2018
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_bluetoothplayer(object):
    def setupUi(self, bluetoothplayer):
        bluetoothplayer.setObjectName("bluetoothplayer")
        bluetoothplayer.resize(480, 320)
        self.label = QtWidgets.QLabel(bluetoothplayer)
        self.label.setGeometry(QtCore.QRect(0, 0, 481, 321))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("resources/music_background.jpg"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.lcdNumber = QtWidgets.QLCDNumber(bluetoothplayer)
        self.lcdNumber.setGeometry(QtCore.QRect(220, 240, 64, 23))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.lcdNumber.setFont(font)
        self.lcdNumber.setObjectName("lcdNumber")
        self.progressBar = QtWidgets.QProgressBar(bluetoothplayer)
        self.progressBar.setGeometry(QtCore.QRect(180, 270, 118, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.gridLayoutWidget = QtWidgets.QWidget(bluetoothplayer)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(160, 90, 186, 125))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Courier 10 Pitch")
        font.setPointSize(20)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Courier 10 Pitch")
        font.setPointSize(20)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Courier 10 Pitch")
        font.setPointSize(20)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)
        self.songLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.songLabel.setObjectName("songLabel")
        self.gridLayout.addWidget(self.songLabel, 1, 1, 1, 1)
        self.artistLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.artistLabel.setObjectName("artistLabel")
        self.gridLayout.addWidget(self.artistLabel, 0, 1, 1, 1)
        self.albumLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.albumLabel.setObjectName("albumLabel")
        self.gridLayout.addWidget(self.albumLabel, 2, 1, 1, 1)
        self.backBtn = QtWidgets.QPushButton(bluetoothplayer)
        self.backBtn.setGeometry(QtCore.QRect(410, 250, 61, 61))
        self.backBtn.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("resources/Antenna-Small.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.backBtn.setIcon(icon)
        self.backBtn.setIconSize(QtCore.QSize(280, 330))
        self.backBtn.setObjectName("backBtn")

        self.retranslateUi(bluetoothplayer)
        QtCore.QMetaObject.connectSlotsByName(bluetoothplayer)

    def retranslateUi(self, bluetoothplayer):
        _translate = QtCore.QCoreApplication.translate
        bluetoothplayer.setWindowTitle(_translate("bluetoothplayer", "Dialog"))
        self.label_2.setText(_translate("bluetoothplayer", "Album:"))
        self.label_3.setText(_translate("bluetoothplayer", "Artist:"))
        self.label_4.setText(_translate("bluetoothplayer", "Song:"))
        self.songLabel.setText(_translate("bluetoothplayer", "TextLabel"))
        self.artistLabel.setText(_translate("bluetoothplayer", "TextLabel"))
        self.albumLabel.setText(_translate("bluetoothplayer", "TextLabel"))

