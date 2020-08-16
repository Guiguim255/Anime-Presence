from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from data.ui.SettingsWindow import Ui_SettingsWindow

from pypresence import Presence, InvalidID
import struct
import json

ORIGINAL_APP_ID = "697842560844038225"


class Settings_UserInterface(QMainWindow, Ui_SettingsWindow):
    onClose = pyqtSignal(bool)
    language_changed = pyqtSignal(str)
    theme_changed = pyqtSignal(str)
    presence_change = pyqtSignal(Presence)

    def __init__(self, theme, translation, presence, config):
        super(Settings_UserInterface, self).__init__()

        self.theme = theme
        self.translation = translation
        self.presence = presence
        self.config = config
        self.setupUi(self, self.theme, self.translation[self.config["user_language"]])

        self.test_presence = None

        self.closeBySave = False
        self.id_changed = False

        for language in sorted(self.translation):
            self.comboBox.addItem(self.translation[language]["name"], language)
        self.comboBox.setCurrentText(self.translation[self.config["user_language"]]["name"])

        if self.config["theme"] == "dark":
            self.checkBox.setChecked(True)
            self.checkBox_2.setChecked(False)
        else:
            self.checkBox.setChecked(False)
            self.checkBox_2.setChecked(True)

        if self.config["App_ID"] != ORIGINAL_APP_ID:
            self.checkBox_3.setChecked(True)
            self.lineEdit.setEnabled(True)
            self.lineEdit.setText(self.config["App_ID"])
        else:
            self.checkBox_3.setChecked(False)
            self.lineEdit.setEnabled(False)

        self.checkBox_3.stateChanged.connect(self.check)
        self.comboBox.currentTextChanged.connect(self.onLangageChanged)
        self.pushButton.clicked.connect(self.save_changes)

    def check(self):
        if self.checkBox_3.checkState():
            self.lineEdit.setEnabled(True)
        else:
            self.lineEdit.clear()
            self.lineEdit.setEnabled(False)

    def onLangageChanged(self, value):
        for language in self.translation:
            if language == value:
                self.language_changed.emit(language)

    def test_id(self):
        try:
            self.test_presence = Presence(self.lineEdit.text())
            self.test_presence.connect()
            self.test_presence.update(state="woa")
            self.test_presence.close()
            return True
        except (InvalidID, struct.error):
            return False

    def save_changes(self):
        new_id = self.lineEdit.text() if self.checkBox_3.checkState() else ORIGINAL_APP_ID
        if self.presence.client_id != new_id:

            if self.warning_message.exec_() != 1024:
                return

            self.presence.close()

            if self.checkBox_3.checkState():
                if self.test_id():
                    self.config["App_ID"] = new_id
                else:
                    self.lineEdit.setStyleSheet("QLineEdit{"
                                                f"background: {self.theme.altBackgroundColor};"
                                                "border: 2px solid #bc1a26;}")
                    return self.error_label.show()
            else:
                self.config["App_ID"] = new_id
            self.id_changed = True
            self.presence = Presence(new_id)

        for language in self.translation:
            if self.translation[language]["name"] == self.comboBox.currentText():
                self.config["user_language"] = language
                break

        if self.checkBox.checkState():
            self.config["theme"] = "dark"
        else:
            self.config["theme"] = "light"

        with open("data/config.json", "w") as f:
            f.write(json.dumps(self.config))
        self.closeBySave = True
        self.close()

    @pyqtSlot()
    def closeEvent(self, event):
        self.onClose.emit(self.closeBySave)
        if self.closeBySave:
            self.error_label.hide()
            self.lineEdit.setStyleSheet("QLineEdit{"
                                        f"background: {self.theme.altBackgroundColor};"
                                        f"border: 2px solid {self.theme.mainBackgroundColor};\n"
                                        "}")
            self.language_changed.emit(self.comboBox.currentText())
            self.theme_changed.emit("dark" if self.checkBox.checkState() else "light")
            if self.id_changed:
                self.presence_change.emit(self.presence)
