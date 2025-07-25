# file size
from kivy.config import Config
Config.set('graphics', 'width', '360') #1080//3
Config.set('graphics', 'height', '800')#2400//3

# basic libraries
import webbrowser as web
import json
from plyer import notification

# scripts
import habit_mgr as hmgr
import database as db
from functions import *
from main_win import *
from streak import streak
from const import user_const

from login.login_script import *
from login.login_ui_script import *

import ui_scripts.color_picker as col
from ui_scripts.reminder import *
from ui_scripts.addHabitUi import *
from ui_scripts.settingsUi import *
from ui_scripts.addHabitUi import *
from ui_scripts.calendar_script import *
from ui_scripts.addHabMUi import *
from ui_scripts.progress_view import *
from ui_scripts.valib_hab_ui import *
from ui_scripts.develop_mode import *

# ui utilities
from kivy.uix.button import Button
from kivy.core.text import LabelBase
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.properties import ListProperty
from kivy.lang import Builder
from kivy.clock import Clock

from kivy.app import App
from kivymd.app import MDApp



LabelBase.register(
    name="FontAwesome",
    fn_regular=resource_path2("assets/fonts/fa-solid.otf")
)

# notification.notify(
#     title='Habit Reminder',
#     message='Time to log your habit!',
#     timeout=5
# )


class WindowMgr(ScreenManager):
    """handles all the different windows"""
    pass

class App(MDApp):
    """MyMainApp is the main application class for the Habit Tracker application. 
    It manages the application's theme, loads the user interface files, and 
    initializes the window manager with different screens."""

    # all the colours
    bg_color = ListProperty([0.051, 0.067, 0.090, 1])
    panel_color = ListProperty([0.086, 0.106, 0.133, 1])
    outline_color = ListProperty([0.129, 0.149, 0.176, 1])
    back_btn_color = ListProperty([0, 0, 0, 1])
    button_color = ListProperty([0.129, 0.149, 0.176, 1])
    sbutton_color = ListProperty([0.1176, 0.5333, 0.898, 1.0])
    text_color = ListProperty([0.788, 0.820, 0.851, 1])
    big_panel = ListProperty([0, 0, 0, 1])  

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_dark = True
        # open the config file
        with open(resource_path2("data/config.json")) as f:
            config = json.load(f)
        db.create_new_day(config['name'])
        streak()
        
    def build(self):
    
        # loads the files for all the windows
        Builder.load_file(resource_path("ui/main/main.kv"))
        Builder.load_file(resource_path("ui/main/add_hab.kv"))
        Builder.load_file(resource_path("ui/main/reminderWindow.kv"))
        Builder.load_file(resource_path("ui/main/add_hab_m.kv"))
        Builder.load_file(resource_path("ui/main/valid_hab.kv"))
        Builder.load_file(resource_path("ui/settings/settings.kv"))
        Builder.load_file(resource_path("ui/settings/aboutWindow.kv"))
        Builder.load_file(resource_path("ui/settings/devmode.kv"))
        Builder.load_file(resource_path("ui/popup/habitpopup.kv"))
        Builder.load_file(resource_path("ui/popup/popupsForReminder.kv"))
        Builder.load_file(resource_path("ui/login_ui/login_page.kv"))
        Builder.load_file(resource_path("ui/login_ui/signup.kv"))
        Builder.load_file(resource_path("ui/calendar/calendar_ui.kv"))
        Builder.load_file(resource_path("ui/calendar/progress_view.kv"))
        
        # adds them to the window manager
        sm = WindowMgr()
        # open the config file
        with open(resource_path2("data/config.json")) as f:
            config = json.load(f)
        if config["first_timer"] == True:
            sm.add_widget(LoginPage(name="login"))
            sm.add_widget(MainWindow(name="main"))
        else:
            sm.add_widget(MainWindow(name="main"))
            sm.add_widget(LoginPage(name="login"))
        sm.add_widget(DevModeScreen(name="devmode"))
        sm.add_widget(ValidHab(name="validHab"))
        sm.add_widget(ValidHabM(name="validHabM"))
        sm.add_widget(ReminderWindow(name="reminder"))  
        sm.add_widget(CalendarScreen(name="calendar"))
        sm.add_widget(SettingsWindow(name="second"))
        sm.add_widget(AddHabitWindow(name="habYesNo"))
        sm.add_widget(AboutWindow(name="about"))
        sm.add_widget(SignupPage(name="signup"))
        sm.add_widget(AddHabitMeasScreen(name="habMeasurable"))
        sm.add_widget(ProgressViewWindow(name="progress_view"))

        self.theme_cls.theme_style = "Dark"

        Clock.schedule_once(self.show_welcome_popup, 0.1)

        return sm
    
    def show_welcome_popup(self, time):
        """method that will be fcalled each time
        the app is launched, if it is the first time
        greet him"""
        # open the config file
        with open(resource_path2("data/config.json")) as f:
            config = json.load(f)
        
        # sets the current theme
        if config["theme"] == "dark":
            self.dark_theme()           
        else:
            self.light_theme()


        # checks if it is they first time here
        if config["first_timer"] == True:
            # creates the db
            db.create_db()

            # sets it so that next time it wont show the popup
            config["first_timer"] = False
            with open(resource_path2("data/config.json"), 'w') as f:
                json.dump(config, f, indent=1)
 
    def popup(self, *args):
        """method that opens the popup to add a habit"""
        popup = AddHabitPopup(self)
        popup.open()

    def dark_theme(self):
        """method that changes the theme to dark"""
        self.theme_cls.theme_style = "Dark"

        self.bg_color = (0.051, 0.067, 0.090, 1)
        self.panel_color = (0.086, 0.106, 0.133, 1)
        self.outline_color = (0.129, 0.149, 0.176, 1)
        self.button_color  = (0.1, 0.1, 0.1, 1)
        self.text_color = (0.788, 0.820, 0.851, 1)
        self.sbutton_color = (0.27, 0.37, 0.70, 1)
        self.back_btn_color = (0, 0, 0, 1)
        self.big_panel = (0, 0, 0, 1)

        theme_text = "Theme: Dark"
        settings_screen = self.root.get_screen('second')
        settings_screen.ids.settings_theme.text = theme_text

        self.root.get_screen('main').empty_hab()
        self.root.get_screen('main').load_all()

    def light_theme(self):
        """method that changes the theme to light"""
        self.theme_cls.theme_style = "Light"

        self.bg_color = (0.95, 0.96, 0.98, 1)
        self.panel_color = (0.93, 0.94, 0.96, 1)
        self.outline_color = (0.78, 0.80, 0.85, 1)
        self.button_color = (0.78, 0.80, 0.85, 1)
        self.sbutton_color = (0.0, 0.478, 0.757, 1.0)
        self.text_color = (0.1, 0.1, 0.1, 1)
        self.back_btn_color = (0.9, 0.9, 0.9,)
        self.big_panel = (1, 1, 1, 1)

        theme_text = "Theme: Light"
        settings_screen = self.root.get_screen('second')
        settings_screen.ids.settings_theme.text = theme_text

        self.root.get_screen('main').empty_hab()
        self.root.get_screen('main').load_all()

    def theme(self):
        """
        Toggles the application's theme between dark mode and light mode.
        """
        # open the config file
        with open(resource_path2("data/config.json")) as f:
            config = json.load(f)

        # light mode
        if config["theme"] == "dark":
            config["theme"] = "light"
        
            self.light_theme()

        # dark mode
        else:
            config["theme"] = "dark"

            self.dark_theme()

        # updates the config file
        with open(resource_path2("data/config.json"), 'w') as f:
            json.dump(config, f, indent=1)

    def push_notif(self, hab, question):
        notification.notify(title=str(hab), message=question, timeout=10)


if __name__=="__main__":
    myapp = App()
    myapp.run()