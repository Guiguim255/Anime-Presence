from pypresence import Presence
import json
from time import sleep, time
from anime_infos import get_anime_info

json_file = open("config.json", "r")
config = json.load(json_file)
json_file.close()

client_id = config["App_ID"]  # You can put your own app ID
RPC = Presence(client_id)  # Initialize the client class
RPC.connect()  # Start the handshake loop

url = "https://animedigitalnetwork.fr/video/no-game-no-life/5000-episode-1-debutant"
actual_epoch = round(time())
url.capitalize()

while True:
    infos = get_anime_info(url)

    if infos[2] != "/":
        state = infos[1] + ", " + "saison " + infos[2] + " épisode " + infos[3]
    else:
        state = infos[1]+", "+"épisode "+infos[3]

    RPC.update(details="Regarde un anime", state=state, large_image=infos[4], small_image=infos[5], start=actual_epoch)
    sleep(60)
