# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AnimePresence_MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(650, 275)
        MainWindow.setMinimumSize(QtCore.QSize(650, 250))
        MainWindow.setMaximumSize(QtCore.QSize(800, 350))
        font = QtGui.QFont()
        font.setFamily("Rubik")
        font.setPointSize(9)
        MainWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("data/ressources/letters.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        MainWindow.setObjectName("MainWindow")
        MainWindow.setStyleSheet("QWidget#MainWindow{background-color: rgb(70, 73, 77);}\n"
                                 "*{color: rgb(255, 255, 255);}\n"
                                 "")
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.logo_image = QtWidgets.QLabel(self.centralwidget)
        self.logo_image.setMinimumSize(QtCore.QSize(80, 80))
        self.logo_image.setMaximumSize(QtCore.QSize(80, 80))
        self.logo_image.setText("")
        self.logo_image.setPixmap(QtGui.QPixmap("data/ressources/letters.png"))
        self.logo_image.setScaledContents(True)
        self.logo_image.setObjectName("logo_image")
        self.horizontalLayout_3.addWidget(self.logo_image)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.title_label = QtWidgets.QLabel(self.centralwidget)
        self.title_label.setMinimumSize(QtCore.QSize(0, 80))
        font = QtGui.QFont()
        font.setFamily("Rubik")
        font.setPointSize(16)
        self.title_label.setFont(font)
        self.title_label.setStyleSheet("")
        self.title_label.setObjectName("title_label")
        self.horizontalLayout_3.addWidget(self.title_label)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        spacerItem2 = QtWidgets.QSpacerItem(20, 26, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.urlLayout = QtWidgets.QVBoxLayout()
        self.url_entry = QtWidgets.QLineEdit(self.centralwidget)
        self.urlLayout.addWidget(self.url_entry)
        self.url_entry.setMinimumSize(QtCore.QSize(400, 30))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.url_entry.setFont(font)
        self.url_entry.setStyleSheet("QLineEdit{\n"
                                     "    background: #616366;\n"
                                     "    border: 2px solid #616366;\n"
                                     "    border-radius: 10px\n"
                                     "}")
        self.url_entry.setObjectName("url_entry")
        self.horizontalLayout_2.addLayout(self.urlLayout)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem5 = QtWidgets.QSpacerItem(20, 25, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem5)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem6)
        self.confirm_button = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.confirm_button.sizePolicy().hasHeightForWidth())
        self.confirm_button.setSizePolicy(sizePolicy)
        self.confirm_button.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Rubik")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.confirm_button.setFont(font)
        self.confirm_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.confirm_button.setMouseTracking(False)
        self.confirm_button.setStyleSheet("QPushButton{\n"
                                          "    background: #616366;\n"
                                          "    border: 2px solid #616366;\n"
                                          "    border-radius: 15px;\n"
                                          "    padding: 2 10px;\n"
                                          "}")
        self.confirm_button.setObjectName("confirm_button")
        self.horizontalLayout.addWidget(self.confirm_button)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem7)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.result_label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Rubik")
        font.setPointSize(9)
        self.result_label.setFont(font)
        self.result_label.setStyleSheet("QLabel{\n"
                                        "    color: #26bc1a;\n"
                                        "}")
        self.result_label.setText("")
        self.result_label.setAlignment(QtCore.Qt.AlignCenter)
        self.result_label.setObjectName("result_label")
        self.verticalLayout.addWidget(self.result_label)
        spacerItem8 = QtWidgets.QSpacerItem(20, 24, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem8)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem9)
        self.settings_button = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.settings_button.setFont(font)
        self.settings_button.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.settings_button.setStyleSheet("    QPushButton{\n"
                                           "    background: #46494d;\n"
                                           "    border: 2px solid #46494d;\n"
                                           "    border-radius: 13px;\n"
                                           "    padding: 2 7px;\n"
                                           "    padding-right: 10px;\n"
                                           "    transition: 0.25s;\n"
                                           "}\n"
                                           "\n"
                                           "QPushButton:hover{\n"
                                           "    background: #616366;\n"
                                           "    border: 2px solid #616366;\n"
                                           "}")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("data/ressources/gearwhite.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.settings_button.setIcon(icon1)
        self.settings_button.setIconSize(QtCore.QSize(16, 16))
        self.settings_button.setObjectName("settings_button")
        self.horizontalLayout_4.addWidget(self.settings_button)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 769, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Anime Presence"))
        self.title_label.setText(_translate("MainWindow", "Enter the url of the anime you are watching"))
        self.confirm_button.setText(_translate("MainWindow", "Confirm"))
        self.settings_button.setText(_translate("MainWindow", "Settings"))
