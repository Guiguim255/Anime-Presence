import json
from urllib.request import urlopen, Request
from PyQt5.QtCore import QThread, pyqtSignal
from bs4 import BeautifulSoup
from urllib.parse import urlparse

headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36"}


class AnimeInfos(QThread):
    infos = pyqtSignal(dict)

    def __init__(self, url, Type, **kwargs):
        super(AnimeInfos, self).__init__(**kwargs)
        self.url = url
        self.Type = Type

    def get(self, url):
        request = Request(url)
        request.add_header("User-Agent",headers["User-Agent"])
        page = urlopen(request).read()
        return page

    def run(self):
        html = self.get(self.url)
        soup = BeautifulSoup(html, "html.parser")
        parsedUrl = urlparse(self.url)
        netloc = parsedUrl[1]
        website = ""
        nEpisode = nSaison = "0"
        if "episode" in self.url:
            nEpisode = parsedUrl[2].split("/")[-1].split("-")[parsedUrl[2].split("/")[-1].split("-").index("episode") + 1]
        if "saison" in self.url:
            nSaison = parsedUrl[2].split("-")[parsedUrl[2].split("-").index("saison") + 1]
            for i,val in enumerate(nSaison):
                if not(val.isdigit()):
                    nSaison = "".join(nSaison[:i])
                    break
        if "animedigitalnetwork" in netloc:
            title = soup.find("meta", {"itemprop":"name"})["content"].split(" - ")[0]
            website = "adn"
        if netloc == "www.wakanim.tv":
            website = "wakanim"
            mainUrl = soup.find("a", {"class":"button -thin -outline"})["href"]
            url2 = "://".join(parsedUrl[:2]) + mainUrl
            soup2 = BeautifulSoup(self.get(url2), "html.parser")
            title = soup2.find("meta", {"itemprop":"name"})["content"].rstrip()
        if netloc == "www.crunchyroll.com":
            website = "crunchyroll"
            title = soup.find("meta", {"property":"og:title"})["content"]
        with open("data/database.json", "r") as f:
            db = json.load(f)

        try:
            image = db[website][title]
            small_image = website + "_logo"
        except KeyError:
            image = website + "_logo"
            small_image = ""

        self.infos.emit({"website":website, "anime_name":title, "ep_nb":nEpisode, "s_nb":nSaison, "image":image, "small_image":small_image})

