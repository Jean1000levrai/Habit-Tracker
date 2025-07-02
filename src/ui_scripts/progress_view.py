import json
from datetime import *

import database as db
from functions import *
from const import user_const

from kivy.uix.button import Button
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle



class VibrantGridButton(Button):
    def __init__(self, border_color=(0, 0, 0, 1), fill_color=(0, 1, 0, 1), **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)  # Transparent, we use canvas
        with self.canvas.before:
            # Border
            Color(*border_color)
            self.border_rect = RoundedRectangle(pos=self.pos, size=self.size)
            # Fill
            Color(*fill_color)
            self.fill_rect = RoundedRectangle(pos=(self.x+2, self.y+2), size=(self.width-4, self.height-4))
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.border_rect.pos = self.pos
        self.border_rect.size = self.size
        self.fill_rect.pos = (self.x+2, self.y+2)
        self.fill_rect.size = (self.width-4, self.height-4)

class ProgressViewWindow(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = App.get_running_app()
        with open(resource_path2("data/config.json")) as f:
            config = json.load(f)
        streak = config["streak"]
        self.calendar()
        if streak <= 1:
            self.ids.streak.text = self.ids.streak.text + str(streak) + " Day"
        else:
            self.ids.streak.text = self.ids.streak.text + str(streak) + " Days"

    def reload(self):
        grid = self.ids.table_grid
        grid.clear_widgets()
        self.calendar()

    def calendar(self):
        # Load config
        with open(resource_path2("data/config.json")) as f:
            config = json.load(f)
        self.user = user_const()

        # Get all habits and dates
        habits = db.get_all_habits(self.user)  # list : (id, name)
        dates = db.get_all_dates(self.user)    # list : date 

        nb_hab = len(habits)
        nb_date = len(dates)

        # set up the grid
        grid = self.ids.table_grid
        grid.clear_widgets()

        x_hab = 40
        x_date = 100
        y_all = 40

        grid.cols = nb_hab + 1  # habits as columns (+1 for date labels)
        grid.rows = nb_date + 1  # dates as rows (+1 for top header)
        grid.size_hint = (None, None)
        grid.width = (nb_hab + 1) * x_hab
        grid.height = (nb_date + 1) * y_all

        # --- Top-left cell empty ---
        grid.add_widget(Button(text='', size_hint=(None, None), size=(x_date, y_all),
                            background_color=(0, 0, 0, 0), disabled=True))

        # --- Top row: habit names ---
        for _, habit_name in habits:
            grid.add_widget(Button(text=habit_name[:4], 
                                    size_hint=(None, None), 
                                    size=(x_hab, y_all),
                                    background_color=(0.1, 0.1, 0.1, 1), color=(1, 1, 1, 1),
                                    disabled=True))

        # --- Date rows ---
        for date in dates:

            # First column: the date
            grid.add_widget(Button(text=date, 
                                size_hint=(None, None), size=(x_date, y_all),
                                background_color=(0.1, 0.1, 0.1, 1), color=(1, 1, 1, 1),
                                disabled=True))

            habs_date = db.habits_has_date(date, self.user)    # list of the habits with this date in logs
            # --- Fills the table ---
            # loops on all the existing habits 
            for hab in habits:
                # if the hab has a date in log: red or green
                if hab[1] in habs_date:

                    hab_id = db.get_info_hab(hab[1], 'id', self.user)

                    if db.check_log(hab_id, date, self.user):
                        color = (0, 1, 0, 1)
                    else:
                        color = (1, 0, 0, 1)
                    grid.add_widget(VibrantGridButton(
                        fill_color=color,   # Red or green   
                        size_hint=(None, None),
                        size=(x_hab, y_all),
                        text=""
                        ))
                # gray if no date in logs
                else:
                    grid.add_widget(VibrantGridButton(
                        fill_color=(0.3, 0.3, 0.3, 1),  # dark gray
                        size_hint=(None, None),
                        size=(x_hab, y_all),
                        text=""
                        ))