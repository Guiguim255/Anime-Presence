# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SettingsWindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SettingsWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(630, 380)
        MainWindow.setMinimumSize(QtCore.QSize(550, 380))
        MainWindow.setMaximumSize(QtCore.QSize(750, 400))
        font = QtGui.QFont()
        font.setFamily("Rubik")
        font.setPointSize(9)
        MainWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("data/ressources/letters.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        MainWindow.setStyleSheet("background-color: rgb(70, 73, 77);\n"
                                 "color: rgb(255, 255, 255);\n"
                                 "")
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Rubik")
        font.setPointSize(12)
        self.groupBox.setFont(font)
        self.groupBox.setFlat(True)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.comboBox = QtWidgets.QComboBox(self.groupBox)
        font = QtGui.QFont()
        font.setFamily("Rubik")
        font.setPointSize(14)
        self.comboBox.setFont(font)
        self.comboBox.setStyleSheet("QComboBox{\n"
                                    "    background: #616366;\n"
                                    "    border: 1px solid #616366;\n"
                                    "    border-radius: 3px;\n"
                                    "}\n"
                                    "\n"
                                    "QComboBox::drop-down{\n"
                                    "    width: 30px;\n"
                                    "    border-left-width: 1px;\n"
                                    "    border-left-color: darkgray;\n"
                                    "    border-left-style: solid;\n"
                                    "}\n"
                                    "\n"
                                    "QComboBox::down-arrow{\n"
                                    "    image: url(data/ressources/expandwhite.png);\n"
                                    "    width: 16px;\n"
                                    "    height: 16px;\n"
                                    "}\n"
                                    "\n"
                                    "QComboBox QAbstractItemView {\n"
                                    "    border: 2px solid #616366;\n"
                                    "    color: white;\n"
                                    "    background-color: #616366;\n"
                                    "    selection-background-color: #757779;\n"
                                    "    selection-border: 2px solid white;\n"
                                    "    outline: 0px;\n"
                                    "}")
        self.comboBox.setObjectName("comboBox")
        self.verticalLayout_2.addWidget(self.comboBox)
        self.verticalLayout.addWidget(self.groupBox)
        spacerItem = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Rubik")
        font.setPointSize(12)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setFlat(True)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.checkBox = QtWidgets.QCheckBox(self.groupBox_2)
        font = QtGui.QFont()
        font.setFamily("Rubik")
        font.setPointSize(14)
        self.checkBox.setFont(font)
        self.checkBox.setStyleSheet("QCheckBox::indicator{\n"
                                      "    width: 20px;\n"
                                      "    height: 20px;\n"
                                      "}\n"
                                      "\n"
                                      "QCheckBox::indicator:unchecked{\n"
                                      "    image: url(data/ressources/notok.png);\n"
                                      "}\n"
                                      "\n"
                                      "QCheckBox::indicator:checked{\n"
                                      "    image: url(data/ressources/ok.png);\n"
                                      "}")
        self.checkBox.setChecked(True)
        self.checkBox.setAutoExclusive(True)
        self.checkBox.setObjectName("checkBox")
        self.verticalLayout_3.addWidget(self.checkBox)
        self.checkBox_2 = QtWidgets.QCheckBox(self.groupBox_2)
        font = QtGui.QFont()
        font.setFamily("Rubik")
        font.setPointSize(14)
        self.checkBox_2.setFont(font)
        self.checkBox_2.setStyleSheet("QCheckBox::indicator{\n"
                                      "    width: 20px;\n"
                                      "    height: 20px;\n"
                                      "}\n"
                                      "\n"
                                      "QCheckBox::indicator:unchecked{\n"
                                      "    image: url(data/ressources/notok.png);\n"
                                      "}\n"
                                      "\n"
                                      "QCheckBox::indicator:checked{\n"
                                      "    image: url(data/ressources/ok.png);\n"
                                      "}")
        self.checkBox_2.setAutoExclusive(True)
        self.checkBox_2.setObjectName("checkBox_2")
        self.verticalLayout_3.addWidget(self.checkBox_2)
        self.verticalLayout.addWidget(self.groupBox_2)
        spacerItem1 = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Rubik")
        font.setPointSize(12)
        self.groupBox_3.setFont(font)
        self.groupBox_3.setFlat(True)
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.checkBox_3 = QtWidgets.QCheckBox(self.groupBox_3)
        font = QtGui.QFont()
        font.setFamily("Rubik")
        font.setPointSize(14)
        self.checkBox_3.setFont(font)
        self.checkBox_3.setStyleSheet("QCheckBox::indicator{\n"
                                      "    width: 20px;\n"
                                      "    height: 20px;\n"
                                      "}\n"
                                      "\n"
                                      "QCheckBox::indicator:unchecked{\n"
                                      "    image: url(data/ressources/notok.png);\n"
                                      "}\n"
                                      "\n"
                                      "QCheckBox::indicator:checked{\n"
                                      "    image: url(data/ressources/ok.png);\n"
                                      "}")
        self.checkBox_3.setObjectName("checkBox_3")
        self.horizontalLayout_2.addWidget(self.checkBox_3)
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox_3)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit.setFont(font)
        self.lineEdit.setStyleSheet("QLineEdit{\n"
                                    "    background: #616366;\n"
                                    "    border: 2px solid #616366;\n"
                                    "}")
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_2.addWidget(self.lineEdit)
        self.verticalLayout.addWidget(self.groupBox_3)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Rubik")
        font.setPointSize(14)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("QPushButton{\n"
                                      "    background: #4cc321;\n"
                                      "    border: 2px solid #4cc321;\n"
                                      "    border-radius: 15px;\n"
                                      "    padding: 2 10px;\n"
                                      "}")
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.error_label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Rubik")
        font.setPointSize(12)
        self.error_label.setFont(font)
        self.error_label.setStyleSheet("QLabel{\n"
                                        "    color: #bc1a26;\n"
                                        "}")
        self.error_label.setText("Invalid app ID")
        self.error_label.setAlignment(QtCore.Qt.AlignCenter)
        self.error_label.setObjectName("result_label")
        self.verticalLayout.addWidget(self.error_label)
        self.error_label.hide()
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem5)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 630, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Anime Presence - Settings"))
        self.groupBox.setTitle(_translate("MainWindow", "LANGUAGE"))
        self.groupBox_2.setTitle(_translate("MainWindow", "THEME"))
        self.checkBox.setText(_translate("MainWindow", "Dark"))
        self.checkBox_2.setText(_translate("MainWindow", "Light"))
        self.groupBox_3.setTitle(_translate("MainWindow", "PERSONNAL APPLICATION"))
        self.checkBox_3.setText(_translate("MainWindow", "Personnal app ID :"))
        self.pushButton.setText(_translate("MainWindow", "Save changes"))
