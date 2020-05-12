from PyQt5.QtWidgets import QMainWindow, QCompleter, QComboBox
from PyQt5.QtCore import pyqtSlot, QUrl, Qt, QStringListModel
from AnimeLabel import AnimeScrollView, Fetcher
from Ui_AnimePresence_MainWindow import Ui_MainWindow
from pypresence import Presence
import json
from time import time
from anime_infos import getAnimeInfos
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests


class UserInterface(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(UserInterface, self).__init__()

        self.setupUi(self)

        json_file = open("data/config.json", "r")
        self.config_json = json.load(json_file)
        json_file.close()

        json_file = open("data/translation.json", "r", encoding="UTF-8")
        self.translation = json.load(json_file)
        json_file.close()

        client_id = self.config_json["App_ID"]  # You can put your own app ID
        self.RPC = Presence(client_id)  # Initialize the client class
        self.RPC.connect()  # Start the handshake loop

        self.language = self.config_json["user_language"]
        self.l_format = self.translation[self.language]["format"]
        self.isRunning = False
        self.infos = {}

        self.confirm_button.clicked.connect(self.on_confirm_button_clicked)


        self.scrollView = AnimeScrollView()
        self.setFocusPolicy(Qt.StrongFocus)
        self.scrollView.clicked.connect(self.onLabelClick)
        self.urlLayout.addWidget(self.scrollView)
        self.url_entry.focusOutEvent = lambda event: self.handleFocus("exit")
        self.url_entry.setPlaceholderText("Enter the name or the URL of the anime you're watching")
        self.url_entry.focusInEvent = lambda event: self.handleFocus("enter")
        self.url_entry.textEdited.connect(self.onEdit)
        self.scrollView.hide()
        self.fetcher = None

        self.choice = WebsiteComboBox()
        self.urlLayout.addWidget(self.choice)
        self.choice.hide()

    def on_confirm_button_clicked(self):
        texte = self.url_entry.text()
        if texte:
            if urlparse(texte)[0]:
                self.update_presence(texte, "url")
                self.result_label.setStyleSheet("QLabel{color: #26bc1a;}")
            else:
                self.update_presence(texte, "name")
            self.result_label.setText(self.translation[self.language]["updated presence"])

            """else:
                self.result_label.setStyleSheet("QLabel{color: #bc1a26;}")
                self.result_label.setText("Invalid url")"""

            #self.url_entry.clear()

    def onLabelClick(self, text):
        self.url_entry.setText(text)
        self.scrollView.hide()
        self.choice.show()
        self.confirm_button.show()

    def handleFocus(self, event):
        if event == "enter":
            self.choice.hide()
            if self.scrollView.animeLabels:
                self.scrollView.show()
                self.confirm_button.hide()
        else:
            if not self.scrollView.hasFocus():
                self.scrollView.hide()
                self.confirm_button.show()
            if not (self.url_entry.text().startswith("http") or self.url_entry.text().startswith("www")):
                self.choice.show()

    def onEdit(self, query):
        self.choice.hide()
        if not(query.startswith("http") or query.startswith("www")):
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
        nStr = lFormat
        nStr = nStr.replace("anime_name", infos["anime_name"])
        if infos["ep_nb"] == "0":
            nStr = nStr[:len(infos["anime_name"])]
            return nStr
        if infos["s_nb"] == "0":
            nStr = nStr.replace("ep_nb", infos["ep_nb"])
            nStr = nStr.replace(" saison s_nb", "")
            return nStr
        nStr = nStr.replace("s_nb", infos["s_nb"]).replace("ep_nb", infos["ep_nb"])
        return nStr



    def update_presence(self, text, type):
        if type == "url":
            infos = getAnimeInfos(text)
        else:
            website = ["", "adn", "crunchyroll","wakanim",""][self.choice.currentIndex()]
            infos = {"ep_nb":"0","s_nb":"0","anime_name":text, "website":"","image":"", "small_image":""}
            if website:
                infos["image"] = website + "_logo"
        state = self.generate_state(self.l_format, infos)
        self.actual_epoch = time()
        if infos["small_image"] and infos["image"]:
            self.RPC.update(details=self.translation[self.language]["watching an anime"], state=state,
                            large_image=infos["image"],
                            small_image=infos["small_image"],
                            start=self.actual_epoch)
        elif infos["image"]:
            self.RPC.update(details=self.translation[self.language]["watching an anime"], state=state,
                            large_image=infos["image"],
                            start=self.actual_epoch)
        else:
            self.RPC.update(details=self.translation[self.language]["watching an anime"], state=state,
                            start=self.actual_epoch)


    @pyqtSlot()
    def closeEvent(self, event):
        self.RPC.close()
        event.accept()

class WebsiteComboBox(QComboBox):
    def __init__(self):
        super(WebsiteComboBox, self).__init__()
        self.insertItem(0, "Sélectionner le site sur lequel vous regardez un anime (optionnel)")
        self.insertItem(1, "Anime Digital Network")
        self.insertItem(2, "Crunchyroll")
        self.insertItem(3, "Wakanim")
        self.insertItem(4, "Autre")
        self.model().item(0).setEnabled(False)

