from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SettingsWindow(object):
    def setupUi(self, MainWindow, theme, json):
        self.MainWindow = MainWindow
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
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setStyleSheet("QPushButton{color:white;\n"
                                      "    background: #4cc321;\n"
                                      "    border: 2px solid #4cc321;\n"
                                      "    border-radius: 15px;\n"
                                      "    padding: 2 10px;\n"
                                      "}")
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
        self.error_label.setAlignment(QtCore.Qt.AlignCenter)
        self.error_label.setObjectName("result_label")
        self.verticalLayout.addWidget(self.error_label)
        self.error_label.hide()
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem5)
        MainWindow.setCentralWidget(self.centralwidget)

        self.theme = theme
        self.setTheme(self.theme)
        self.setText(json)

    def setText(self, json):
        self.MainWindow.setWindowTitle(f"{json['title']} - {json['settings']}")
        self.groupBox.setTitle(json["language"].upper())
        self.groupBox_2.setTitle(json["theme"].upper())
        self.checkBox.setText(json["dark"])
        self.checkBox_2.setText(json["light"])
        self.groupBox_3.setTitle(json["personal application"].upper())
        self.checkBox_3.setText(json["personal app id"])
        self.pushButton.setText(json["save"])
        self.error_label.setText(json["error"])

    def setTheme(self, theme):
        self.theme = theme
        self.MainWindow.setStyleSheet(f"QMainWindow{{background-color: {self.theme.mainBackgroundColor};\n"
                                          f"color: {self.theme.fontColor}; {'border-top: 2px solid #F0F0F0' if self.theme.name == 'light' else ''}}}"
                                      f"QAbstractItemView {{border: 1px solid {theme.fontColor}; color: {self.theme.fontColor}; background-color: "
                                      f"{self.theme.altBackgroundColor};selection-background-color: #FF0000; outline: 0px;}}"
                                      )
        self.comboBox.setStyleSheet(
            f"QComboBox {{color: {self.theme.fontColor};background: {self.theme.altBackgroundColor};padding: 0px 0px 0px 0px; border: 1px solid {self.theme.mainBackgroundColor};border-radius: "
            "3px;}QComboBox::drop-down{width: 30px;border-left-width: 1px;border-left-color: "
            f"{theme.mainBackgroundColor};border-left-style: {self.theme.fontColor} solid;}}QComboBox::down-arrow{{image: url("
            f"data/ressources/expand{'white' if self.theme.name == 'dark' else ''}.png);width: 16px;height: 16px;}}")
        view = QtWidgets.QListView(self.comboBox)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setFamily("Rubik")
        view.setStyleSheet(f""" 
                                 QListView::item:selected {{                 
                                 color: {self.theme.fontColor};
                                 background-color: {self.theme.mainBackgroundColor}}}""")
        view.setFont(font)
        self.comboBox.setView(view)

        self.groupBox_2.setStyleSheet(f"color:{self.theme.fontColor};")
        self.groupBox.setStyleSheet(f"color:{self.theme.fontColor};")
        self.groupBox_3.setStyleSheet(f"color:{self.theme.fontColor};")
        self.lineEdit.setStyleSheet("QLineEdit{\n"
                                                   f"    background: {self.theme.altBackgroundColor};\n"
                                                   f"    border: 2px solid {self.theme.mainBackgroundColor};\n"
                                                   "}")
