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
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.clock import Clock

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
            self.manager.get_screen("main").empty_hab()
            self.manager.get_screen("main").load_all()
        else:
            self.manager.current = "signup"
        self.ids.username.text = ''
        self.ids.password.text = ''
    
    def password_show(self):
        if self.ids.pwd_show.text == '':
            self.ids.pwd_show.text = ''
            self.ids.password.password = True
        else:
            self.ids.pwd_show.text = ''
            self.ids.password.password = False
    
    def dismiss_func(self):
        self.manager.get_screen("main").load_all()


class SignupPage(Screen):

    def temp_popup(self):
        popup = Popup( 
            title = '',
            separator_height = 0,
            content=Label(text= "successfully signed in!"),
            size_hint=(None, None),
            size=(300, 200),
            auto_dismiss = False
        )

        popup.open()

        Clock.schedule_once(lambda dt: popup.dismiss(), 0.7)



    def signup(self):
        username = self.ids.username.text
        email = self.ids.email.text
        pwd = self.ids.password.text

        self.manager.current = "login"

        db.create_db(username)    
        li.set_info(username, email, pwd)

        self.ids.username.text = ''
        self.ids.email.text = ''
        self.ids.password.text = ''

        self.temp_popup()



