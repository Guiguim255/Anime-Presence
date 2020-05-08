import json


def get_image(infos):
    with open("data/database.json", "r") as f:
        db = json.load(f)

    try:
        image = (db[infos["website"]])[infos["anime_name"]]
        small_image = infos["website"] + "_logo"
    except KeyError:
        image = infos["website"] + "_logo"
        small_image = "/"

    informations = infos
    informations["image"] = image
    informations["small_image"] = small_image

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

    informations = {"website": "wakanim", "anime_name": nom, "s_nb": saison, "ep_nb": episode}

    return informations


def adn_infos(url):
    n = []
    nom = (url[3].replace("-", " ")).title()

    part = url[-1].replace("-", " ")
    for word in part.split():
        n.append(word)

    episode = n[n.index("episode") + 1]
    saison = "/"

    informations = {"website": "adn", "anime_name": nom, "s_nb": saison, "ep_nb": episode}

    return informations


def crunchyroll_info(url):
    n = []
    nom = (url[3].replace("-", " ")).title()

    part = url[-1].replace("-", " ")
    for word in part.split():
        n.append(word)

    episode = n[n.index("episode") + 1]
    saison = "/"

    informations = {"website": "crunchyroll", "anime_name": nom, "s_nb": saison, "ep_nb": episode}

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
