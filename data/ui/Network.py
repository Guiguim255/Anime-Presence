from PyQt5.QtNetwork import QNetworkRequest, QNetworkReply, QNetworkAccessManager
from PyQt5.QtCore import QByteArray, QObject, QUrl, pyqtSignal
import json
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re

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
                extraLarge
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
URL = "https://graphql.anilist.co"

class Anime:

    def __init__(self, id, title, coverImage, episodes, seasonYear, description, format, duration):
        self.id = id
        self.nativeTitle = title.get("native")
        self.englishTitle = title.get("english")
        self.romajiTitle = title.get("romaji")
        self.title = self.englishTitle or self.romajiTitle or self.nativeTitle
        self.extraLargeImage = coverImage.get("extraLarge")
        self.extraLargeDataImage = bytes()
        self.largeImage = coverImage.get("large")
        self.largeDataImage = bytes()
        self.episodes = episodes
        self.seasonYear = seasonYear
        self.description = description
        self.format = format
        self.duration = duration


class Fetcher(QObject):
    finished = pyqtSignal(list)

    def __init__(self):
        super(Fetcher, self).__init__()
        self.animes = dict()
        self.terminated = False
        self.manager = QNetworkAccessManager()
        self.count, self.length = 0, 0

    def run(self, query, per_page = 10):
        variables["search"], variables["perPage"] = query, per_page
        request = QNetworkRequest(QUrl(URL))
        request.setHeader(QNetworkRequest.ContentTypeHeader,
                          'application/json')
        array = QByteArray()
        array.append(json.dumps({"query": QUERY, "variables": variables}))
        self.manager.finished.connect(self.getImages)
        self.manager.post(request, array)

    def getImages(self, reply:QNetworkReply):
        if reply.error() == QNetworkReply.NoError:
            self.manager.finished.disconnect(self.getImages)
            self.manager.finished.connect(self.handleData)
            response = json.loads(str(reply.readAll(), "utf-8"))
            self.length = 10 if response["data"]["Page"]["pageInfo"]["total"] >= 10 else response["data"]["Page"]["pageInfo"]["total"]
            print(len(response["data"]["Page"]["media"]))
            for index, media in enumerate(response["data"]["Page"]["media"]):
                if self.terminated:
                    return
                anime = Anime(**media)
                self.animes[anime.largeImage] = anime
                request = QNetworkRequest(QUrl(anime.largeImage))
                request.setAttribute(QNetworkRequest.HttpPipeliningAllowedAttribute, True)
                self.manager.get(request)
        else:
            pass

    def get_image(self, link, callback):
        request = QNetworkRequest(QUrl(link))
        self.manager.finished.connect(lambda reply: self.handle_image(reply, callback))
        self.manager.get(request)

    def handle_image(self, reply, callback):
        data = bytes()
        if reply.error() == QNetworkReply.NoError:
            data = reply.readAll()
        callback(data)

    def handleData(self, reply:QNetworkReply):
        if reply.error() == QNetworkReply.NoError:
            data = reply.readAll()
            self.animes[reply.url().url()].largeDataImage = data
            self.count += 1
            if self.count == self.length:
                self.finished.emit(list(self.animes.values()))
                self.terminate()
        else:
            print("error")

    def terminate(self):
        self.terminated = True
        self.manager.deleteLater()
        del self.manager

    def parse_url(self, arg:QNetworkReply, callback, step = 1):
        title, episode = "", 0
        if step == 1:
            parsed = urlparse(arg)
            path = parsed.path
            if parsed.netloc == "www.crunchyroll.com":
                title = path.split("/")[-2].replace("-", " ")
                match = re.match(r".*episode-([0-9]*)", path)
                if match:
                    episode = int(match.group(1))
                callback(title, episode)
            elif parsed.netloc in ("animedigitalnetwork.fr", "www.wakanim.tv"):
                request = QNetworkRequest(QUrl(arg))
                request.setHeader(QNetworkRequest.UserAgentHeader, b"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36")
                self.manager.finished.connect(lambda reply: self.parse_url(reply, callback, 2))
                self.manager.get(request)
        elif step == 2:
            if arg.error() == QNetworkReply.NoError:
                text = str(arg.readAll(), "utf-8")
                soup = BeautifulSoup(text, "html.parser")
                parsed = urlparse(arg.url().url())
                if parsed.netloc == "animedigitalnetwork.fr":
                    infos = str(soup.title).lstrip("<title>").rstrip("</title>").split(" - ")
                    title = infos[0]
                    if "- LE FILM - " in title:
                        title = "".join(title.split("- LE FILM -"))
                    match = re.match(r".*Épisode ([0-9]*)", infos[-4])
                    if match:
                        episode = int(match.group(1))
                elif parsed.netloc == "www.wakanim.tv":
                    title = soup.find("span", {"class": "episode_title"}).text
                    span = soup.find("span", {"class": "episode_subtitle"}).text
                    match = re.match(r".*ÉPISODE ([0-9]*)", span, flags = re.DOTALL)
                    if match:
                        episode = match.group(1)
            callback(title, episode)
