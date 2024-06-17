# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from Deskpet_Beeswax import *
from Deskpet_Beeswax import beeswax
from Deskpet_Lappland import lappland
from Deskpet_Magallan import magallan
from log import *
from stor import *
from ex import *
from regi import *
from Deskpet_Lappland import *
from Deskpet_Magallan import *
import os
import random
import sys
import win32api
import win32con
from PyQt5 import QtGui, QtCore
from PyQt5.Qt import *
from PyQt5.QtCore import Qt, QRect, QTimer
from PyQt5.QtGui import QPainter, QImage, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QSystemTrayIcon, QAction, QMenu, QMainWindow, QMessageBox

num = 0

class loginwindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow_log()
        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.ui.login.clicked.connect(self.into_storage)
        self.ui.exit.clicked.connect(self.ex)
        self.ui.register_2.clicked.connect(self.regi)
        self.show()

    def regi(self):
        self.re = regiwindow()
        self.close()

    def into_storage(self):
        name = self.ui.username.text()
        password = self.ui.password.text()
        flag = 0
        f = open('user.txt', mode='r')
        line = f.readline()
        while line:
            if name in line and password in line:
                flag = 1
                break
            line = f.readline()
        if flag == 1:
            self.st = storagewindow()
            self.close()
        else:
            QMessageBox.critical(self, '错误', '用户名或密码错误！请重新输入！')
            self.ui.password.clear()
            self.ui.username.clear()

    def ex(self):
        self.close()
        sys.exit()

    # 拖动鼠标
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and self.isMaximized() == False:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, mouse_event):
        if QtCore.Qt.LeftButton and self.m_flag:
            self.move(mouse_event.globalPos() - self.m_Position)  # 更改窗口位置
            mouse_event.accept()

    def mouseReleaseEvent(self, mouse_event):
        self.m_flag = False
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))


class storagewindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow_stor()
        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.ui.to1.clicked.connect(self.goto_1)
        self.ui.to0.clicked.connect(self.goto_0)
        self.ui.to2.clicked.connect(self.goto_2)
        self.ui.exit.clicked.connect(self.ex)
        self.show()

    def goto_0(self):
        self.main = beeswax.MainWindows()
        self.main.show()
        self.hide()

    def goto_1(self):
        self.main = lappland.MainWindows()
        self.main.show()
        self.hide()

    def goto_2(self):
        self.main = magallan.MainWindows()
        self.main.show()
        self.hide()

    def ex(self):
        self.ex = exitwindow()
        self.ex.show()
        self.close()

    # 拖动鼠标
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and self.isMaximized() == False:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, mouse_event):
        if QtCore.Qt.LeftButton and self.m_flag:
            self.move(mouse_event.globalPos() - self.m_Position)  # 更改窗口位置
            mouse_event.accept()

    def mouseReleaseEvent(self, mouse_event):
        self.m_flag = False
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))


class exitwindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow_ex()
        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.ui.exit.clicked.connect(self.ex)
        self.ui.notexit.clicked.connect(self.back)
        self.show()

    def back(self):
        self.st = storagewindow()
        self.close()

    def ex(self):
        self.log = loginwindow()
        self.close()

    # 拖动鼠标
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and self.isMaximized() == False:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, mouse_event):
        if QtCore.Qt.LeftButton and self.m_flag:
            self.move(mouse_event.globalPos() - self.m_Position)  # 更改窗口位置A+++++++++++
            mouse_event.accept()

    def mouseReleaseEvent(self, mouse_event):
        self.m_flag = False
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))


class regiwindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow_regi()
        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.ui.exit.clicked.connect(self.ex)
        self.ui.enter.clicked.connect(self.register)
        self.ui.reset.clicked.connect(self.reset)
        self.show()

    def reset(self):
        self.ui.password.clear()
        self.ui.username.clear()

    def register(self):
        name = self.ui.username.text()
        password = self.ui.password.text()
        f = open('user.txt', mode='a')
        if name != "" and password != "":
            f.write("\n" + name + " " + password)
            f.close()
            QMessageBox.critical(self, '注册成功', '注册成功！欢迎您使用桌面宠物！')
            self.log = loginwindow()
            self.close()
        else:
            QMessageBox.critical(self, '错误', '用户名或密码不能为空！请重新输入！')
            self.ui.password.clear()
            self.ui.username.clear()

    def ex(self):
        self.log = loginwindow()
        self.close()

    # 拖动鼠标
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and self.isMaximized() == False:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, mouse_event):
        if QtCore.Qt.LeftButton and self.m_flag:
            self.move(mouse_event.globalPos() - self.m_Position)  # 更改窗口位置
            mouse_event.accept()

    def mouseReleaseEvent(self, mouse_event):
        self.m_flag = False
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = loginwindow()

    sys.exit(app.exec_())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
