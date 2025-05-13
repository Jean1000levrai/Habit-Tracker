import database as db
import login.login_script as li

from kivy.uix.button import Button
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.properties import ListProperty

class LoginPage(Screen):
    def login(self):
        username = self.ids.username.text
        pwd = self.ids.password.text
        if li.test_log(username, pwd):
            self.manager.current = "main"
        else:
            self.manager.current = "signup"

class SignupPage(Screen):
    pass