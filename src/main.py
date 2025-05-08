import habit_mgr as hmgr
import database as db
import color_picker as col

from kivy.config import Config
Config.set('graphics', 'width', '360') #1080//3
Config.set('graphics', 'height', '800')#2400//3

from kivy.uix.button import Button
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.properties import ListProperty


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
                            'left'), setattr(self.manager, 'current', 'info')))
                )
            
            # binds to the main app the buttons for changing their colors for the themes
            app.bind(text_color=lambda instance, value, b=btn: setattr(b, 'color', value))

            self.ids.labelled_habits.add_widget(btn)

class SettingsWindow(Screen):
    """the settings window"""
    def __init__(self, **kw):
        super().__init__(**kw)
        self.theme_dark = True

    def theme(self):
        """Toggles the application theme between light and dark modes."""
        """method that changes the button's 
        name according to the themes"""
        if self.theme_dark:
            self.ids.settings_theme.text = "Theme: Light"
            self.theme_dark = False
        else:
            self.ids.settings_theme.text = "Theme: Dark"
            self.theme_dark = True

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
            color= self.app.text_color,
            on_release=(lambda instance: (setattr(self.manager.transition, 'direction', 
                            'left'), setattr(self.manager, 'current', 'info')))
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
    pass

class AddHabitPopup(Popup):
    """popup where the user will be able to
    chose between a yes or no habit or one
    that measures something e g. 'num of pages read'"""
    def __init__(self, obj, **kwargs):
        super(AddHabitPopup, self).__init__(**kwargs)
        self.obj = obj

class WindowMgr(ScreenManager):
    """handles all the different windows"""
    pass

class MyMainApp(App):
    class MyMainApp:
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
        
        # adds them to the window manager
        sm = WindowMgr()
        sm.add_widget(MainWindow(name="main"))
        sm.add_widget(SettingsWindow(name="second"))
        sm.add_widget(AddHabitWindow(name="habYesNo"))
        sm.add_widget(HabitInfoWindow(name="info"))

        return sm
    
    def popup(self):
        """method that opens the popup"""
        popup = AddHabitPopup(self)
        popup.open()

    def theme(self):
        """
        Toggles the application's theme between dark mode and light mode.
        """
        # light mode
        if self.theme_dark:
            self.theme_dark = False
        
            self.bg_color = (0.97, 0.97, 0.97, 1)
            self.panel_color = (0.93, 0.93, 0.93, 1)
            self.outline_color = (0.8, 0.8, 0.8, 1)
            self.text_color = (0.1, 0.1, 0.1, 1)
            self.button_color = (1, 1, 1, 0.5)
            self.big_panel = (0.8, 0.8, 0.8, 1)

        # dark mode
        else:
            self.theme_dark = True

            self.bg_color = (0.051, 0.067, 0.090, 1)
            self.panel_color = (0.086, 0.106, 0.133, 1)
            self.outline_color = (0.129, 0.149, 0.176, 1)
            self.text_color = (0.788, 0.820, 0.851, 1)
            self.button_color = (0.129, 0.149, 0.176, 1)
            self.big_panel = (0, 0, 0, 1)



if __name__=="__main__":
    myapp = MyMainApp()
    myapp.run()