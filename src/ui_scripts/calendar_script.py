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
        id_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        self.days_btn = {}
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

            self.days_btn[id_days[i]] = btn
            print(btn.text)
            # self.app.bind(text_color=lambda instance, value, b=btn: setattr(b, 'color', value))
            self.ids.top_panel_cal.add_widget(btn)
            btn.bind(on_release=lambda instance, b=btn: self.on_btn_release(b))
            self.sets_days()
            
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


    def sets_days(self):
        today_date = datetime.today().strftime("%d-%m-%Y")
        today_day = datetime.today().strftime("%A")
        self.ids.date.text = today_date


    def on_btn_release(self, btn):
        print(btn.text)
        