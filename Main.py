from pypresence import Presence
import json
from time import sleep, time
from anime_infos import get_anime_info

json_file = open("config.json", "r")
config = json.load(json_file)
json_file.close()

json_file = open("translation.json", "r", encoding="UTF-8")
translation = json.load(json_file)
json_file.close()

client_id = config["App_ID"]  # You can put your own app ID
RPC = Presence(client_id)  # Initialize the client class
RPC.connect()  # Start the handshake loop

url = "https://www.wakanim.tv/fr/v2/catalogue/episode/2497/made-in-abyss-saison-1-episode-04-vostfr"
language = "fr"
language_format = (translation[language])["format"]

actual_epoch = round(time())
url.capitalize()

while True:
    infos = get_anime_info(url)

    if infos[2] != "/":
        state = language_format.replace("watching", translation[language]["watching"])
        state = state.replace("anime_name", infos[1])
        state = state.replace("saison", translation[language]["saison"])
        state = state.replace("s_nb", infos[2])
        state = state.replace("episode", translation[language]["episode"])
        state = state.replace("ep_nb", infos[3])
    else:
        state = language_format.replace("watching", translation[language]["watching"])
        state = state.replace("anime_name", infos[1])
        state = state.replace("episode", translation[language]["episode"])
        state = state.replace("ep_nb", infos[3])

    RPC.update(details="Regarde un anime", state=state, large_image=infos[4], small_image=infos[5], start=actual_epoch)
    sleep(60)
