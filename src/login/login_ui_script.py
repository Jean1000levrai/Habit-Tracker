import database as db
import login.login_script as li
import functions as fct
import json

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
            # open the config file
            with open(fct.resource_path2("data/config.json")) as f:
                config = json.load(f)
            config["name"] = self.ids.username.text
            with open(fct.resource_path2("data/config.json"), 'w') as f:
                json.dump(config, f, indent=1)
            self.manager.get_screen("main").load_all()
        else:
            self.manager.current = "signup"
    
    def password_show(self):
        if self.ids.pwd_show.text == '':
            self.ids.pwd_show.text = ''
            self.ids.password.password = True
        else:
            self.ids.pwd_show.text = ''
            self.ids.password.password = False


class SignupPage(Screen):
    pass