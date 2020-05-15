from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from data.ui.SettingsWindow import Ui_SettingsWindow

from pypresence import Presence, ServerError
import json


class Settings_UserInterface(QMainWindow, Ui_SettingsWindow):

    onClose = pyqtSignal(bool)

    def __init__(self):
        super(Settings_UserInterface, self).__init__()

        self.setupUi(self)

        self.test_presence = None

        self.closeBySave = False

        json_file = open("data/config.json", "r")
        self.config_json = json.load(json_file)
        json_file.close()

        json_file = open("data/translation.json", "r", encoding="UTF-8")
        self.translation = json.load(json_file)
        json_file.close()

        for language in self.translation:
            self.comboBox.addItem(self.translation[language]["name"])
        self.comboBox.setCurrentText(self.translation[self.config_json["user_language"]]["name"])

        if self.config_json["theme"] == "dark":
            self.checkBox.setChecked(True)
            self.checkBox_2.setChecked(False)
        else:
            self.checkBox.setChecked(False)
            self.checkBox_2.setChecked(True)

        if self.config_json["App_ID"] != "697842560844038225":
            self.checkBox_3.setChecked(True)
            self.lineEdit.setEnabled(True)
            self.lineEdit.setText(self.config_json["App_ID"])
        else:
            self.checkBox_3.setChecked(False)
            self.lineEdit.setEnabled(False)

        self.checkBox_3.stateChanged.connect(self.chehd)

        self.pushButton.clicked.connect(self.save_changes)

    def chehd(self):
        if self.checkBox_3.checkState():
            self.lineEdit.setEnabled(True)
        else:
            self.lineEdit.clear()
            self.lineEdit.setEnabled(False)

    def test_id(self):
        if not(self.lineEdit.text()):return False
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
                                    "    background: #616366;\n"
                                    "    border: 2px solid #bc1a26;\n"
                                    "}")
                return self.error_label.show()
        else:
            self.config_json["App_ID"] = "697842560844038225"

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
        self.lineEdit.setStyleSheet("QLineEdit{\n"
                                    "    background: #616366;\n"
                                    "    border: 2px solid #616366;\n"
                                    "}")
        if self.test_presence:
            self.test_presence.close()
        self.onClose.emit(self.closeBySave)
