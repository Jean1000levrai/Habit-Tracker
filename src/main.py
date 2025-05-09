import habit_mgr as hmgr
import database as db
import color_picker as col
import webbrowser as web
import json

from addHabitUi import *
from settingsUi import *

from kivy.config import Config
Config.set('graphics', 'width', '360') #1080//3
Config.set('graphics', 'height', '800')#2400//3

from kivy.uix.button import Button
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.properties import ListProperty
from kivy.clock import Clock


class MainWindow(Screen):
    """the main screen window"""
    def __init__(self, **kw):
        super().__init__(**kw)
        info = ''
        app = App.get_running_app()

        # displays all the habits from the db
        # by loop on all the db and displays it with a button
        for row in db.show_habit_for_gui('*'):
            info = f"{row[1]}"
            btn = Button(
                text=f'{info}', 
                background_color=(0, 0, 0, 0), 
                color=app.text_color,
                on_release=(lambda instance: (setattr(self.manager.transition, 'direction', 
                            'left'), setattr(self.manager, 'current', 'info'))),
                halign="left",
                valign="middle",
                text_size=(self.width, None),
                padding=(0, 0)
                )
            
            # binds to the main app the buttons for changing their colors for the themes
            app.bind(text_color=lambda instance, value, b=btn: setattr(b, 'color', value))

            self.ids.labelled_habits.add_widget(btn)

class WelcomePopup(Popup):
    def __init__(self, obj, **kwargs):
        super(WelcomePopup, self).__init__(**kwargs)
        self.obj = obj

class WindowMgr(ScreenManager):
    """handles all the different windows"""
    pass

class MyMainApp(App):
    """MyMainApp is the main application class for the Habit Tracker application. 
    It manages the application's theme, loads the user interface files, and 
    initializes the window manager with different screens."""

    # all the colours
    bg_color = ListProperty([0.051, 0.067, 0.090, 1])
    panel_color = ListProperty([0.086, 0.106, 0.133, 1])
    outline_color = ListProperty([0.129, 0.149, 0.176, 1])
    button_color = ListProperty([0.129, 0.149, 0.176, 1])
    text_color = ListProperty([0.788, 0.820, 0.851, 1])
    big_panel = ListProperty([0, 0, 0, 1 ])  

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_dark = True
        
    def build(self):
        
        # loads the files for all the windows
        Builder.load_file("ui/main.kv")
        Builder.load_file("ui/settings.kv")
        Builder.load_file("ui/add_hab.kv")
        Builder.load_file("ui/habitpopup.kv")
        Builder.load_file("ui/habitInfoWindow.kv")
        Builder.load_file("ui/aboutWindow.kv")
        Builder.load_file("ui/reminderWindow.kv")
        
        # adds them to the window manager
        sm = WindowMgr()
        sm.add_widget(MainWindow(name="main"))
        sm.add_widget(SettingsWindow(name="second"))
        sm.add_widget(AddHabitWindow(name="habYesNo"))
        sm.add_widget(HabitInfoWindow(name="info"))
        sm.add_widget(AboutWindow(name="about"))
        sm.add_widget(ReminderWindow(name="reminder"))

        Clock.schedule_once(self.show_welcome_popup, 0.1)

        return sm
    
    def show_welcome_popup(self, time):
        """method that will be fcalled each time
        the app is launched, if it is the first time
        greet him"""
        # open the config file
        with open("data/config.json") as f:
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

            # greet them with popup
            popup = WelcomePopup(self)
            popup.open()

            # sets it so that next time it wont show the popup
            config["first_timer"] = False
            with open("data/config.json", 'w') as f:
                json.dump(config, f, indent=1)
 
    def popup(self):
        """method that opens the popup"""
        popup = AddHabitPopup(self)
        popup.open()
        
    def popup_time(self):
        popup = DatePopup(self)
        popup.open()

    def popup_date(self):
        popup = TimePopup(self)
        popup.open()

    def dark_theme(self):
        self.bg_color = (0.051, 0.067, 0.090, 1)
        self.panel_color = (0.086, 0.106, 0.133, 1)
        self.outline_color = (0.129, 0.149, 0.176, 1)
        self.text_color = (0.788, 0.820, 0.851, 1)
        self.button_color = (0.129, 0.149, 0.176, 1)
        self.big_panel = (0, 0, 0, 1)

        theme_text = "Theme: Dark"
        settings_screen = self.root.get_screen('second')
        settings_screen.ids.settings_theme.text = theme_text

    def light_theme(self):
        self.bg_color = (0.97, 0.97, 0.97, 1)
        self.panel_color = (0.93, 0.93, 0.93, 1)
        self.outline_color = (0.8, 0.8, 0.8, 1)
        self.text_color = (0.1, 0.1, 0.1, 1)
        self.button_color = (1, 1, 1, 0.5)
        self.big_panel = (0.8, 0.8, 0.8, 1)

        theme_text = "Theme: Light"
        settings_screen = self.root.get_screen('second')
        settings_screen.ids.settings_theme.text = theme_text

    def theme(self):
        """
        Toggles the application's theme between dark mode and light mode.
        """
        # open the config file
        with open("data/config.json") as f:
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
        with open("data/config.json", 'w') as f:
            json.dump(config, f, indent=1)


if __name__=="__main__":
    myapp = MyMainApp()
    myapp.run()