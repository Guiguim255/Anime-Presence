from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtGui import  QStandardItemModel, QStandardItem
from data.ui.SettingsWindow import Ui_SettingsWindow

from pypresence import Presence, ServerError
import json

ORIGINAL_APP_ID = "697842560844038225"

class Settings_UserInterface(QMainWindow, Ui_SettingsWindow):
    onClose = pyqtSignal(bool)
    languageChanged = pyqtSignal(str)
    themeChanged = pyqtSignal(str)

    def __init__(self, theme, tr):
        super(Settings_UserInterface, self).__init__()

        self.theme = theme
        self.tr = tr
        self.setupUi(self, self.theme, self.tr)

        self.test_presence = None

        self.closeBySave = False

        json_file = open("data/config.json", "r")
        self.config_json = json.load(json_file)
        json_file.close()

        json_file = open("data/translation.json", "r", encoding="UTF-8")
        self.translation = json.load(json_file)
        json_file.close()

        self.language = self.config_json["user_language"]

        for language in sorted(self.translation):
            self.comboBox.addItem(self.translation[language]["name"], language)
        self.comboBox.setCurrentText(self.translation[self.config_json["user_language"]]["name"])


        if self.config_json["theme"] == "dark":
            self.checkBox.setChecked(True)
            self.checkBox_2.setChecked(False)
        else:
            self.checkBox.setChecked(False)
            self.checkBox_2.setChecked(True)

        if self.config_json["App_ID"] != ORIGINAL_APP_ID:
            self.checkBox_3.setChecked(True)
            self.lineEdit.setEnabled(True)
            self.lineEdit.setText(self.config_json["App_ID"])
        else:
            self.checkBox_3.setChecked(False)
            self.lineEdit.setEnabled(False)

        self.checkBox_3.stateChanged.connect(self.chehd)
        self.comboBox.currentTextChanged.connect(self.onLangageChanged)
        self.pushButton.clicked.connect(self.save_changes)

    def chehd(self):
        if self.checkBox_3.checkState():
            self.lineEdit.setEnabled(True)
        else:
            self.lineEdit.clear()
            self.lineEdit.setEnabled(False)

    def onLangageChanged(self, value):
        for language in self.translation:
            if language == value:
                self.languageChanged.emit(language)


    def test_id(self):
        if not (self.lineEdit.text()):
            return False
        try:
            self.test_presence = Presence(self.lineEdit.text())
            self.test_presence.connect()
            self.test_presence.update(state="woa")
            self.test_presence.close()
            return True
        except ServerError:
            return False

    def save_changes(self):
        if self.checkBox_3.checkState():
            if self.test_id():
                self.config_json["App_ID"] = self.lineEdit.text()
            else:
                self.lineEdit.setStyleSheet("QLineEdit{\n"
                                            f"    background: {self.theme.mainBackgroundColor};\n"
                                            "    border: 2px solid #bc1a26;\n"
                                            "}")
                return self.error_label.show()
        else:
            self.config_json["App_ID"] = ORIGINAL_APP_ID

        for language in self.translation:
            if self.translation[language]["name"] == self.comboBox.currentText():
                self.config_json["user_language"] = language
                break

        if self.checkBox.checkState():
            self.config_json["theme"] = "dark"
        else:
            self.config_json["theme"] = "light"

        with open("data/config.json", "w") as f:
            f.write(json.dumps(self.config_json))
        self.closeBySave = True
        self.close()

    @pyqtSlot()
    def closeEvent(self, event):
        if self.test_presence:
            self.test_presence.close()
        self.onClose.emit(self.closeBySave)
        if self.closeBySave:
            self.languageChanged.emit(self.comboBox.currentText())
            self.themeChanged.emit("dark" if self.checkBox.checkState() else "light")