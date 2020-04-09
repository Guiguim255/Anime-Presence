import json


def get_image(infos):
    with open("database.json", "r") as f:
        db = json.load(f)

    try:
        image = (db[infos[0]])[infos[1]]
        small_image = infos[0] + "_logo"
    except KeyError:
        image = infos[0] + "_logo"
        small_image = "/"

    informations = infos
    informations.append(image)
    informations.append(small_image)

    return informations


def wakanim_info(url):
    m = url
    n = []
    part = m[-1].replace("-", " ")

    for word in part.split():
        n.append(word)

    try:
        del (n[n.index("cour") + 1])
        n.remove("cour")
    except ValueError:
        pass

    del (n[-1])
    saison = n[n.index("saison") + 1]
    episode = n[n.index("episode") + 1]
    nom = ""
    for x in range(len(n) - 4):
        nom += " " + n[x]
    nom = nom.title()

    x = []

    for letter in nom:
        x.append(letter)

    x.remove(x[0])

    nom = ""
    for element in x:
        nom += element

    informations = ["wakanim", nom, saison, episode]

    return informations


def adn_infos(url):
    n = []
    nom = (url[3].replace("-", " ")).title()

    part = url[-1].replace("-", " ")
    for word in part.split():
        n.append(word)

    episode = n[n.index("episode") + 1]
    saison = "/"

    informations = ["adn", nom, saison, episode]

    return informations


def crunchyroll_info(url):
    n = []
    nom = (url[3].replace("-", " ")).title()

    part = url[-1].replace("-", " ")
    for word in part.split():
        n.append(word)

    episode = n[n.index("episode") + 1]
    saison = "/"

    informations = ["crunchyroll", nom, saison, episode]
    return informations


def get_anime_info(url):
    url = url.replace("/", " ")
    m = []
    for element in url.split():
        m.append(element)

    if m[1] == "www.wakanim.tv":
        return get_image(wakanim_info(m))

    if m[1] == "www.animedigitalnetwork.fr" or "animedigitalnetwork.fr":
        return get_image(adn_infos(m))

    if m[1] == "www.crunchyroll.com":
        return get_image(crunchyroll_info(m))

    else:
        pass
