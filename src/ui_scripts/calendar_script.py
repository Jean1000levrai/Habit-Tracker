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
        days = ['M', 'T', 'W', 'Th', 'F', 'S', 'Su']
        self.days_btn = []
        self.app = App.get_running_app()

        for i in range(7):
            btn = Button(
                text = str(days[i]),
                pos_hint= {'right': 0.16 + i*0.13,'top': 0.3},
                size_hint_x = None,
                size_hint_y = None,
                width = 40,
                height = 40,
                background_color=self.app.button_color,
                color=self.app.text_color,
            )

            self.days_btn.append(btn)
            # self.app.bind(text_color=lambda instance, value, b=btn: setattr(b, 'color', value))
            self.ids.top_panel_cal.add_widget(btn)
            btn.bind(on_release=self.on_btn_release)
    def sets_days(self):
        today_date = datetime.today().strftime("%d-%m-%Y")
        today_day = datetime.today().strftime("%A")


    def on_btn_release(self, event):
        print("clicked lol")