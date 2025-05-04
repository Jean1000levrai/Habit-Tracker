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

class WindowMgr(ScreenManager):
    pass

kv = Builder.load_file("ui.kv")

class MyMainApp(App):
    def build(self):
        return kv


if __name__=="__main__":
    myapp = MyMainApp()
    myapp.run()