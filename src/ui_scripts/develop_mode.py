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
        output = db.dev_insert(query)
        output2 = ''
        n = len(str(output))
        print(n)
        for i in range(n):
            if i%42==0:
                output2 = output2 + "\n"
            output2 = output2 + str(output)[i]

        self.ids.sql_input.text = ''
        print(output2)
        self.ids.output.text = str(output2)