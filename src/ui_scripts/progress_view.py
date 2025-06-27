import json

import database as db
from functions import *

from kivy.uix.button import Button
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty

class ProgressViewWindow(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = App.get_running_app()

        # open the config file
        with open(resource_path2("data/config.json")) as f:
            config = json.load(f)
        self.user = config["name"]


        nb_hab = db.nb_hab(self.user)
        nb_date = db.nb_dates(self.user)

        self.table_layout = BoxLayout(
            col = nb_date,
            rows = nb_hab
        )
        # rows habits
        for i in range(nb_hab):
            
            # columns dates
            for j in range(nb_date):
                pass