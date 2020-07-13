from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QScrollArea, QVBoxLayout, QSizePolicy, QSpinBox, QComboBox
from PyQt5.QtGui import QPixmap, QPalette, QColor
from PyQt5.QtCore import Qt, pyqtSignal, QThread
from itertools import zip_longest
import asyncio
import aiohttp
from bs4 import BeautifulSoup

class Anime:

    def __init__(self, urlImage, mainTitle, note, type_, epNb, releasedDate, altTitle):
        self.mainTitle = mainTitle
        self.urlImage = urlImage
        self.type = type_
        self.epNb = epNb
        self.releasedDate = releasedDate
        self.note = note
        self.dataImage = None
        self.altTitle = altTitle

    def setData(self, data):
        self.dataImage = data


class AnimeScrollView(QScrollArea):
    clicked = pyqtSignal(Anime)

    def __init__(self, theme):
        super(AnimeScrollView, self).__init__()

        self.setObjectName("AnimeScrollView")
        self.fontColor = ""
        self.mainBackgroundColor = ""
        self.altBackgroundColor = ""


        self.widget = QWidget()
        self.animeLabels = []
        self.layout = QVBoxLayout(self.widget)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidget(self.widget)
        self.setWidgetResizable(True)
        self.setGeometry(0, 0, 400, 142)
        self.setFixedHeight(142)
        self.verticalScrollBar().setSingleStep(142)
        self.hide()

        self.theme = theme
        self.setTheme(theme)

    def setTheme(self, theme):
        self.theme = theme
        self.setStyleSheet(f"QWidget#AnimeScrollView{{background-color:{theme.mainBackgroundColor};}}")
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(theme.mainBackgroundColor))
        self.setAutoFillBackground(True)
        self.setPalette(palette)
        for animeLabel in self.animeLabels:
            animeLabel.setTheme(theme)

    def fill(self, animes):
        for i in reversed(range(self.layout.count())):
            layoutToRemove = self.layout.itemAt(i).layout()
            for t in reversed(range(layoutToRemove.count())):
                widgetToRemove = layoutToRemove.itemAt(t).widget()
                layoutToRemove.removeWidget(widgetToRemove)
                widgetToRemove.setParent(None)
            self.layout.removeItem(layoutToRemove)
            layoutToRemove.setParent(None)
        self.animeLabels.clear()
        for pair in zip_longest(animes[::2], animes[1::2]):
            layout = QHBoxLayout(self.widget)
            self.animeLabels.append(AnimeLabel(pair[0], self.theme))
            self.animeLabels[-1].labelClicked.connect(self.onClick)
            layout.addWidget(self.animeLabels[-1])
            if pair[1] is not None:
                self.animeLabels.append(AnimeLabel(pair[1], self.theme))
                layout.addWidget(self.animeLabels[-1])
                self.animeLabels[-1].labelClicked.connect(self.onClick)
            self.layout.addLayout(layout)
        self.show()
        if not animes:
            self.hide()

    def onClick(self, anime):
        self.clicked.emit(anime)


class AnimeLabel(QWidget):
    labelClicked = pyqtSignal(Anime)

    def __init__(self, anime: Anime, theme):
        super(AnimeLabel, self).__init__()

        self.setAutoFillBackground(True)
        self.setFixedHeight(71)

        self.anime = anime
        self.theme = theme

        self.layout = QHBoxLayout()

        self.image = QPixmap()
        self.image.loadFromData(self.anime.dataImage)
        self.image = self.image.scaledToHeight(50, Qt.SmoothTransformation)
        self.imLabel = QLabel()
        self.imLabel.setPixmap(self.image)
        self.imLabel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)

        self.titleLabel = QLabel(self)
        self.titleLabel.setWordWrap(True)
        self.titleLabel.setTextFormat(Qt.RichText)
        title = self.anime.mainTitle
        if len(title) > 48:
            title = title[:46] + "..."
        self.titleLabel.setText(
            f"""<html><body><p align="center"><b>{title}</b></p></body></html>""")
        self.titleLabel.setAlignment(Qt.AlignVCenter)

        self.layout.addWidget(self.imLabel)
        self.layout.addWidget(self.titleLabel)
        self.setLayout(self.layout)

        self.setTheme(self.theme)

    def setTheme(self, theme):
        self.theme = theme
        color, bgColor = 'black' if self.theme.name == 'light' else 'white', 'white' if self.theme.name == 'light' else 'black'
        self.setStyleSheet(f"QToolTip{{background-color:{bgColor};color:{color};border: 1px solid {color}}}")
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(theme.mainBackgroundColor))
        self.setPalette(palette)
        if len(self.anime.mainTitle) > 48:
            self.setToolTip(f"<p style='white-space:pre'>{self.anime.mainTitle} ({self.anime.releasedDate})</p>")
        elif self.anime.altTitle:
            self.setToolTip(f"<p style='white-space:pre'>{self.anime.altTitle} ({self.anime.releasedDate})</p>")

    def mousePressEvent(self, event) -> None:
        self.labelClicked.emit(self.anime)

    def leaveEvent(self, event):
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(self.theme.mainBackgroundColor))
        self.setPalette(palette)

    def enterEvent(self, event):
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(self.theme.altBackgroundColor))
        self.setPalette(palette)

class WebsiteComboBox(QComboBox):
    def __init__(self, translate, theme):
        super(WebsiteComboBox, self).__init__()
        self.insertItem(0, " ")
        self.insertItem(1, "Anime Digital Network")
        self.insertItem(2, "Crunchyroll")
        self.insertItem(3, "Wakanim")
        self.insertItem(4, translate["other"])
        self.json = translate
        self.theme = theme
        self.setTheme(self.theme)
        self.setText(self.json)

    def setTheme(self, theme):
        self.theme = theme
        self.setStyleSheet(
            f"QComboBox {{background: {theme.mainBackgroundColor};border: 1px solid {theme.mainBackgroundColor};border-radius: "
            "3px;}QComboBox::drop-down{width: 30px;border-left-width: 1px;border-left-color: "
            f"{theme.mainBackgroundColor};border-left-style: solid;}}QComboBox::down-arrow{{image: url("
            f"data/ressources/expand{'white' if theme.name == 'dark' else ''}.png);width: 16px;height: 16px;}}"
            f"QComboBox QAbstractItemView {{border: 2px solid {theme.mainBackgroundColor}; color: {theme.fontColor}; background-color: "
            f"{theme.mainBackgroundColor};selection-background-color: {theme.altBackgroundColor}; selection-border: 2px solid {theme.fontColor};outline: "
            "0px;}")

    def setText(self, json):
        self.json = json
        self.removeItem(0)
        self.insertItem(0, self.json["select website"])
        self.model().item(0).setEnabled(False)



class EpisodeBox(QSpinBox):

    def __init__(self, min, max):
        super(EpisodeBox, self).__init__()
        self.lineEdit().setPlaceholderText("Episode")
        self.setMinimum(min)
        self.setMaximum(max)

class Fetcher(QThread):
    finished = pyqtSignal(list)

    def __init__(self, query):
        super(Fetcher, self).__init__()
        self.query = query

    def parse(self, div):
        text = div.text
        text = [x.strip() for x in text.split("\n") if x.strip()]
        dic = {"altTitle": "", "urlImage": div.img["src"], "mainTitle": text[0]}
        if len(text) == 4:
            dic["altTitle"] = text[1][1:].lstrip()
        dic["note"] = text[-1]
        t = text[-2].split(" - ")
        if not t[1].startswith("?"):
            t[1] = int(t[1].split()[0])
        else:
            t[1] = 0
        dic["type_"], dic["epNb"], dic["releasedDate"] = t[0], t[1], t[2]
        return Anime(**dic)

    async def get(self, session, url, contentType):
        async with session.get(url) as response:
            if contentType == "text":
                return await response.text()
            return await response.content.read()

    def run(self):
        async def main():
            async with aiohttp.ClientSession() as session:
                page = await self.get(session, f"https://www.anime-gate.net/ajax/animes/suggest?search={self.query}", "text")
                soup = BeautifulSoup(page, "html.parser")
                divs = soup.find_all("div", {"class": "clearfix suggest"}) + soup.find_all("div", {
                    "class": "clearfix suggest space-up"})
                animes = list(map(self.parse, divs))
                tasks = []
                for anime in animes:
                    task = asyncio.ensure_future(self.get(session, anime.urlImage, "img"))
                    tasks.append(task)
                imgArray = await asyncio.gather(*tasks)
                [animes[x].setData(imgArray[x]) for x in range(len(imgArray))]
                self.finished.emit(animes)

        if self.query:
            asyncio.run(main())
        else:
            self.finished.emit([])



