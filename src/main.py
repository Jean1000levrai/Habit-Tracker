from kivy.config import Config
Config.set('graphics', 'width', '360') #1080//3
Config.set('graphics', 'height', '800')#2400//3

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen


class MainWindow(Screen):
    pass

class SettingsWindow(Screen):
    pass

class AddHabitWindow(Screen):
    pass

class WindowMgr(ScreenManager):
    pass


class MyMainApp(App):
    def build(self):
        Builder.load_file("ui/main.kv")
        Builder.load_file("ui/settings.kv")
        Builder.load_file("ui/add_window.kv")
        
        sm = WindowMgr()
        sm.add_widget(MainWindow(name="main"))
        sm.add_widget(SettingsWindow(name="second"))

        return sm


if __name__=="__main__":
    myapp = MyMainApp()
    myapp.run()