import habit_mgr as hmgr
import database as db
import ui_scripts.color_picker as col
import webbrowser as web

from functions import *
import json

from kivy.uix.button import Button
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.properties import ListProperty
from kivymd.uix.pickers import MDTimePicker


class AddHabitWindow(Screen):
    """the window where you add a habit"""
    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = App.get_running_app()
        self.info = {}
        self.hab = hmgr.HabitYesNo()
        self.hab_name = ''
        # open the config file
        with open(resource_path2("data/config.json")) as f:
            config = json.load(f)
        self.user = config["name"]

    def get_info(self):
        """method that gets the informations from 
        the textinput that the player has filled.
        returns a HabitYesNo containing these infos"""
        # gets the infos into a dic
        self.info["name"] = self.ids.name.text
        self.info["descr"] = self.ids.descr.text
        self.info["qu"] = self.ids.qu.text

        # resets the text inputs
        self.ids.name.text = ""
        self.ids.descr.text = ""
        self.ids.qu.text = ""

        # creates a HabitYesNo with the dic 
        self.hab.name = self.info["name"]
        self.hab.description = self.info["descr"]
        self.hab.question = self.info["qu"]

        return self.hab

    def save_btn(self):
        """method that handles the 'save' button 
        at the bottom of the screen. It updates the
        database with the HabitYesNo and displays it
        on the main screen. prints an error if the input
        isnt correct.""" 
        # try:
        info = self.get_info()
        db.add_habit(info, self.user)
        self.manager.get_screen("main").empty_hab()
        self.manager.get_screen("main").load_all()

        db.print_table(self.user)
        # except:
        #     print("not a valid input")

    def on_btn_release(self, instance):
        # recovers the name of the clicked btn
        self.hab_name = instance.text
        print(self.hab_name)

        self.add_the_info()

        # handles the window change
        self.manager.transition.direction = "left"
        self.manager.current = "info"

    def add_the_info(self):
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
        db.delete_habit(self.hab_name, self.user)

    def color_selected(self, color):
        self.info["col"] = (str(color))
        self.hab.colour = self.info["col"]

class HabitInfoWindow(Screen):
    """window where the informations of the habit will be displayed"""
    def __init__(self, **kw):
        super().__init__(**kw)
        # open the config file
        with open(resource_path2("data/config.json")) as f:
            config = json.load(f)
        self.user = config["name"]

    def delete_habit(self):
        # open the config file
        with open(resource_path2("data/config.json")) as f:
            config = json.load(f)

        hab_name = self.ids.name_of_the_hab.text[3:]
        db.delete_habit(hab_name, config["name"])

        # sets it so that next time it wont show the popup
        config["first_timer"] = False
        with open(resource_path2("data/config.json"), 'w') as f:
            json.dump(config, f, indent=1)

class AddHabitPopup(Popup):
    """popup where the user will be able to
    chose between a yes or no habit or one
    that measures something e g. 'num of pages read'"""
    def __init__(self, obj, **kwargs):
        super(AddHabitPopup, self).__init__(**kwargs)
        self.obj = obj

class ReminderWindow(Screen):
    def date_popup(self):
        popup = DatePopup(self)
        popup.open()
    
    def time_popup(self):
        popup = TimePopup(self)
        popup.open()

    def next(self):
        times = self.ids.times.text         # gets the nb of times
        container = self.ids.time_select
        container.clear_widgets()   # clears to not stack if opened more than once

        # add the btns
        for i in range(int(times)):
            btn = Button(text="00:00",
                         size_hint_y = None,
                         height = 40) 
            container.add_widget(btn)
    
class TimePickerPopup(Popup):
    def __init__(self, parent_screen, **kwargs):
        super().__init__(**kwargs)
        self.parent_screen = parent_screen

class DatePopup(Popup):
    def __init__(self, parent_screen, **kwargs):
        super().__init__(**kwargs)
        self.parent_screen = parent_screen

class TimePopup(Popup):
    def __init__(self, parent_screen, **kwargs):
        super(TimePopup, self).__init__(**kwargs)
        self.parent_screen = parent_screen

    def next(self):
        popup = MDTimePicker()
        popup.open()  
    