import rumps
import getpass
import os
import requests

from utils.logger import Logger
from utils.note import Note

user_name = getpass.getuser()

def check_files():
    files = [
        "https://raw.githubusercontent.com/bentettmar/barnotes/main/data/icon.png",
        "https://raw.githubusercontent.com/bentettmar/barnotes/main/data/note.txt"
    ]

    if not os.path.exists(os.path.expanduser("~/Library/Application Support/BarNotes")):
        os.makedirs(os.path.expanduser("~/Library/Application Support/BarNotes"))

    for file in files:
        if not os.path.exists(os.path.expanduser(f"~/Library/Application Support/BarNotes/{file.split('/')[-1]}")):
            r = requests.get(file)
            with open(os.path.expanduser(f"~/Library/Application Support/BarNotes/{file.split('/')[-1]}"), "wb") as f:
                f.write(r.content)

class BarNotes(rumps.App):
    def __init__(self):
        super(BarNotes, self).__init__("BarNotes", title="  " + Note.get_note(), icon=f"/users/{user_name}/Library/Application Support/BarNotes/icon.png")
        
        self.logger = Logger()
        self.logger.log("BarNotes initialized")

        self.menu = ["Edit Note"]

    @rumps.clicked("Edit Note")
    def edit(self, _):
        window = rumps.Window(title="Edit your note", message="The max amount of characters is 100.", dimensions=(300, 85), ok="Save", cancel="Cancel")
        window.default_text = Note.get_note()
        window.icon = f"/users/{user_name}/Library/Application Support/BarNotes/icon.png"

        self.logger.log("Edit Note window opened")

        response = window.run()
        if response.clicked == 1:
            self.logger.log(f"Set note to {response.text}")
            Note.set_note(response.text)
            self.title = "  " + Note.get_note()
        elif response.clicked == 0:
            self.logger.log("Note was not changed")

    def start(self):
        self.logger.log("BarNotes running")
        self.run()

if __name__ == "__main__":
    check_files()
    app = BarNotes()
    app.start()
