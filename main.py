from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import pyqtSlot
from data.ui.Theme import Theme
from data.ui.Network import Fetcher
from UI import MainWindow
from pypresence import Presence
import json
import time
from SettingsQt import Settings_UserInterface, ORIGINAL_APP_ID
import sys
import os.path
import webbrowser


class UserInterface(QMainWindow, MainWindow):
    languageChanged = pyqtSlot(str)
    themeChanged = pyqtSlot(str)

    def __init__(self):
        super(UserInterface, self).__init__()

        print("Loading languages...")
        with open("data/translation.json", "r", encoding="UTF-8") as json_file:
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

        print("Initializing the presence...")
        client_id = self.config_json["App_ID"]
        self.RPC = Presence(client_id)
        print("Connecting...")
        self.RPC.connect()

        print("Loading settings window...")
        self.settingsWindow = Settings_UserInterface(self.theme, self.translation[self.language], self.RPC)
        self.settings_button.clicked.connect(self.openSettings)
        self.settingsWindow.onClose.connect(self.onSettingsClosed)
        self.settingsWindow.theme_changed.connect(self.setAllThemes)
        self.settingsWindow.language_changed.connect(self.setAllTexts)
        self.settingsWindow.presence_change.connect(self.set_id)

        print("Ready")

        self.episode = 0
        self.currentAnime = None

        self.confirm_button.clicked.connect(self.on_confirm_button_clicked)
        self.scrollView.clicked.connect(self.onLabelClick)
        self.urlLayout.addWidget(self.scrollView)
        self.web_button.clicked.connect(lambda event: webbrowser.open(f"https://discord.com/developers/applications/{self.config_json['App_ID']}/rich-presence/assets"))
        if self.config_json['App_ID'] != ORIGINAL_APP_ID:
            self.web_button.show()
        self.url_entry.focusOutEvent = lambda event: self.handleFocus("exit")
        self.url_entry.focusInEvent = lambda event: self.handleFocus("enter")
        self.url_entry.textEdited.connect(self.onEdit)
        self.scrollView.hide()
        self.fetcher = None

    @pyqtSlot(str)
    def setAllTexts(self, language):
        lang = ""
        for i in self.translation:
            if self.translation[i]["name"] == language:
                lang = i
                break
        if lang != self.language:
            self.language = lang
            self.setText(self.translation[self.language])
            self.settingsWindow.setText(self.translation[self.language])
            self.settingsWindow.warning_message.changeText(self.translation[self.language])
            self.choice.setText(self.translation[self.language])
            self.scrollView.setText(self.translation[self.language])

    @pyqtSlot(str)
    def setAllThemes(self, theme_name):
        if theme_name != self.theme.name:
            self.theme = Theme.get_theme(theme_name)
            self.setTheme(self.theme)
            self.settingsWindow.setTheme(self.theme)
            self.scrollView.setTheme(self.theme)
            self.choice.setTheme(self.theme)

    def set_id(self, presence):
        self.RPC = presence
        self.RPC.connect()
        self.result_label.clear()
        self.confirm_button.setText(self.translation[self.language]["start"])
        if self.RPC.client_id == ORIGINAL_APP_ID:
            self.web_button.hide()
        else:
            self.web_button.clicked.disconnect()
            self.web_button.clicked.connect(lambda event: webbrowser.open(
                f"https://discord.com/developers/applications/{self.RPC.client_id}/rich-presence/assets"))
            self.web_button.show()

    def on_confirm_button_clicked(self):
        button_text = self.confirm_button.text()
        if button_text == self.translation[self.language]["start"]:
            if self.currentAnime:
                self.confirm_button.setText(self.translation[self.language]["stop"])
                self.get_presence()
                self.result_label.setText(self.translation[self.language]["updated presence"])
        else:
            self.result_label.clear()
            self.RPC.clear()
            self.confirm_button.setText(self.translation[self.language]["start"])

    def onLabelClick(self, anime):
        self.url_entry.setText(anime.title)
        self.urlLabel = anime.title
        self.currentAnime = anime
        if anime.episodes > 1:
            self.episodeComboBox.show()
            self.episodeComboBox.init(anime.episodes)
            if self.episode and self.episode <= anime.episodes:
                self.episodeComboBox.combo.setCurrentIndex(self.episode - 1)
        self.episode = 0
        self.scrollView.hide()
        self.choice.show()
        self.confirm_button.show()

    def handleFocus(self, event):
        if event == "enter":
            self.choice.hide()
            self.episodeComboBox.hide()
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
                self.episodeComboBox.show()

    def onEdit(self, query):
        if query.strip():
            self.choice.hide()
            self.episodeComboBox.hide()
            if not (query.startswith("http") or query.startswith("www")):
                self.fetcher = Fetcher()
                self.fetcher.finished.connect(self.scrollView.fill)
                self.fetcher.error.connect(self.scrollView.onError)
                self.fetcher.run(query, 10)
            else:
                self.fetcher = Fetcher()
                self.fetcher.error.connect(self.scrollView.onError)
                self.fetcher.urlParsed.connect(self.handleUrl)
                self.fetcher.parse_url(query)
        else:
            self.scrollView.hide()
            self.choice.show()
            self.episodeComboBox.show()

    @pyqtSlot(str, int, str)
    def handleUrl(self, title, episode, website):
        self.choice.setCurrentIndex(["animedigitalnetwork.fr", "www.crunchyroll.com", "www.wakanim.tv"].index(website))
        self.episode = episode
        self.onEdit(title)

    def generate_state(self, lang_format, infos):
        episode, ep_nb, saison, s_nb = "", "", "", ""
        if infos.get("s_nb", "0") not in ("0", "1"):
            saison = self.translation[self.language]['saison'].capitalize()
            s_nb = infos['s_nb']
        if infos.get("ep_nb", "0") != "0":
            episode = self.translation[self.language]['episode'].capitalize()
            ep_nb = infos['ep_nb']
        return lang_format.format(saison=saison, s_nb=s_nb, episode=episode, ep_nb=ep_nb)

    def openSettings(self):
        self.hide()
        self.settingsWindow.show()
        self.settingsWindow.closeBySave = False

    def onSettingsClosed(self, var):
        if var:
            self.show()
        else:
            self.close()

    def get_presence(self):
        website = [["adn_logo", "Anime Digital Network"], ["crunchyroll_logo", "Crunchyroll"], ["wakanim_logo", "Wakanim"], ""][self.choice.currentIndex()]
        infos = {"ep_nb": str(self.episodeComboBox.counter), "s_nb": "0", "anime_name": self.currentAnime.title, "website": website,
                 "image": [str(self.currentAnime.id), f"{self.currentAnime.romajiTitle} ({self.currentAnime.seasonYear}), {self.currentAnime.episodes} episodes"]}
        self.update_presence(infos)

    def update_presence(self, infos):
        params = {"start": int(time.time()),
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
