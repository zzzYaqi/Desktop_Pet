import os
import random
import sys
import win32api
import win32con
from PyQt5 import QtGui,QtCore
from PyQt5.Qt import *
from PyQt5.QtCore import Qt, QRect, QTimer
from PyQt5.QtGui import QPainter, QImage, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QSystemTrayIcon, QAction, QMenu
import subprocess

class MainWindows(QWidget):
    def __init__(self):
        # 调用父类初始化函数
        super(MainWindows, self).__init__()
        #去掉边框
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        # qr = self.geometry()
        # cp = QtGui.QGuiApplication.primaryScreen().availableGeometry().center()
        # qr.moveCenter(cp)
        # # self.move(qr.topLeft())

        # 当前宠物
        self.resource='Deskpet_Lappland\\deskpet'

        # 设置窗口的尺寸
        self.resize(3000, 3000)

        # 初始化菜单，托盘与右键人物用同一套菜单
        self.menu_init()
        self.tray_init()
        self.right_press_menu()

        # 当前图片位置(左上角)
        self.position_x = 700
        self.position_y = 0

        # flag
        self.end_drop_flag=False  # 落地
        self.relax_flag=False  # relax
        self.Geocentric_travel_notes=False  # 人为拖下去
        self.Poke_flag=False  # 戳一戳
        self.sit_flag=False
        self.sleep_flag=False
        self.attack_flag = False
        self.skill_flag = False
        self.idle_flag = False

        self.right_press_flag=False  # 是否右键按下

        # 当前加载的图片路径与第几张图与当前图片的第几个周期与...
        self.image_index=0  # 第几张图
        self.the_same_image=0  # 当前图片的第几个周期
        self.the_same_image_index=3  # 同一图组加载多少图
        self.path=os.path.join(self.resource,str(self.image_index)+'.png')

        # 扫描各图像包图像量
        self.relax_index=len(os.listdir(os.path.join(self.resource, 'left', 'relax')))
        self.drop_index=len(os.listdir(os.path.join(self.resource, 'left', 'drop')))
        self.run_index=len(os.listdir(os.path.join(self.resource, 'left', 'move')))
        self.poke_index=len(os.listdir(os.path.join(self.resource, 'left', 'poke')))
        self.sit_index=len(os.listdir(os.path.join(self.resource, 'left', 'sit')))
        self.sleep_index=len(os.listdir(os.path.join(self.resource, 'left', 'sleep')))
        self.attack_index = len(os.listdir(os.path.join(self.resource, 'left', 'attack')))
        self.skill_index = len(os.listdir(os.path.join(self.resource, 'left', 'skill')))
        self.idle_index = len(os.listdir(os.path.join(self.resource, 'left', 'idle')))

        # 图像刷新频率(ms)
        self.image_refresh_rate=30

        # 运动方向与长度
        self.run_diction='left'
        self.run_diction_index=0  # 1,-1
        self.run_length=0

        # 睡眠时间与坐下时间
        self.sleep_or_sit_nowtime=0
        self.sleep_or_sit_time=0

        # 步长
        self.step_length=2

        # 牛顿棺材板部分
        self.delta_x=0
        self.delta_y=0
        self.Gravity_velocity=0  # 当前加速度
        self.Gravitational_acceleration=1  # 重力加速度

        # 边界
        self.left_bound = -150
        self.right_bound = win32api.GetSystemMetrics(win32con.SM_CXSCREEN) -100
        self.up_bound = -200
        self.down_bound = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)-320

        # 初始化一个定时器
        self.timer = QTimer()
        self.timer.start(self.image_refresh_rate)
        self.timer.timeout.connect(self.Central_processor)

        # 对话框
        QToolTip.setFont(QFont('楷体', 14))
        y = ['每次见到你都很开心呀']
        self.setToolTip(random.choice(y))

    # 中心处理器
    # 优先级：
    # 是否坠落
    # 是否落地
    # 是否attack
    # 是否skill
    # 是否idle（idle是带装备的relax）
    # 是否戳一戳
    # 是否relax
    # 是否run(move)
    # 是否sit
    # 是否sleep
    # 下一个动作判断
    def Central_processor(self):

    ###落地及后续动作###
        if self.position_y!=self.down_bound:
            if self.position_y>self.down_bound:
                self.Geocentric_travel_notes=True
            self.the_coffin_board_of_Newton()
            self.repaint()
        elif self.end_drop_flag==True:
            self.path=os.path.join(self.resource,self.run_diction,'drop',str(self.image_index)+'.png')
            self.the_same_image+=1
            self.the_same_image_index_check()
            if self.image_index>=self.drop_index:
                self.end_drop_flag=False
                self.attack_flag = True
                self.image_index=0
            self.repaint() #坠落
        elif self.attack_flag == True:
            self.path = os.path.join(self.resource, self.run_diction, 'attack', str(self.image_index) + '.png')
            self.the_same_image += 1
            self.the_same_image_index_check()
            if self.image_index >= self.attack_index:
                self.attack_flag = False
                self.skill_flag = True
                self.image_index = 0
            if self.the_same_image == 0:
                self.repaint()
        elif self.skill_flag == True:
            self.path = os.path.join(self.resource, self.run_diction, 'skill', str(self.image_index) + '.png')
            self.the_same_image += 1
            self.the_same_image_index_check()
            if self.image_index >= self.skill_index:
                self.skill_flag = False
                self.idle_flag = True
                self.image_index = 0
            if self.the_same_image == 0:
                self.repaint()
        elif self.idle_flag == True:
            self.path = os.path.join(self.resource, self.run_diction, 'idle', str(self.image_index) + '.png')
            self.the_same_image += 1
            self.the_same_image_index_check()
            if self.image_index >= self.idle_index:
                self.idle_flag = False
                self.image_index = 0
            if self.the_same_image == 0:
                self.repaint()

        elif self.Poke_flag==True:
            self.path=os.path.join(self.resource,self.run_diction,'poke',str(self.image_index)+'.png')
            self.the_same_image += 1
            self.the_same_image_index_check()
            if self.image_index>=self.poke_index:
                self.path=os.path.join(self.resource,self.run_diction,'relax','0.png')
                self.Poke_flag=False
                self.image_index=0
            if self.the_same_image==0:
                self.repaint()
        elif self.run_diction_index!=0 or self.relax_flag==True or self.sit_flag==True or self.sleep_flag==True:
            if self.relax_flag==True:  # relax
                self.path = os.path.join(self.resource, self.run_diction,'relax', str(self.image_index) + '.png')
                self.the_same_image += 1
                self.the_same_image_index_check()
                if self.image_index >= self.relax_index:
                    self.relax_flag = False
                    self.image_index = 0
                if self.the_same_image == 0:
                    self.repaint()
            elif self.sit_flag==True:
                self.path=os.path.join(self.resource, self.run_diction, 'sit', str(self.image_index) + '.png')
                self.the_same_image += 1
                self.the_same_image_index_check()
                if self.image_index >= self.sit_index:
                    self.sleep_or_sit_nowtime+=1
                    if self.sleep_or_sit_nowtime>=self.sleep_or_sit_time:
                        self.sleep_or_sit_nowtime=0
                        self.sit_flag = False
                    self.image_index = 0
                if self.the_same_image == 0:
                    self.repaint()
            elif self.sleep_flag==True:
                self.path=os.path.join(self.resource, self.run_diction, 'sleep', str(self.image_index) + '.png')
                self.the_same_image += 1
                self.the_same_image_index_check()
                if self.image_index >= self.sleep_index:
                    self.sleep_or_sit_nowtime+=1
                    if self.sleep_or_sit_nowtime>=self.sleep_or_sit_time:
                        self.sleep_or_sit_nowtime=0
                        self.sleep_flag = False
                    self.image_index = 0
                if self.the_same_image==0:
                    self.repaint()
            else:
                self.position_x=self.position_x+self.step_length*self.run_diction_index
                self.path = os.path.join(self.resource, self.run_diction, 'move', str(self.image_index) + '.png')
                self.the_same_image += 1
                self.the_same_image_index_check()
                self.run_length-=self.step_length
                if self.position_x>=self.right_bound or self.position_x<=self.left_bound:
                    self.run_length=0
                if self.image_index>=self.run_index:
                    self.image_index=1
                if self.run_length<=0:
                    self.run_diction_index = 0
                    self.image_index = 0
                self.repaint()
        else:
            next_action_index=random.randint(1,110)
            if next_action_index<=70:  # relax
                self.relax_flag=True
            elif next_action_index<=100:  # run(move)
                if next_action_index<=85:
                    self.run_diction='left'
                    self.run_diction_index=-1
                else:
                    self.run_diction='right'
                    self.run_diction_index=1
                self.run_length = random.randint(1, 5) * (self.run_index-1) * self.step_length*self.the_same_image_index
            elif next_action_index<=105:  # sit
                self.sleep_or_sit_time=(next_action_index-100)*8
                self.sit_flag=True
            elif next_action_index<=110:  # sleep
                self.sleep_or_sit_time=(next_action_index-103)*10
                self.sleep_flag=True
            self.repaint()

    def the_coffin_board_of_Newton(self):
        self.position_x = self.position_x + self.delta_x
        self.position_y = self.position_y + self.delta_y + self.Gravity_velocity
        self.Gravity_velocity += self.Gravitational_acceleration
        if self.Geocentric_travel_notes==False:
            if self.position_y >= self.down_bound:
                self.position_y = self.down_bound
                self.end_drop_flag = True
                self.the_coffin_board_of_Newton_flag=False
                self.delta_x=0
                self.delta_y=0
                self.Gravity_velocity = 0
                self.image_index+=1
        else:
            if self.position_y>self.down_bound+300:
                self.position_y=self.up_bound
                self.Geocentric_travel_notes=False
        # 左右穿墙
        if self.position_x > self.right_bound:
            self.position_x = self.left_bound
        elif self.position_x < self.left_bound:
            self.position_x = self.right_bound


    # 鼠标相关代码
    # 一次性（检测鼠标按下）
    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        self.timer.stop()
        self.image_index = 0
        self.relax_flag = False
        self.sit_flag = False
        self.sleep_flag = False
        self.right_press_flag=False
        self.run_diction_index = 0
        self.Gravity_velocity = 0
        self.the_same_image = 0
        if ev.buttons() == QtCore.Qt.LeftButton:  # 左键 绑定
            self.Poke_flag = True
            self.mouse_drag_pos = ev.globalPos() - self.pos()
        elif ev.buttons() == QtCore.Qt.RightButton:  # 右键 绑定
            self.right_press_flag=True

    # 只要鼠标按下循环触发
    def mouseMoveEvent(self, event):
        self.Poke_flag=False
        self.delta_x=int((QCursor.pos().x()-75-self.position_x)/5)
        self.delta_y=int((QCursor.pos().y()-119-self.position_y)/5)
        self.position_x=QCursor.pos().x()-75
        self.position_y=QCursor.pos().y()-119
        if self.delta_x > 0:
            self.run_diction = 'right'
        elif self.delta_x<0:
            self.run_diction = 'left'
        self.path=os.path.join(self.resource,self.run_diction,'drop','0.png')
        self.repaint()

    # 重写鼠标抬起事件
    def mouseReleaseEvent(self, event):
        if self.position_y==self.down_bound:
            pass
        else:
            self.Poke_flag=False
        if not self.right_press_flag:
            self.timer.start(self.image_refresh_rate)


    def paintEvent(self, event):
        qp = QPainter(self)
        # 装载图像
        image = QImage(self.path)
        rect3 = QRect(self.position_x, self.position_y, int(image.width()*3/4), int(image.height()*3/4)) #修改小人大小
        qp.drawImage(rect3, image)

    def menu_init(self):
        quit_action = QAction('退出', self, triggered=self.quit)  # 设置右键点开能看到的选项与相应功能
        quit_action.setIcon(QIcon('deskpet\\0.png'))  # 设置右键点开时左边的图片

        shot = QAction('截图', self, triggered = self.screenshot)
        Shot_Icon = QIcon('screenshot.png')
        shot.setIcon(Shot_Icon)

        self.tray_icon_menu = QMenu(self)
        self.tray_icon_menu.addAction(quit_action)  # 添加功能

        self.tray_icon_menu.addAction(shot)

    def tray_init(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon('deskpet\\0.png'))  # 托盘图案
        self.tray_icon.setContextMenu(self.tray_icon_menu)  # 绑定功能
        self.tray_icon.show()  # show

    def right_press_menu(self):
        # 将ContextMenuPolicy设置为Qt.CustomContextMenu
        # 否则无法使用customContextMenuRequested信号
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        # 创建QMenu信号事件
        self.customContextMenuRequested.connect(self.showMenu)
    def showMenu(self):
        self.tray_icon_menu.exec_(QCursor.pos())  # 在鼠标位置显示

    def the_same_image_index_check(self):
        if self.the_same_image>=self.the_same_image_index:
            self.image_index+=1
            self.the_same_image=0

    def screenshot(self):
        # os.system('screenshot.exe')
        subprocess.run('screenshot.exe')

    def enterEvent(self, event):  # 鼠标移进时调用
        # print('鼠标移入')
        self.setCursor(Qt.ClosedHandCursor)  # 设置鼠标形状。需要from PyQt5.QtGui import QCursor,from PyQt5.QtCore import Qt
        '''
        Qt.PointingHandCursor   指向手            Qt.WaitCursor  旋转的圆圈
        ArrowCursor   正常箭头                 Qt.ForbiddenCursor 红色禁止圈
        Qt.BusyCursor      箭头+旋转的圈      Qt.WhatsThisCursor   箭头+问号
        Qt.CrossCursor      十字              Qt.SizeAllCursor    箭头十字
        Qt.UpArrowCursor 向上的箭头            Qt.SizeBDiagCursor  斜向上双箭头
        Qt.IBeamCursor   I形状                 Qt.SizeFDiagCursor  斜向下双箭头
        Qt.SizeHorCursor  水平双向箭头          Qt.SizeVerCursor  竖直双向箭头
        Qt.SplitHCursor                        Qt.SplitVCursor  
        Qt.ClosedHandCursor   非指向手          Qt.OpenHandCursor  展开手
        '''
        # self.unsetCursor()   #取消设置的鼠标形状

    def talk(self):
        if not self.talk_condition:
            self.label1.setText(random.choice(self.sentence))
            self.label1.setStyleSheet("font: bold;font:15pt '楷体';color:yellow;background-color: black")  # 设置边框
            self.label1.adjustSize()
            self.talk_condition = 1
        else:
            self.label1.setText("")
            self.label1.adjustSize()
            self.talk_condition = 0

    def quit(self):
        self.close()
        sys.exit()