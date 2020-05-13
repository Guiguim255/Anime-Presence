import json
from bs4 import BeautifulSoup
import asyncio
import aiohttp
from urllib.parse import urlparse

headers={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36"}

def getAnimeInfos(url):
    async def get(session, url):
        async with session.get(url, headers=headers) as response:
            return await response.text()
    async def main():
        async with aiohttp.ClientSession() as session:
            html = await get(session, url)
            soup = BeautifulSoup(html, "html.parser")
            parsedUrl = urlparse(url)
            netloc = parsedUrl[1]
            website = ""
            nEpisode = nSaison = "0"
            if "episode" in url:
                nEpisode = parsedUrl[2].split("/")[-1].split("-")[parsedUrl[2].split("/")[-1].split("-").index("episode") + 1]
            if "saison" in url:
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
                html2 = await get(session, url2)
                soup2 = BeautifulSoup(html2, "html.parser")
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

            return {"website":website, "anime_name":title, "ep_nb":nEpisode, "s_nb":nSaison, "image":image, "small_image":small_image}
    loop = asyncio.get_event_loop()
    infos = loop.run_until_complete(main())
    return infos

