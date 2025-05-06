import habit_mgr as hmgr
import database as db

from kivy.config import Config
Config.set('graphics', 'width', '360') #1080//3
Config.set('graphics', 'height', '800')#2400//3

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup


class MainWindow(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        print("it works")

class SettingsWindow(Screen):
    pass

class AddHabitWindow(Screen):

    def get_info(self):
        info = []
        info.append(self.ids.name.text)
        info.append(self.ids.descr.text)
        info.append(self.ids.qu.text)
        info.append(self.ids.col.text)

        self.ids.name.text = ""
        self.ids.descr.text = ""
        self.ids.qu.text = ""
        self.ids.col.text = ""

        hab = hmgr.HabitYesNo()
        hab.name = info[0]
        hab.description = info[1]
        hab.question = info[2]
        hab.colour = info[3]

        return hab

    def save_btn(self):
        try:
            info = self.get_info()
            db.add_habit(info)
            db.print_table()
        except:
            print("not a valid input")

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
        
        sm = WindowMgr()
        sm.add_widget(MainWindow(name="main"))
        sm.add_widget(SettingsWindow(name="second"))
        sm.add_widget(AddHabitWindow(name="habYesNo"))

        return sm
    
    def popup(self):
        popup = AddHabitPopup(self)
        popup.open()
        

        
if __name__=="__main__":
    myapp = MyMainApp()
    myapp.run()
    print(db.show_habit_for_gui("eat"))