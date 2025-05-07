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


class MainWindow(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        info = ''
        for row in db.show_habit_for_gui('*'):
            info = f"{row[1]}"
            btn = Button(text=f'{info}', background_color=(0, 0, 0, 0))
            self.ids.labelled_habits.add_widget(btn)

class SettingsWindow(Screen):
    pass

class AddHabitWindow(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.info = {}
        self.hab = hmgr.HabitYesNo()

    def get_info(self):
        self.info["name"] = self.ids.name.text
        self.info["descr"] = self.ids.descr.text
        self.info["qu"] = self.ids.qu.text

        self.ids.name.text = ""
        self.ids.descr.text = ""
        self.ids.qu.text = ""

        self.hab.name = self.info["name"]
        self.hab.description = self.info["descr"]
        self.hab.question = self.info["qu"]

        return self.hab

    def save_btn(self):   
        # try:
        info = self.get_info()
        db.add_habit(info)
        btn = Button(text=f'{self.info["name"]}', background_color=(0, 0, 0, 0))
        self.manager.get_screen("main").ids.labelled_habits.add_widget(btn)
        db.print_table()
        # except:
        #     print("not a valid input")

    def color_selected(self, color):
        self.info["col"] = (str(color))
        self.hab.colour = self.info["col"]

class HabitInfoWindow(Screen):
    pass

class AddHabitPopup(Popup):
    def __init__(self, obj, **kwargs):
        super(AddHabitPopup, self).__init__(**kwargs)
        self.obj = obj

class WindowMgr(ScreenManager):
    pass

class MyMainApp(App):
    def build(self):
        Builder.load_file("ui/main.kv")
        Builder.load_file("ui/settings.kv")
        Builder.load_file("ui/add_hab.kv")
        Builder.load_file("ui/habitpopup.kv")
        Builder.load_file("ui/habitInfoWindow.kv")
        
        sm = WindowMgr()
        sm.add_widget(MainWindow(name="main"))
        sm.add_widget(SettingsWindow(name="second"))
        sm.add_widget(AddHabitWindow(name="habYesNo"))
        sm.add_widget(HabitInfoWindow(name="info"))

        return sm
    
    def popup(self):
        popup = AddHabitPopup(self)
        popup.open()

        
if __name__=="__main__":
    myapp = MyMainApp()
    myapp.run()