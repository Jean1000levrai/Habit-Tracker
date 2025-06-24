# scripts
import habit_mgr as hmgr
import database as db
from functions import *

from login.login_script import *
from login.login_ui_script import *

from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle, RoundedRectangle


class HabitRow(BoxLayout):
    def __init__(self, habit_name, app, on_btn_release, dell, details_btn_release, **kwargs):
        super().__init__(orientation='horizontal', size_hint_y=None, height=60, **kwargs)
        self.app = app
        self.habit_name = habit_name

        # Background
        with self.canvas.before:
            self.bg_color = Color(app.button_color)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)
        self.set_background_color(app.button_color )

        # Main text button
        self.btn = Button(
            text=habit_name,
            size_hint_x=0.7,
            size_hint_y=1,
            background_color=(0, 0, 0, 0),
            color=app.text_color,
            halign="left",
            valign="middle",
            padding=(10, 10),
            text_size=(0, None)
        )
        self.btn.bind(width=self._update_text_size)

        # delete button
        self.btn_dell = Button(
            font_name="FontAwesome",
            text=" X ",
            size_hint_x=0.1,
            size_hint_y=None,
            height=30,
            width=50,
            background_color=(0.8, 0.2, 0.3, 1),
            background_normal='',
            halign="center",
            valign="middle",
            pos_hint={"center_y": 0.5}
        )
        self.btn_dell.bind(size=self._update_text_size)

        # Details/edit button
        self.btn_detail = Button(
            font_name="FontAwesome",
            text="",
            size_hint_x=0.2,
            size_hint_y=1,
            background_color=(0, 0, 0, 0),
            color=app.text_color,
            halign="center",
            valign="middle"
        )

        # Re-bind color changes from app
        app.bind(button_color=lambda _, value: setattr(self.bg_color, 'rgba', value))
        app.bind(text_color=lambda _, value: setattr(self.btn, 'color', value))
        app.bind(text_color=lambda _, value: setattr(self.btn_detail, 'color', value))

        # Events
        self.btn.bind(on_release=on_btn_release)
        self.btn_dell.bind(on_release=dell)
        self.btn_detail.bind(on_release=details_btn_release)

        # Add buttons
        self.add_widget(self.btn)
        self.add_widget(self.btn_detail)
        self.add_widget(self.btn_dell)

    def update_rect(self, *_):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def _update_text_size(self, instance, _):
        instance.text_size = (instance.width, None)
    
    def set_background_color(self, rgba):
        """Update background color dynamically."""
        self.bg_color.rgba = rgba

class MainWindow(Screen):
    """the main screen window"""
    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = App.get_running_app()
        self.hab_name = ''
        self.lst_btn = []
        self.lst_bg_btn = []
        self.lst_btn_dell = []
        self.lst_btn_details = []
        self.load_all()

    def empty_hab(self):
        layout = self.ids.labelled_habits

        layout.remove_widget(self.add)
        for btn in self.lst_bg_btn:
            if btn.parent:
                layout.remove_widget(btn)
        self.lst_btn.clear()
        self.lst_bg_btn.clear()
        self.lst_btn_dell.clear()
        self.lst_btn_details.clear()

    def load_all(self):
        # open the config file
        with open(resource_path2("data/config.json")) as f:
            config = json.load(f)
        self.user = config["name"]

        # displays the name of the user at the top
        self.ids.title_app.text = self.user

        # adds the default height of the scrollview
        self.ids.labelled_habits.height = 0

        # displays all the habits from the db
        # by loop on all the db and displays it with a button
        for row in db.show_habit_for_gui('*',self.user):

            habit_name = row[1]

            habit_row = HabitRow(habit_name, self.app, self.on_btn_release, self.delete_habit, self.details_btn_release)

            # Store references (optional)
            self.lst_btn.append(habit_row.btn)
            self.lst_btn_dell.append(habit_row.btn_dell)
            self.lst_btn_details.append(habit_row.btn_detail)
            self.lst_bg_btn.append(habit_row)

            self.ids.labelled_habits.add_widget(habit_row)
            self.ids.labelled_habits.height += habit_row.height
        self.add = Button(text="ADD",
            size_hint_x=None,
            size_hint_y=None,
            height = 50,
            width = 100,
            background_color=self.app.sbutton_color,
            background_normal = '',
            color=self.app.text_color,
            halign="left",
            valign="middle",
            padding=(10, 10),
            pos_hint={"center_x": 0.5},
            on_release=self.app.popup
            )
        
        self.app.bind(text_color=lambda _, value: setattr(self.add, 'color', value))
        self.ids.labelled_habits.add_widget(self.add)
        self.ids.labelled_habits.height += self.add.height

    def delete_habit(self, instance):
        # open the config file
        with open(resource_path2("data/config.json")) as f:
            config = json.load(f)

        hab_name = instance.parent.btn.text
        print(hab_name)
        db.delete_habit(hab_name, config["name"])
        
        self.manager.get_screen("main").empty_hab()
        self.manager.get_screen("main").load_all()

    def check(self, instance):
        if self.lst_btn_dell[instance]:
            instance.text = "  "
            self.lst_btn_dell[instance] = False
            
        else:
            instance.text = "  "
            self.lst_btn_dell[instance] = True

    def on_btn_release(self, instance):
        print("checking in process ...")

    def details_btn_release(self, instance):
        # recovers the name of the clicked btn
        self.hab_name = instance.parent.btn.text
        print(instance.parent.btn.text)

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

class SureDelPopup(Popup):
    pass

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

