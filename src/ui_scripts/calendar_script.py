import habit_mgr as hmgr
import database as db
import ui_scripts.color_picker as col
import webbrowser as web
import calendar as cldr
from datetime import datetime

from functions import *
import json

from kivy.uix.button import Button
from kivy.app import App
from kivy.uix.screenmanager import Screen


class CalendarScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.days = ['M', 'T', 'W', 'Th', 'F', 'S', 'Su']
        self.id_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        self.days_to_monday = {
            'M': 0, 'Monday': 0,
            'T': 1, 'Tuesday': 1,
            'W': 2, 'Wednesday': 2,
            'Th': 3, 'Thursday': 3,
            'F': 4, 'Friday': 4,
            'S': 5, 'Saturday': 5,
            'Su': 6, 'Sunday': 6
        }
        self.days_btn = {}
        self.hours_btn = {}

        self.current_day = datetime.today().strftime("%A")
        self.current_date = datetime.today().strftime("%d-%m-%Y")
        
        self.app = App.get_running_app()

        # open the config file
        with open(resource_path2("data/config.json")) as f:
            config = json.load(f)
        self.user = config["name"]

        self.sets_every_day()
        self.sets_day(self.current_day, self.current_date)
        self.sets_every_hours()


    def sets_every_hours(self):
        # adds every hours as a btn 
        for j in range(24):
            btn1 = Button(
                text = f"{j} : 00",

                background_color=(0,0,0,0),
                color=self.app.text_color,
                size_hint_x = None,
                width = 90,
            )
            btn2 = Button(
                text = "",

                background_color=self.app.button_color,
                color=self.app.text_color,
            )
            self.ids.calendar_square.add_widget(btn1)
            self.ids.calendar_square.add_widget(btn2)
            self.hours_btn[btn1.text] = btn2

    def delete_every_hours(self):
        pass



    def sets_every_day(self):
        # adds every days as a btn
        for i in range(7):
            btn = Button(
                text = str(self.days[i]),
                pos_hint= {'right': 0.16 + i*0.13,'top': 0.3},
                size_hint_x = None,
                size_hint_y = None,
                width = 40,
                height = 40,
                background_color=self.app.button_color,
                color=self.app.text_color,
            )

            self.days_btn[self.id_days[i]] = btn
            self.days_btn[self.days[i]] = btn

            self.ids.top_panel_cal.add_widget(btn)
            btn.bind(on_release=lambda instance, b=btn: self.on_btn_release(b, instance))

    def sets_day(self, today_day, today_date):   
        self.days_btn[today_day].background_color = (0, 0.5, 0, 1)
        self.ids.date.text = today_date

    def delete_every_day(self):
        layout = self.ids.top_panel_cal
        # clears days
        for day in self.days_btn.values():
            if day.parent:
                layout.remove_widget(day)
        self.days_btn.clear()


    def day_forward(self):
        print("next day")

    def day_backward(self):
        print("previous day")

    def add_hab_cal(self, day):
        # open the config file
        with open(resource_path2("data/config.json")) as f:
            config = json.load(f)
        self.user = config["name"]

    def on_btn_release(self, btn, instance):
        self.current_day = btn.text
        self.delete_every_day()
        self.sets_every_day()
        self.sets_day(self.current_day, self.current_date)
