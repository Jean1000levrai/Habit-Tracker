import webbrowser as web

from kivy.uix.button import Button
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.properties import ListProperty


class SettingsWindow(Screen):
    """the settings window"""
    def __init__(self, **kw):
        super().__init__(**kw)
        self.theme_dark = True

    def link_github(self):
        link = 'https://github.com/Jean1000levrai/Habit-Tracker'
        web.open(link)

class AboutWindow(Screen):
    pass
