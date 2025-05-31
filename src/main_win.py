# scripts
import habit_mgr as hmgr
import database as db
from functions import *

from login.login_script import *
from login.login_ui_script import *


class MainWindow(Screen):
    """the main screen window"""
    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = App.get_running_app()
        self.hab_name = ''
        self.lst_btn = []
        self.lst_btn_check = {}
        self.load_all()

    def empty_hab(self):
        layout = self.ids.labelled_habits
        # clears habits
        for btn in self.lst_btn:
            if btn.parent:
                layout.remove_widget(btn)
        self.lst_btn.clear()
        # clears check boxes
        for cb in self.lst_btn_check:
            if cb.parent:
                layout.remove_widget(cb)
        self.lst_btn_check.clear()

    def load_all(self):
        # open the config file
        with open(resource_path2("data/config.json")) as f:
            config = json.load(f)
        self.user = config["name"]

        # displays the name of the user at the top
        self.ids.title_app.text = self.user

        # displays all the habits from the db
        # by loop on all the db and displays it with a button
        for row in db.show_habit_for_gui('*',self.user):
            info = f"{row[1]}"
            btn = Button(
                text=f'{info}', 
                size_hint_x=0.8,         # makes the btn expand correctly, according to smart people
                size_hint_y=None,
                height=60,
                background_color=(0, 0, 0, 0),
                color=self.app.text_color,
                halign="left",
                valign="middle",
                text_size=(0, None),
                padding=(10, 10)
            )
            btn_check = [Button(
                font_name="FontAwesome",
                text="  ",
                on_release=self.check,
                size_hint_x=0.2,
                size_hint_y=None,
                height=60,
                background_color=(0, 0, 0, 0),
                valign="middle",
                halign="center",
                padding=(0, 0), 
                text_size=(0, None),
            ),
            False]
            
            btn.bind(width=lambda instance, value: setattr(instance, 'text_size', (value, None)))
            btn_check[0].bind(size=lambda instance, value: setattr(instance, 'text_size', value))
            
            self.lst_btn.append(btn)
            self.lst_btn_check[btn_check[0]] = btn_check[1]

            self.app.bind(text_color=lambda instance, value, b=btn: setattr(b, 'color', value))
            self.ids.labelled_habits.add_widget(btn)
            self.ids.labelled_habits.add_widget(btn_check[0])
            btn.bind(on_release=self.on_btn_release)

    def check(self, instance):
        if self.lst_btn_check[instance]:
            instance.text = "  "
            self.lst_btn_check[instance] = False
            
        else:
            instance.text = "  "
            self.lst_btn_check[instance] = True

    def on_btn_release(self, instance):
        # recovers the name of the clicked btn
        self.hab_name = instance.text
        print(self.hab_name)

        self.add_the_info()

        # handles the window change
        self.manager.transition.direction = "left"
        self.manager.current = "info"

    def add_the_info(self):

        self.manager.get_screen("info").ids.name_of_the_hab.text = f"<- {self.hab_name}"
        question = db.get_info_hab(self.hab_name, "question", self.user)
        self.manager.get_screen("info").ids.qu_for_hab.text = question

        descr = db.get_info_hab(self.hab_name, "description", self.user)
        self.manager.get_screen("info").ids.descr_for_hab.text = str(descr)

        reminder = db.get_info_hab(self.hab_name, "reminder", self.user)
        self.manager.get_screen("info").ids.rem_for_hab.text = str(reminder)

        frequency = db.get_info_hab(self.hab_name, "frequency", self.user)
        self.manager.get_screen("info").ids.freq_for_hab.text = str(frequency)

class WelcomePopup(Popup):
    def __init__(self, obj, **kwargs):
        super(WelcomePopup, self).__init__(**kwargs)
        self.obj = obj
    
    def set_name(self):
        name = self.ids.set_name.text

        # open the config file
        with open("data/config.json") as f:
            config = json.load(f)

        config["name"] = name

        # update the data
        with open("data/config.json", 'w') as f:
            json.dump(config, f, indent=1)

class WindowMgr(ScreenManager):
    """handles all the different windows"""
    pass
