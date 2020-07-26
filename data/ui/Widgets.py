from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QScrollArea, QVBoxLayout, QSizePolicy, QComboBox
from PyQt5.QtGui import QPixmap, QPalette, QColor
from PyQt5.QtCore import Qt, pyqtSignal, QThread
from itertools import zip_longest
import asyncio
import aiohttp


class Anime:

    def __init__(self, anime_id, image_url, title, romaji, type_, episodes, released_date, duration, description):
        self.id = anime_id
        self.title = title
        self.romaji = romaji
        self.image_url = image_url
        self.type = type_
        self.episodes = episodes
        self.released_date = released_date
        self.dataImage = None
        self.duration = duration
        self.description = description

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
        title = self.anime.title
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
        if len(self.anime.title) > 48:
            self.setToolTip(f"<p style='white-space:pre'>{self.anime.title} ({self.anime.released_date})</p>")

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


class Fetcher(QThread):
    finished = pyqtSignal(list)

    def __init__(self, query):
        super(Fetcher, self).__init__()
        self.query = query

    async def get(self, session, url, contentType):
        async with session.get(url) as response:
            if contentType == "text":
                return await response.text()
            return await response.content.read()

    def run(self):
        async def main():
            async with aiohttp.ClientSession() as session:
                variables["search"] = self.query
                async with session.post("https://graphql.anilist.co",
                                        json={"query": QUERY, "variables": variables}) as response:
                    page = (await response.json())["data"]["Page"]
                animes = list()
                tasks = []
                if page["pageInfo"]["total"] > 0:
                    for media in page["media"]:
                        anime = Anime(anime_id=media["id"],
                                      image_url=media["coverImage"]["large"],
                                      episodes=media["episodes"],
                                      released_date=media["seasonYear"],
                                      description=media["description"],
                                      title=media["title"]["english"] or media["title"]["romaji"],
                                      romaji=media["title"]["romaji"],
                                      duration=media["duration"],
                                      type_=media["format"])
                        animes.append(anime)
                        task = asyncio.ensure_future(self.get(session, anime.image_url, "img"))
                        tasks.append(task)
                    imgArray = await asyncio.gather(*tasks)
                    [animes[x].setData(imgArray[x]) for x in range(len(imgArray))]
                    self.finished.emit(animes)
                else:
                    self.finished.emit(list())

        if self.query:
            asyncio.run(main())
        else:
            self.finished.emit([])


QUERY = """
query ($id: Int, $page: Int, $perPage: Int, $search: String, $type: MediaType) {
    Page (page: $page, perPage: $perPage) {
        pageInfo
        {
            total
        }
        media (id: $id, search: $search, type: $type) {
            id
            title {
                native
                english
                romaji
            }
            coverImage {
                large
                  }
            episodes
            seasonYear
            description
            format
            duration
        }
    }
}
"""

variables = {
    "page": 1,
    "type": "ANIME",
    "perPage": 10,
    "search": ""
}
