import json

import functions as fct
import database as db

from kivy.uix.button import Button
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.properties import ListProperty



class DevModeScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

    def save(self):
        query = self.ids.sql_input.text
        db.dev_insert(query)
        self.ids.sql_input.text = ''