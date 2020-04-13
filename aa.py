from tkinter import Tk, Label, Button, Entry, PhotoImage, Canvas, END
from pypresence import Presence
import json
from time import time
from anime_infos import get_anime_info


class Userinterface(Tk):
    def __init__(self):
        super().__init__()

        json_file = open("config.json", "r")
        self.config = json.load(json_file)
        json_file.close()

        json_file = open("translation.json", "r", encoding="UTF-8")
        self.translation = json.load(json_file)
        json_file.close()

        client_id = self.config["App_ID"]  # You can put your own app ID
        self.RPC = Presence(client_id)  # Initialize the client class
        self.RPC.connect()  # Start the handshake loop

        self.language = "fr"
        self.l_format = self.translation[self.language]["format"]

        self.actual_epoch = round(time())

        self.title("Anime Presence")
        self.iconbitmap("icon.ico")
        self.geometry("400x300")

        self.image = PhotoImage(file="icon.png").subsample(6)
        self.canvas = Canvas(self, width=100, height="100")
        self.canvas.create_image(50, 50, image=self.image)
        self.canvas.pack()

        self.title_label = Label(self, text=self.translation[self.language]["please enter url"])
        self.title_label.pack()
        self.url_entry = Entry(self)
        self.url_entry.pack()
        self.confirm_button = Button(self, text="Confirmer", command=self.confirm)
        self.confirm_button.pack()

        self.result_label = Label(self, text="", fg="#26bc1a")
        self.result_label.pack()

    def confirm(self):
        url = self.url_entry.get()
        url.capitalize()

        self.update_presence(url)

        self.url_entry.delete(0, END)

        self.result_label.config(text="Présence mise à jour")

    def generate_state(self, language_format, translations, variables, removable=None):
        new_str = language_format
        for element in translations:
            new_str = new_str.replace(element, self.translation[self.language][element])

        for element in variables:
            new_str = new_str.replace(element, self.infos[element])

        if removable is not None:
            for element in removable:
                new_str = new_str.replace(element, "")

        return new_str

    def update_presence(self, url):
        self.infos = get_anime_info(url)

        if self.infos["s_nb"] != "/":
            state = self.generate_state(self.l_format, ["saison", "episode"], ["anime_name", "ep_nb", "s_nb"])
        else:
            state = self.generate_state(self.l_format, ["episode"], ["anime_name", "ep_nb"], ["saison", "s_nb"])

        self.RPC.update(details=self.translation[self.language]["watching an anime"], state=state,
                        large_image=self.infos["image"],
                        small_image=self.infos["small_image"],
                        start=self.actual_epoch)


window = Userinterface()
window.mainloop()
