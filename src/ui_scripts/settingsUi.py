import webbrowser as web
import json

import functions as fct

from kivy.uix.button import Button
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.properties import ListProperty


class SettingsWindow(Screen):
    """the settings window"""
    def __init__(self, **kw):
        super().__init__(**kw)
        self.theme_dark = True

    def link_github(self):
        link = 'https://github.com/Jean1000levrai/Habit-Tracker'
        web.open(link)
    
    def signout(self):
        # open the config file
        with open(fct.resource_path2("data/config.json")) as f:
            config = json.load(f)
        # resets the username to default
        config["name"] = ''
        with open(fct.resource_path2("data/config.json"), 'w') as f:
            json.dump(config, f, indent=1)
        # loads the default config when signed out
        self.manager.get_screen("main").empty_hab()
        self.manager.get_screen("main").load_all()
    
    def sort_hab(self):
        text = self.ids.sort_hab.text[9:]

        # open the config file
        with open(fct.resource_path2("data/config.json")) as f:
            config = json.load(f)

        # change the sorting method through the config file
        config["sort"] = text
        with open(fct.resource_path2("data/config.json"), 'w') as f:
            json.dump(config, f, indent=1)

        # reloads the habits
        self.manager.get_screen("main").empty_hab()
        self.manager.get_screen("main").load_all()



class AboutWindow(Screen):
    pass
