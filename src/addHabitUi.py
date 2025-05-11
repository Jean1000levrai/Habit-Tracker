import habit_mgr as hmgr
import database as db
import color_picker as col
import webbrowser as web

from kivy.uix.button import Button
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.properties import ListProperty


class AddHabitWindow(Screen):
    """the window where you add a habit"""
    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = App.get_running_app()
        self.info = {}
        self.hab = hmgr.HabitYesNo()

    def get_info(self):
        """method that gets the informations from 
        the textinput that the player has filled.
        returns a HabitYesNo containing these infos"""
        # gets the infos into a dic
        self.info["name"] = self.ids.name.text
        self.info["descr"] = self.ids.descr.text
        self.info["qu"] = self.ids.qu.text

        # resets the text inputs
        self.ids.name.text = ""
        self.ids.descr.text = ""
        self.ids.qu.text = ""

        # creates a HabitYesNo with the dic 
        self.hab.name = self.info["name"]
        self.hab.description = self.info["descr"]
        self.hab.question = self.info["qu"]

        return self.hab

    def save_btn(self):
        """method that handles the 'save' button 
        at the bottom of the screen. It updates the
        database with the HabitYesNo and displays it
        on the main screen. prints an error if the input
        isnt correct.""" 
        # try:
        info = self.get_info()
        db.add_habit(info)
        btn = Button(
            text=f'{self.info["name"]}', 
            background_color=(0, 0, 0, 0), 
            color=self.app.text_color,
            on_release=(lambda instance: (setattr(self.manager.transition, 'direction', 
                        'left'), setattr(self.manager, 'current', 'info'))),
            halign="left",
            valign="middle",
            text_size=(self.width, None),
            padding=(132, 0)
            )
        
        # binds the buttons for changing their colors for the themes
        self.app.bind(text_color=lambda instance, value, b=btn: setattr(b, 'color', value))

        # adds the button the display
        self.manager.get_screen("main").ids.labelled_habits.add_widget(btn)
        db.print_table()
        # except:
        #     print("not a valid input")

    def color_selected(self, color):
        self.info["col"] = (str(color))
        self.hab.colour = self.info["col"]

class HabitInfoWindow(Screen):
    """window where the informations of the habit will be displayed"""
    def delete_habit(self):
        name = None
        db.delete_habit(name)


class AddHabitPopup(Popup):
    """popup where the user will be able to
    chose between a yes or no habit or one
    that measures something e g. 'num of pages read'"""
    def __init__(self, obj, **kwargs):
        super(AddHabitPopup, self).__init__(**kwargs)
        self.obj = obj

class ReminderWindow(Screen):
    pass

class DatePopup(Popup):
    def __init__(self, obj, **kwargs):
        super(DatePopup, self).__init__(**kwargs)
        self.obj = obj

class TimePopup(Popup):
    def __init__(self, obj, **kwargs):
        super(TimePopup, self).__init__(**kwargs)
        self.obj = obj