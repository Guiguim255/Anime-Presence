from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QScrollArea, QVBoxLayout, QSizePolicy
from PyQt5.QtGui import QPixmap, QPalette, QColor
from PyQt5.QtCore import Qt, pyqtSignal, QThread
from itertools import zip_longest
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import re

pattern = re.compile("([0-9]+) Episodes")

class AnimeScrollView(QScrollArea):
    clicked = pyqtSignal(list)

    def __init__(self):
        super(AnimeScrollView, self).__init__()

        palette = QPalette()
        self.setObjectName("AnimeScrollView")
        self.setStyleSheet("QWidget#AnimeScrollView{background-color:#46494D;}")
        palette.setColor(QPalette.Background, QColor("#46494D"))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        self.widget = QWidget()
        self.animeLabels = []
        self.layout = QVBoxLayout(self.widget)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidget(self.widget)
        self.setWidgetResizable(True)
        self.setMinimumHeight(142)
        self.setGeometry(0, 0, 400, 142)
        self.verticalScrollBar().setSingleStep(48)
        self.hide()

    def fill(self, titles):
        for i in reversed(range(self.layout.count())):
            layoutToRemove = self.layout.itemAt(i).layout()
            for t in reversed(range(layoutToRemove.count())):
                widgetToRemove = layoutToRemove.itemAt(t).widget()
                layoutToRemove.removeWidget(widgetToRemove)
                widgetToRemove.setParent(None)
            self.layout.removeItem(layoutToRemove)
            layoutToRemove.setParent(None)
        self.animeLabels.clear()
        for pair in zip_longest(titles[::2], titles[1::2]):
            layout = QHBoxLayout(self.widget)
            self.animeLabels.append(AnimeLabel(*pair[0]))
            self.animeLabels[-1].labelClicked.connect(self.onClick)
            layout.addWidget(self.animeLabels[-1])
            if pair[1] is not None:
                self.animeLabels.append(AnimeLabel(*pair[1]))
                layout.addWidget(self.animeLabels[-1])
                self.animeLabels[-1].labelClicked.connect(self.onClick)
            self.layout.addLayout(layout)
        self.show()
        if not titles:
            self.hide()

    def onClick(self, infos):
        self.clicked.emit(infos)


class AnimeLabel(QWidget):
    labelClicked = pyqtSignal(list)

    def __init__(self, title, byteArray, url, episode):
        super(AnimeLabel, self).__init__()
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor("#46494D"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        self.url = url
        self.episode = episode

        self.title = title
        if len(title) > 48:
            title = title[:46] + "..."
            self.setToolTip(f"<p style='color:black;white-space:pre'>{self.title}</p>")
        self.layout = QHBoxLayout()

        self.image = QPixmap()
        self.image.loadFromData(byteArray)
        self.image = self.image.scaledToHeight(50, Qt.SmoothTransformation)
        self.imLabel = QLabel()
        self.imLabel.setPixmap(self.image)
        self.imLabel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)

        self.titleLabel = QLabel(self)
        self.titleLabel.setWordWrap(True)
        self.titleLabel.setTextFormat(Qt.RichText)
        self.titleLabel.setText(
            f"""<html><body><p align="center"><b>{title}</b></p></body></html>""")
        self.titleLabel.setAlignment(Qt.AlignVCenter)

        self.layout.addWidget(self.imLabel)
        self.layout.addWidget(self.titleLabel)
        self.setLayout(self.layout)

    def mousePressEvent(self, event) -> None:
        self.labelClicked.emit([self.title, self.url, self.episode])

    def leaveEvent(self, event):
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor("#46494D"))
        self.setPalette(palette)

    def enterEvent(self, event):
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor("#797f86"))
        self.setPalette(palette)


class Fetcher(QThread):
    finished = pyqtSignal(list)

    def __init__(self, query):
        super(Fetcher, self).__init__()
        self.query = query

    def run(self):
        async def get(session, url, contentType):
            async with session.get(url) as response:
                if contentType == "text":
                    return await response.text()
                return await response.content.read()

        async def main():
            async with aiohttp.ClientSession() as session:
                page = await get(session, f"https://www.anime-gate.net/ajax/animes/suggest?search={self.query}", "text")
                soup = BeautifulSoup(page, "html.parser")
                divs = soup.find_all("div", {"class": "clearfix suggest"}) + soup.find_all("div", {"class":"clearfix suggest space-up"})
                url= [x["data-url"] for x in divs]
                episodes = [int(re.findall(pattern, x)[0]) for x in [x.text for x in divs]]
                imgs = soup.find_all("img", {"class": "pull-left"})
                imgLinks, titles = [*map(lambda x: x["src"], imgs)], [*map(lambda x: x["title"], imgs)]
                tasks = []
                for imgLink in imgLinks:
                    task = asyncio.ensure_future(get(session, imgLink, "img"))
                    tasks.append(task)
                imgArray = await asyncio.gather(*tasks)
                self.finished.emit([*zip(titles, imgArray, url, episodes)])

        if self.query:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            future = asyncio.ensure_future(main())
            loop.run_until_complete(future)
        else:
            self.finished.emit([])