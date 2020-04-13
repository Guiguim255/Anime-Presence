from pypresence import Presence
import json
from time import sleep, time
from anime_infos import get_anime_info


def generate_state(language_format, translations, variables):
    new_str = language_format
    for element in translations:
        new_str = new_str.replace(element, translation[language][element])

    for element in variables:
        new_str = new_str.replace(element, infos[element])

    return new_str


json_file = open("config.json", "r")
config = json.load(json_file)
json_file.close()

json_file = open("translation.json", "r", encoding="UTF-8")
translation = json.load(json_file)
json_file.close()

client_id = config["App_ID"]  # You can put your own app ID
RPC = Presence(client_id)  # Initialize the client class
RPC.connect()  # Start the handshake loop

language = "fr"
l_format = (translation[language])["format"]

actual_epoch = round(time())


def update_presence(url):
    infos = get_anime_info(url)

    if infos["s_nb"] != "/":
        state = generate_state(l_format, ["saison", "episode"], ["anime_name", "ep_nb", "s_nb"])
    else:
        state = generate_state(l_format, ["episode"], ["anime_name", "ep_nb"])

    RPC.update(details=translation[language]["watching an anime"], state=state, large_image=infos["image"],
               small_image=infos["small_image"],
               start=actual_epoch)
