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


class AddHabitWindow(Screen):
    """the window where you add a habit"""
    def __init__(self, edit_mode = False, **kw):
        super().__init__(**kw)
        self.app = App.get_running_app()
        self.info = {}
        self.hab = hmgr.HabitYesNo()
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
        # gets the infos into a dic
        self.info["name"] = self.ids.name.text
        self.info["descr"] = self.ids.descr.text
        self.info["qu"] = self.ids.qu.text
        self.info["frequency"] = reminder_var

        # resets the text inputs
        self.ids.name.text = ""
        self.ids.descr.text = ""
        self.ids.qu.text = ""

        # creates a HabitYesNo with the dic 
        self.hab.name = self.info["name"]
        self.hab.description = self.info["descr"]
        self.hab.question = self.info["qu"]
        self.hab.frequency = self.info["frequency"]


        return self.hab

    def save_btn(self):
        """method that handles the 'save' button 
        at the bottom of the screen. It updates the
        database with the HabitYesNo and displays it
        on the main screen. prints an error if the input
        isnt correct.""" 
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
                db.add_habit(info, self.user)
            self.manager.get_screen("main").empty_hab()
            self.manager.get_screen("main").load_all()

            db.print_table(self.user)
        except:
            print(self.edit_mode)
            print("not a valid input")

    def on_btn_releasde(self, instance):
        # open the config file
        with open(resource_path2("data/config.json")) as f:
            config = json.load(f)
        self.user = config["name"]

        # recovers the name of the clicked btn
        self.hab_name = instance.text
        print(self.hab_name)

        self.add_the_info()

        # handles the window change
        self.manager.transition.direction = "left"
        self.manager.current = "info"

    def add_the_info(self):
        # open the config file
        with open(resource_path2("data/config.json")) as f:
            config = json.load(f)
        self.user = config["name"]

        self.manager.get_screen("info").ids.name_of_the_hab.text = f"<- {self.hab_name}"
        question = db.get_info_hab(self.hab_name, "question", self.user)
        self.manager.get_screen("info").ids.qu_for_hab.text = question

        descr = db.get_info_hab(self.hab_name, "description", self.user)
        self.manager.get_screen("info").ids.descr_for_hab.text = str(descr)

        reminder = db.get_info_hab(self.hab_name, "reminder", self.user)
        self.manager.get_screen("info").ids.rem_for_hab.text = str(reminder)

        frequency = db.get_info_hab(self.hab_name, "frequency", self.user)
        self.manager.get_screen("info").ids.freq_for_hab.text = str(frequency)

    def delete_habit(self):
        # open the config file
        with open(resource_path2("data/config.json")) as f:
            config = json.load(f)
        self.user = config["name"]

        db.delete_habit(self.hab_name, self.user)

    def reminder_on_off(self):
        if self.ids.reminder_off.text == "Reminder : off":
            self.ids.reminder_off.text = "Reminder : on"
        else:
            self.ids.reminder_off.text = "Reminder : off"

class AddHabitPopup(Popup):
    """popup where the user will be able to
    chose between a yes or no habit or one
    that measures something e g. 'num of pages read'"""
    def __init__(self, obj, **kwargs):
        super(AddHabitPopup, self).__init__(**kwargs)
        self.obj = obj

