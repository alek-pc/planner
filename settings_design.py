# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings_design.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(478, 309)
        font = QtGui.QFont()
        font.setPointSize(10)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.bt_back = QtWidgets.QPushButton(self.centralwidget)
        self.bt_back.setGeometry(QtCore.QRect(10, 0, 75, 23))
        self.bt_back.setStyleSheet("")
        self.bt_back.setObjectName("bt_back")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(100, 0, 303, 231))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.rbts = QtWidgets.QHBoxLayout()
        self.rbts.setObjectName("rbts")
        self.rbt_light_theme = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.rbt_light_theme.setChecked(True)
        self.rbt_light_theme.setObjectName("rbt_light_theme")
        self.rbts.addWidget(self.rbt_light_theme)
        self.rbt_dark_theme = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.rbt_dark_theme.setObjectName("rbt_dark_theme")
        self.rbts.addWidget(self.rbt_dark_theme)
        self.rbt_own_theme = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.rbt_own_theme.setObjectName("rbt_own_theme")
        self.rbts.addWidget(self.rbt_own_theme)
        self.verticalLayout.addLayout(self.rbts)
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 0, 0, 1, 1)
        self.bt1 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.bt1.setMinimumSize(QtCore.QSize(0, 30))
        self.bt1.setMaximumSize(QtCore.QSize(30, 16777215))
        self.bt1.setText("")
        self.bt1.setObjectName("bt1")
        self.gridLayout_2.addWidget(self.bt1, 0, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 0, 2, 1, 1)
        self.bt2 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.bt2.setMinimumSize(QtCore.QSize(0, 30))
        self.bt2.setMaximumSize(QtCore.QSize(30, 16777215))
        self.bt2.setAutoFillBackground(False)
        self.bt2.setStyleSheet(" background-color: rgb(255, 0, 0)")
        self.bt2.setText("")
        self.bt2.setObjectName("bt2")
        self.gridLayout_2.addWidget(self.bt2, 0, 3, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.bt3 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.bt3.setMinimumSize(QtCore.QSize(30, 30))
        self.bt3.setMaximumSize(QtCore.QSize(30, 16777215))
        self.bt3.setText("")
        self.bt3.setObjectName("bt3")
        self.gridLayout.addWidget(self.bt3, 1, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_8.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 3, 2, 1, 1)
        self.bt4 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.bt4.setMinimumSize(QtCore.QSize(0, 30))
        self.bt4.setMaximumSize(QtCore.QSize(30, 16777215))
        self.bt4.setText("")
        self.bt4.setObjectName("bt4")
        self.gridLayout.addWidget(self.bt4, 1, 3, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_6.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 1, 2, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_7.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 3, 0, 1, 1)
        self.bt5 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.bt5.setMinimumSize(QtCore.QSize(30, 30))
        self.bt5.setMaximumSize(QtCore.QSize(30, 16777215))
        self.bt5.setText("")
        self.bt5.setObjectName("bt5")
        self.gridLayout.addWidget(self.bt5, 3, 1, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_10.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 4, 2, 1, 1)
        self.bt8 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.bt8.setMinimumSize(QtCore.QSize(0, 30))
        self.bt8.setMaximumSize(QtCore.QSize(30, 16777215))
        self.bt8.setText("")
        self.bt8.setObjectName("bt8")
        self.gridLayout.addWidget(self.bt8, 4, 3, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_9.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 4, 0, 1, 1)
        self.bt7 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.bt7.setMinimumSize(QtCore.QSize(30, 30))
        self.bt7.setMaximumSize(QtCore.QSize(30, 16777215))
        self.bt7.setText("")
        self.bt7.setObjectName("bt7")
        self.gridLayout.addWidget(self.bt7, 4, 1, 1, 1)
        self.bt6 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.bt6.setMinimumSize(QtCore.QSize(0, 30))
        self.bt6.setMaximumSize(QtCore.QSize(30, 16777215))
        self.bt6.setText("")
        self.bt6.setObjectName("bt6")
        self.gridLayout.addWidget(self.bt6, 3, 3, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.standard = QtWidgets.QPushButton(self.centralwidget)
        self.standard.setGeometry(QtCore.QRect(300, 240, 100, 23))
        self.standard.setObjectName("standard")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 478, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Настройки"))
        self.bt_back.setText(_translate("MainWindow", "Назад"))
        self.rbt_light_theme.setText(_translate("MainWindow", "Свтелая тема"))
        self.rbt_dark_theme.setText(_translate("MainWindow", "Тёмная тема"))
        self.rbt_own_theme.setText(_translate("MainWindow", "Своя тема"))
        self.label.setText(_translate("MainWindow", "Цвета"))
        self.label_3.setText(_translate("MainWindow", "Фон"))
        self.label_4.setText(_translate("MainWindow", "Текст"))
        self.label_2.setText(_translate("MainWindow", "Календарь"))
        self.label_8.setText(_translate("MainWindow", "Свой праздник"))
        self.label_6.setText(_translate("MainWindow", "Выходной день"))
        self.label_7.setText(_translate("MainWindow", "Общий праздник"))
        self.label_10.setText(_translate("MainWindow", "Напоминания"))
        self.label_9.setText(_translate("MainWindow", "Свой выходной"))
        self.label_5.setText(_translate("MainWindow", "Рабочий день"))
        self.standard.setText(_translate("MainWindow", "По умолчанию"))
