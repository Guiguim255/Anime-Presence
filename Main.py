from tkinter import Tk, Label, Button, Entry, PhotoImage, Canvas, END, Menu
from pypresence import Presence
import json
from time import time
from anime_infos import get_anime_info


class Userinterface(Tk):
    def __init__(self):
        super().__init__()

        json_file = open("data/config.json", "r")
        self.config_json = json.load(json_file)
        json_file.close()

        json_file = open("data/translation.json", "r", encoding="UTF-8")
        self.translation = json.load(json_file)
        json_file.close()

        client_id = self.config_json["App_ID"]  # You can put your own app ID
        self.RPC = Presence(client_id)  # Initialize the client class
        self.RPC.connect()  # Start the handshake loop

        self.language = self.config_json["user_language"]
        self.l_format = self.translation[self.language]["format"]

        self.title("Anime Presence")
        self.iconbitmap("data/images/icon.ico")
        self.geometry("400x300")

        menubar = Menu(self)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label=self.translation[self.language]["change language"], command=self.language_window)

        menubar.add_cascade(label=self.translation[self.language]["settings"], menu=filemenu)
        self.config(menu=menubar)

        self.image = PhotoImage(file="data/images/icon.png").subsample(6)
        self.canvas = Canvas(self, width=100, height="100")
        self.canvas.create_image(50, 50, image=self.image)
        self.canvas.pack()

        self.title_label = Label(self, text=self.translation[self.language]["please enter url"])
        self.title_label.pack()
        self.url_entry = Entry(self)
        self.url_entry.pack()
        self.confirm_button = Button(self, text=self.translation[self.language]["confirm"], command=self.confirm)
        self.confirm_button.pack()

        self.result_label = Label(self, text="", fg="#26bc1a")
        self.result_label.pack()

    def confirm(self):
        url = self.url_entry.get()
        url.capitalize()

        self.update_presence(url)

        self.url_entry.delete(0, END)

        self.result_label.config(text=self.translation[self.language]["updated presence"])

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
        self.actual_epoch = round(time())
        self.infos = get_anime_info(url)

        if self.infos["s_nb"] != "/":
            state = self.generate_state(self.l_format, ["saison", "episode"], ["anime_name", "ep_nb", "s_nb"])
        else:
            state = self.generate_state(self.l_format, ["episode"], ["anime_name", "ep_nb"], ["saison", "s_nb"])

        self.RPC.update(details=self.translation[self.language]["watching an anime"], state=state,
                        large_image=self.infos["image"],
                        small_image=self.infos["small_image"],
                        start=self.actual_epoch)

    def language_window(self):
        self.canvas.destroy()
        self.title_label.destroy()
        self.url_entry.destroy()
        self.confirm_button.destroy()
        self.result_label.destroy()

        self.language_label = Label(self,
                                    text=self.translation[self.language]["enter abbreviation"])
        self.language_label.pack()

        self.language_entry = Entry(self)
        self.language_entry.pack()

        self.language_button = Button(self, text=self.translation[self.language]["save"], command=self.change_language)
        self.language_button.pack()

        self.language_result_label = Label(self, text="")
        self.language_result_label.pack()

    def change_language(self):
        new_language = self.language_entry.get()

        if self.language_exist(new_language):
            self.config_json["user_language"] = new_language

            with open('data/config.json', 'w') as f:
                json.dump(self.config_json, f, indent=2)

            self.language_result_label.config(
                text=self.translation[new_language]["language changed"], fg="#26bc1a")
        else:
            self.language_result_label.config(text="This language is not available", fg="#ff0000")

    def language_exist(self, language_to_check):
        try:
            test = self.translation[language_to_check]["episode"]
            return True
        except KeyError:
            return False


window = Userinterface()
window.mainloop()
