# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'storage.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow_stor(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 10, 691, 481))
        self.label.setStyleSheet("border-image: url(images/storage.png)")
        self.label.setText("")
        self.label.setObjectName("label")
        self.to0 = QtWidgets.QPushButton(self.centralwidget)
        self.to0.setGeometry(QtCore.QRect(360, 340, 111, 141))
        self.to0.setStyleSheet("border-image: url(images/0.png)")
        self.to0.setText("")
        self.to0.setObjectName("to0")
        self.to1 = QtWidgets.QPushButton(self.centralwidget)
        self.to1.setGeometry(QtCore.QRect(100, 190, 111, 141))
        self.to1.setStyleSheet("border-image: url(images/1.png)")
        self.to1.setText("")
        self.to1.setObjectName("to1")
        self.to2 = QtWidgets.QPushButton(self.centralwidget)
        self.to2.setGeometry(QtCore.QRect(490, 190, 81, 131))
        self.to2.setStyleSheet("border-image: url(images/2.png)")
        self.to2.setText("")
        self.to2.setObjectName("to2")
        self.exit = QtWidgets.QPushButton(self.centralwidget)
        self.exit.setGeometry(QtCore.QRect(500, 70, 41, 51))
        self.exit.setStyleSheet("border:none;\n"
"background-color:rgba(0,0,0,0);")
        self.exit.setText("")
        self.exit.setObjectName("exit")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
