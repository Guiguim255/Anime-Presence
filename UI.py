from PyQt5 import QtCore, QtGui, QtWidgets
from data.ui.Widgets import AnimeScrollView, WebsiteComboBox, EpisodeComboBox

class MainWindow():

    def setupUi(self, MainWindow:QtWidgets.QMainWindow, theme, json):
        self.theme = theme
        self.MainWindow = MainWindow
        MainWindow.resize(800, 320)
        MainWindow.setMaximumSize(800, 320)
        font = QtGui.QFont()
        font.setFamily("Rubik")
        font.setPointSize(9)
        MainWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("data/ressources/letters.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setObjectName("MainWindow")

        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.logo_image = QtWidgets.QLabel(self.centralwidget)
        self.logo_image.setFixedSize(QtCore.QSize(80, 80))
        self.logo_image.setPixmap(QtGui.QPixmap("data/ressources/letters.png"))
        self.logo_image.setScaledContents(True)
        self.horizontalLayout_3.addWidget(self.logo_image)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.title_label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.title_label.setFont(font)
        self.horizontalLayout_3.addWidget(self.title_label)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        spacerItem2 = QtWidgets.QSpacerItem(20, 26, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)

        self.urlLayout = QtWidgets.QVBoxLayout()
        self.url_entry = QtWidgets.QLineEdit(self.centralwidget)
        self.urlLayout.addWidget(self.url_entry)
        self.url_entry.setMinimumSize(QtCore.QSize(400, 30))
        self.scrollView = AnimeScrollView(theme, json)
        self.MainWindow.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.choice = WebsiteComboBox(json, theme)
        self.urlLayout.addWidget(self.choice)
        self.choice.hide()
        self.episodeComboBox = EpisodeComboBox(json, theme)
        self.urlLayout.addWidget(self.episodeComboBox)
        self.episodeComboBox.hide()

        self.horizontalLayout_2.addLayout(self.urlLayout)

        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem5 = QtWidgets.QSpacerItem(20, 25, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem5)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem6)
        self.confirm_button = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        #font.setWeight(50)
        self.confirm_button.setFont(font)
        self.confirm_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.confirm_button.setMouseTracking(False)
        self.horizontalLayout.addWidget(self.confirm_button)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem7)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.result_label = QtWidgets.QLabel(self.centralwidget)
        self.result_label.setFont(font)
        self.result_label.setStyleSheet("QLabel{\n"
                                        "    color: #26bc1a;\n"
                                        "}")
        self.result_label.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.addWidget(self.result_label)
        spacerItem8 = QtWidgets.QSpacerItem(20, 24, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem8)
        self.horizontalLayout_4 = QtWidgets.QGridLayout()
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem9)
        self.settings_button = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.settings_button.setFont(font)
        self.horizontalLayout_4.addWidget(self.settings_button, 1, 1)

        self.web_button = QtWidgets.QPushButton(self.centralwidget)
        self.web_button.setFont(font)
        self.web_button.hide()
        self.web_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.MinimumExpanding)
        self.horizontalLayout_4.addWidget(self.web_button, 1, 0)
        self.verticalLayout.addLayout(self.horizontalLayout_4)

        MainWindow.setCentralWidget(self.centralwidget)

        self.setText(json)
        self.setTheme(self.theme)

    def setText(self, json):
        self.MainWindow.setWindowTitle(json["title"])
        self.title_label.setText(json["enter url"])
        self.confirm_button.setText(json["start"])
        self.settings_button.setText(json["settings"])
        self.url_entry.setPlaceholderText(json["enter url"])
        self.episodeComboBox.setText(json)
        self.web_button.setText(json.get("assets"))


    def setTheme(self, theme):
        self.theme = theme
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(f"data/ressources/gear{'white' if theme.name == 'dark' else ''}"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.settings_button.setIcon(icon)
        self.settings_button.setIconSize(QtCore.QSize(16, 16))
        self.MainWindow.setStyleSheet(
            f"QWidget#MainWindow{{background-color: {theme.mainBackgroundColor}; {'border-top: 2px solid #F0F0F0;' if theme.name == 'light' else ''}}}\n"
            f"*{{color: {theme.fontColor};}}\n"
            "")
        self.url_entry.setStyleSheet("QLineEdit{\n"
                                     f"    background: {theme.altBackgroundColor};\n"
                                     f"    border: 2px solid {theme.altBackgroundColor};\n"
                                     "    border-radius: 10px\n"
                                     "}")
        self.confirm_button.setStyleSheet("QPushButton{\n"
                                          f"    background: {theme.altBackgroundColor};\n"
                                          f"    border: 2px solid {theme.altBackgroundColor};\n"
                                          "    border-radius: 15px;\n"
                                          "    padding: 2 10px;\n"
                                          "}")

        self.settings_button.setStyleSheet("    QPushButton{\n"
                                           f"    background: {theme.mainBackgroundColor};\n"
                                           f"    border: 2px solid {theme.mainBackgroundColor};\n"
                                           "    border-radius: 13px;\n"
                                           "    padding: 2 7px;\n"
                                           "    padding-right: 10px;\n"
                                           "}\n"
                                           "\n"
                                           "QPushButton:hover{\n"
                                           f"    background: {theme.altBackgroundColor};\n"
                                           f"    border: 2px solid {theme.altBackgroundColor};\n"
                                           "}")
        self.web_button.setStyleSheet("    QPushButton{\n"
                                           f"    background: {theme.mainBackgroundColor};\n"
                                           f"    border: 2px solid {theme.mainBackgroundColor};\n"
                                           "    border-radius: 13px;\n"
                                           "    padding: 2 7px;\n"
                                           "    padding-right: 10px;\n"
                                           "}\n"
                                           "\n"
                                           "QPushButton:hover{\n"
                                           f"    background: {theme.altBackgroundColor};\n"
                                           f"    border: 2px solid {theme.altBackgroundColor};\n"
                                           "}")
        self.episodeComboBox.setTheme(theme)
