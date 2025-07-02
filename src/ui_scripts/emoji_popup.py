from functions import *
import json
from const import user_const

from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout


class EmojiPopup(Popup):
    def __init__(self, obj, **kwargs):
        super(EmojiPopup, self).__init__(**kwargs)
        self.obj = obj
        with open(resource_path2("data/config.json"), "r") as f:
            self.config = json.load(f)
        
        self.title = "Pick an Emoji"
        self.size_hint = (0.8, 0.8)

        self.scroll = ScrollView()

        self.grid = GridLayout(cols=8, spacing=5, padding=10, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))

        def emoji_btn(emoji):
            btn = Button(text=emoji)
            self.grid.add_widget(btn)

        for emoji in self.config["EMOJIS"]:
            emoji_btn(emoji)

        self.scroll.add_widget(self.grid)
        self.add_widget(self.scroll)

