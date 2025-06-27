import habit_mgr as hmgr
import database as db
import ui_scripts.color_picker as col
import webbrowser as web
import calendar as cldr
from datetime import datetime, timedelta

from functions import *
import json
import database as db

from kivy.uix.button import Button
from kivy.app import App
from kivy.uix.screenmanager import Screen


class CalendarScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = App.get_running_app()
        
        # data to be used to ease the dev
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
        # dict to store the btns
        self.days_btn = {}
        self.hours_btn = {}
        # var to store the current time
        self.current_btn = datetime.today().strftime("%A")
        self.current_day = datetime.today().strftime("%A")
        self.current_date = datetime.today().strftime("%d-%m-%Y")
        self.current_now = datetime.today()
        

        # open the config file
        with open(resource_path2("data/config.json")) as f:
            config = json.load(f)
        self.user = config["name"]

        # initialize the calendar a first time
        self.sets_every_day()
        self.sets_day(self.current_day, self.current_date)
        self.sets_every_hours()


    def _update_button_bg(self, btn):
        def update(_, value):
            btn.background_color = value
        return update

    def _update_button_fg(self, btn):
        def update(_, value):
            btn.color = value
        return update
    
#----------the hours btns----------
    def sets_every_hours(self):
        """method that initializes all the hours of the calendar
        and stores it in a dict"""
        # adds every hours as a btn 
        for j in range(24):
            # creates the btn
            # the hours indicator
            btn1 = Button(
                text = f"{j} : 00",

                background_color=(0,0,0,0),
                background_normal = '',
                color=self.app.text_color,
                size_hint_x = None,
                width = 90,
            )
            #  where the habits will be shown
            btn2 = Button(
                text = "",

                background_color=self.app.button_color,
                background_normal = '',
                color=self.app.text_color,
            )

            # Bind color updates
            self.app.fbind('button_color', self._update_button_bg(btn2))
            self.app.fbind('text_color', self._update_button_fg(btn2))
            # adds it
            self.ids.calendar_square.add_widget(btn1)
            self.ids.calendar_square.add_widget(btn2)
            # stores it
            self.hours_btn[btn1.text] = btn2

    def delete_every_hours(self):
        """method that deletes all the hours
        used to reset when changing days for 
        example. sets_every_hours() needs to be called 
        right after."""
        pass

# ----------the days btns----------
    def sets_every_day(self):
        """methods that creates all the days btn"""
        # adds every days as a btn
        for i in range(7):
            # creates the btn
            btn = Button(
                text = str(self.days[i]),
                pos_hint= {'right': 0.16 + i*0.13,'top': 0.3},
                size_hint_x = None,
                size_hint_y = None,
                width = 40,
                height = 40,
                background_color=self.app.button_color,
                background_normal = '',
                color=self.app.text_color,
            )

            # Bind color updates
            self.app.fbind('button_color', self._update_button_bg(btn))
            self.app.fbind('text_color', self._update_button_fg(btn))

            # stores it (accessible through full name or abrevietion)
            # e.g. 'M' or "Monday"
            self.days_btn[self.id_days[i]] = btn
            self.days_btn[self.days[i]] = btn

            # adds it and binds it
            self.ids.top_panel_cal.add_widget(btn)
            btn.bind(on_release=lambda instance, b=btn: self.on_btn_release(b, instance))

    def sets_day(self, today_day, today_date):
        """method that selects one day and put in green"""  
        self.days_btn[today_day].background_color = (0, 0.5, 0, 1)
        self.ids.date.text = today_date

    def delete_every_day(self):
        """method that deletes all the 
        day btns. useful when you want to put one btn
        in green when selected an dont want to have duplicates
        need to call sets_every_day() right after"""
        layout = self.ids.top_panel_cal
        # clears days
        for day in self.days_btn.values():
            if day.parent:      # checks if it has a parent to be sure it is a btn and not someting else
                layout.remove_widget(day)
        self.days_btn.clear()   #clears trhe dict where the btns are stored

    def day_forward(self, nb=1):
        """methods that changes the day according to
        the user input, default skip a day."""
        # skips the nb days that the users want
        self.current_now = self.current_now + timedelta(days=nb)
        self.current_date = self.current_now.strftime("%d-%m-%Y")
        self.current_day = self.current_now.strftime("%A")

        # updates with the methods we ve created
        self.delete_every_day()
        self.sets_every_day()
        self.sets_day(self.current_day, self.current_date)

        self.current_btn = self.current_day # keeps the current selected btn in memory

    def on_btn_release(self, btn, instance):
        """method called when a btn day is pressed
        skips to the according day"""
        self.current_day = btn.text
        minus = self.days_to_monday[self.current_btn]
        self.current_btn = self.current_day
        cur = self.days_to_monday[self.current_day]
        # the current day to monday - the day clicked to monday
        # e.g. (th = 3) - (su = 6) = -3 the time to skip to be up to date
        self.day_forward(cur - minus)
    
    def add_hab_cal(self, day):
        """method that adds a habit in the calendar
        according to what is in the db"""
        # open the config file
        with open(resource_path2("data/config.json")) as f:
            config = json.load(f)
        self.user = config["name"]

        
