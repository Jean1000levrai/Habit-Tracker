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
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label


class ReminderWindow(Screen):
    def date_popup(self):
        popup = DatePopup(self)
        popup.open()
    
    def time_popup(self):
        popup = TimePopup(self)
        popup.open()

    def save(self):
        print('nothin is saved bruuhh')

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
        self.next()
        self.time = "00:00:00"
        self.time_tab = []

    def get_time(self, instance, time):
        global reminder_var
        self.time = str(time)
        self.time_tab.append(str(time))
        print(time)

        # Change the text of the button that was clicked
        if hasattr(self, 'current_btn') and self.current_btn:
            self.current_btn.text = str(time)

    def next1(self, instance):
        self.current_btn = instance  # Store the button that was clicked
        popup = MDTimePicker()
        popup.bind(on_save=self.get_time)
        popup.open()
    
    def day_next(self, instance):
        if not self.btn_days[instance.text[:-2]][1]:
            instance.text = instance.text[:-2] + " "
            self.btn_days[instance.text[:-2]][1] = True
            
        else:
            instance.text = instance.text[:-2] + " "
            self.btn_days[instance.text[:-2]][1] = False
            
        print(self.btn_days[instance.text[:-2]][1])

    def next(self):
        global reminder_var
        reminder_var[2] = []
        self.btn = {}
        self.btn_days = {}

        # ------time------
        times = self.parent_screen.ids.times.text         # gets the nb of times

        container = self.ids.time_select
        container.clear_widgets()   # clears to not stack if opened more than once

        try:
            n = int(times)
        except (ValueError, TypeError):
            n = 0
        if n>6:
            n=6
        # add the btns
        for i in range(n):
            self.btn[str(i)] = Button(text="00:00:00",
                         size_hint_y = None,
                         height = 40,
                         on_release = self.next1) 
            container.add_widget(self.btn[str(i)])
        
        # ------date------
        if self.parent_screen.ids.date_popup.text == "Weekly":
                    days = ['M', 'T', 'W', 'T H', 'F', 'S', 'S u']
                    self.container_days = self.ids.days_select
                    for day in days:
                        #  uncheck /  check
                        self.btn_days[day] = [Button(
                            font_name= "FontAwesome",
                            text = f"{day} ",
                            on_release = self.day_next
                        ),
                        False]
                        self.container_days.add_widget(self.btn_days[day][0])

    def save(self):
        global reminder_var

        # update the var holding the value
        # time  
        reminder_var[2].extend(self.time_tab)
        while len(reminder_var[2]) != int(self.parent_screen.ids.times.text):
            reminder_var[2].append("00:00:00")

        # times
        reminder_var[0] = self.parent_screen.ids.times.text

        # frequency
        reminder_var[1] = self.parent_screen.ids.date_popup.text

        # days
        i = 0
        for day in self.btn_days:
            reminder_var[3][i] = self.btn_days[day][1]
            i = i + 1

        print(reminder_var)

        
    def dismiss_1(self):
        global reminder_var
        reminder_var[2] = []


reminder_var = [0, "Daily", [], [False, False, False, False, False, False, False]]