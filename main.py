from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import pyqtSlot
from data.ui.Theme import Theme
from data.ui.Widgets import Fetcher
from UI import MainWindow
from anime_infos import AnimeInfos
from SettingsQt import Settings_UserInterface
from pypresence import Presence
import json
import time
import sys
import os.path


class UserInterface(QMainWindow, MainWindow):
    languageChanged = pyqtSlot(str)
    themeChanged = pyqtSlot(str)

    def __init__(self):
        super(UserInterface, self).__init__()

        print("Loading languages...")
        with open("data/translation.json", "r", encoding = "UTF-8") as json_file:
            self.translation = json.load(json_file)

        print("Loading configuration...")
        if os.path.isfile("data/config.json"):
            with open("data/config.json", "r") as json_file:
                self.config_json = json.load(json_file)
        else:
            print("Creating configuration...")
            with open("data/default_config.json", "r") as json_file:
                default_config = json_file.read()
                with open("data/config.json", "w") as new_config:
                    new_config.write(default_config)
                self.config_json = json.loads(default_config)

        self.language = self.config_json["user_language"]
        self.theme = Theme.get_theme(self.config_json["theme"])
        self.l_format = self.translation[self.language]["format"]

        print("Setting up the window and loading configuration...")
        self.setupUi(self, self.theme, self.translation[self.language])

        print("Loading settings window...")
        self.settingsWindow = Settings_UserInterface(self.theme, self.translation[self.language])
        self.settings_button.clicked.connect(self.openSettings)
        self.settingsWindow.onClose.connect(self.onSettingsClosed)
        self.settingsWindow.themeChanged.connect(self.setAllThemes)
        self.settingsWindow.languageChanged.connect(self.setAllTexts)

        print("Initializing the presence...")
        client_id = self.config_json["App_ID"]
        self.RPC = Presence(client_id)
        print("Connecting...")
        self.RPC.connect()
        print("Ready")

        self.isRunning = False
        self.infos = {}
        self.episode = 0
        self.currentAnime = None

        self.confirm_button.clicked.connect(self.on_confirm_button_clicked)
        self.scrollView.clicked.connect(self.onLabelClick)
        self.urlLayout.addWidget(self.scrollView)
        self.url_entry.focusOutEvent = lambda event: self.handleFocus("exit")
        self.url_entry.focusInEvent = lambda event: self.handleFocus("enter")
        self.url_entry.textEdited.connect(self.onEdit)
        self.scrollView.hide()
        self.fetcher = None
        self.spinbox.textFromValue = lambda x: f"{self.translation[self.language]['episode'].title()} {x}"
        self.spinbox.setMinimum(1)
        self.spinbox.valueChanged.connect(self.update_episode)

    @pyqtSlot(str)
    def setAllTexts(self, language):
        lang = ""
        for l in self.translation:
            if self.translation[l]["name"] == language:
                lang = l
        if lang != self.language:
            print("Changing")
            self.language = lang
            self.setText(self.translation[self.language])
            self.settingsWindow.setText(self.translation[self.language])
            self.choice.setText(self.translation[self.language])

    @pyqtSlot(str)
    def setAllThemes(self, themeName):
        if themeName != self.theme.name:
            self.theme = Theme.get_theme(themeName)
            self.setTheme(self.theme)
            self.settingsWindow.setTheme(self.theme)
            self.scrollView.setTheme(self.theme)
            self.choice.setTheme(self.theme)

    def update_episode(self):
        self.episode = self.spinbox.value()

    def on_confirm_button_clicked(self):
        text = self.url_entry.text()
        buttonText = self.confirm_button.text()
        if buttonText == self.translation[self.language]["start"]:
            if text:
                self.confirm_button.setText(self.translation[self.language]["stop"])
                if text.startswith("http") or text.startswith("www"):
                    self.get_presence(text, "url")
                    self.result_label.setStyleSheet("QLabel{color: #26bc1a;}")
                else:
                    self.get_presence(text, "name")
                self.result_label.setText(self.translation[self.language]["updated presence"])
        else:
            self.result_label.clear()
            self.RPC.clear()
            self.confirm_button.setText(self.translation[self.language]["start"])

            """else:
                self.result_label.setStyleSheet("QLabel{color: #bc1a26;}")
                self.result_label.setText("Invalid url")"""

    def onLabelClick(self, anime):
        self.url_entry.setText(anime.title)
        self.urlLabel = anime.title
        self.maxEpisode = int(anime.episodes)
        if self.maxEpisode > 1:
            self.spinbox.show()
            self.spinbox.setMaximum(anime.episodes)
        self.scrollView.hide()
        self.choice.show()
        self.confirm_button.show()
        self.currentAnime = anime

    def handleFocus(self, event):
        if event == "enter":
            self.choice.hide()
            self.spinbox.hide()
            if self.scrollView.animeLabels:
                self.scrollView.show()
                self.confirm_button.hide()
        else:
            if not self.scrollView.hasFocus():
                self.scrollView.hide()
                self.confirm_button.show()
            if not (self.url_entry.text().startswith("http") or self.url_entry.text().startswith(
                    "www")) and not self.scrollView.isVisible() and self.url_entry.text():
                self.choice.show()
                self.spinbox.show()

    def onEdit(self, query):
        self.choice.hide()
        self.spinbox.hide()
        if not (query.startswith("http") or query.startswith("www")):
            if not self.isRunning:
                self.isRunning = True
                self.fetcher = Fetcher(query)
                self.fetcher.finished.connect(self.f)
                self.fetcher.finished.connect(self.scrollView.fill)
                self.fetcher.start()
            else:
                self.fetcher.terminate()
                self.isRunning = False
                return self.onEdit(query)
        else:
            self.confirm_button.show()
            self.scrollView.hide()

    def f(self, x):
        self.isRunning = False

    def generate_state(self, lFormat, infos):
        episode, ep_nb, saison, s_nb = "", "", "", ""
        if infos.get("s_nb", "0") not in ("0", "1"):
            saison = self.translation[self.language]['saison'].capitalize()
            s_nb = infos['s_nb']
        if infos.get("ep_nb", "0") != "0":
            episode = self.translation[self.language]['episode'].capitalize()
            ep_nb = infos['ep_nb']
        return lFormat.format(saison=saison, s_nb=s_nb, episode=episode, ep_nb=ep_nb)

    def openSettings(self):
        self.hide()
        self.settingsWindow.show()
        self.settingsWindow.closeBySave = False

    def onSettingsClosed(self, var):
        if var:
            self.show()
        else:
            self.close()

    def get_presence(self, text, Type):
        if Type == "url":
            thread = AnimeInfos(text, Type, parent=self)
            thread.infos.connect(self.update_presence)
            thread.start()
        else:
            website = ["", ["adn_logo", "Anime Digital Network"], ["crunchyroll_logo", "Crunchyroll"], ["wakanim_logo", "Wakanim"], ""][self.choice.currentIndex()]
            infos = {"ep_nb": str(self.episode), "s_nb": "0", "anime_name": self.currentAnime.title, "website": website,
                     "image": [str(self.currentAnime.id), f"{self.currentAnime.romaji} ({self.currentAnime.released_date}), {self.currentAnime.episodes} episodes"]}
            self.update_presence(infos)

    def update_presence(self, infos):
        params = {"start": time.time(),
                  "details": f"{self.translation[self.language]['watching']} {infos['anime_name']}",
                  "state": self.generate_state(self.l_format, infos)}

        response = self.RPC.update(**{"large_image": infos["image"][0]})
        if response["data"]["assets"].get("large_image"):
            params["large_image"], params["large_text"] = infos["image"]
            if infos["website"]:
                params["small_image"], params["small_text"] = infos["website"]
        else:
            if infos["website"]:
                params["large_image"] = infos["website"][0]
                params["large_text"] = infos["image"][1]

        self.RPC.update(**params)

    @pyqtSlot()
    def closeEvent(self, event):
        self.RPC.close()
        event.accept()


app = QApplication(sys.argv)
win = UserInterface()
win.show()
app.exec_()
