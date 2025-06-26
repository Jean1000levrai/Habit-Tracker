import habit_mgr as hmgr
import database as db
import ui_scripts.color_picker as col
from ui_scripts.reminder import reminder_var

import webbrowser as web
import json
from functions import *

from kivy.uix.button import Button
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.properties import ListProperty
from kivymd.uix.pickers import MDTimePicker
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class AddHabitMeasScreen(Screen):
    def __init__(self, edit_mode = False, **kw):
        super().__init__(**kw)
        self.app = App.get_running_app()
        self.info = {}
        self.hab = hmgr.HabitMeasurable()
        self.hab_name = ''
        self.edit_mode = edit_mode
        self.current_hab_name = ''

        # open the config file
        with open(resource_path2("data/config.json")) as f:
            config = json.load(f)
        self.user = config["name"]

    def get_info(self):
        """method that gets the informations from 
        the textinput that the user has filled.
        returns a HabitYesNo containing these infos"""

        print("reminder varrrrrrrrrrrrr")
        print(reminder_var)
        # gets the infos into a dic
        self.info["name"] = self.ids.name.text
        self.info["threshold"] = self.ids.threshold.text
        self.info["unit"] = self.ids.unit.text
        self.info["qu"] = self.ids.qu.text
        self.info["descr"] = self.ids.descr.text
        self.info["frequency"] = reminder_var

        # resets the text inputs
        self.ids.name.text = ""
        self.ids.descr.text = ""
        self.ids.qu.text = ""
        self.ids.threshold.text = ""
        self.ids.unit.text = ""

        # creates a HabitMeasurable with the dic 
        self.hab.name = self.info["name"]
        self.hab.description = self.info["descr"]
        self.hab.question = self.info["qu"]
        self.hab.frequency = self.info["frequency"]
        self.hab.unit = self.info["unit"]
        self.hab.threshold = self.info["threshold"]

        return self.hab

    def save_btn(self):
        """method that handles the 'save' button 
        at the bottom of the screen. It updates the
        database with the HabitMeasurable and displays it
        on the main screen. prints an error if the input
        isnt correct.""" 
        print("saved")
        # open the config file
        with open(resource_path2("data/config.json")) as f:
            config = json.load(f)
        self.user = config["name"]

        try:
            print(self.edit_mode)
            info = self.get_info()
            if self.edit_mode:
                db.update(info, self.current_hab_name, self.user)
                self.edit_mode = False
            else:
                db.add_habit_m(info, self.user)
            self.manager.get_screen("main").empty_hab()
            self.manager.get_screen("main").load_all()

            db.print_table(self.user)
        except:
            print(self.edit_mode)
            print("not a valid input")