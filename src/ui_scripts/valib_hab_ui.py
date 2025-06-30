from functions import *
import json

from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, RoundedRectangle
from kivy.app import App


class ValidHab(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = App.get_running_app()
        with open(resource_path2("data/config.json")) as f:
            config = json.load(f)
        self.user = config["name"]

        # "Completed!" button as described
        self.completed_btn = Button(
            text="Completed!",
            size_hint=(0.4, 0.2),
            font_size='18sp',
            color=self.app.text_color,
            background_color=(0, 0, 0, 0),
            background_normal='',
            pos_hint={"x": 0.55, "y": 0.15},
        )
        self.completed_btn.bind(
            on_release=lambda instance: self.manager.get_screen('main').validate(self.ids.back.text[4:], self.user)
        )
        with self.completed_btn.canvas.before:
            self.bg_color = Color(rgba=self.app.sbutton_color)
            self.bg_rect = RoundedRectangle(pos=self.completed_btn.pos, size=self.completed_btn.size)
        self.completed_btn.bind(pos=self.update_rect, size=self.update_rect)

        self.ids.panel.add_widget(self.completed_btn)

    def update_rect(self, *args):
        self.bg_rect.pos = self.completed_btn.pos
        self.bg_rect.size = self.completed_btn.size


class ValidHabM(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = App.get_running_app()

    #     # "Completed!" button as described
    #     self.completed_btn = Button(
    #         text="Completed!",
    #         size_hint=(0.4, 0.2),
    #         font_size='18sp',
    #         color=self.app.text_color,
    #         background_color=(0, 0, 0, 0),
    #         background_normal='',
    #         pos_hint={"x": 0.55, "y": 0.05},
    #         on_release=self.check()
    #     )
    #     with self.completed_btn.canvas.before:
    #         self.bg_color = Color(rgba=self.app.sbutton_color)
    #         self.bg_rect = RoundedRectangle(pos=self.completed_btn.pos, size=self.completed_btn.size)
    #     self.completed_btn.bind(pos=self.update_rect, size=self.update_rect)

    #     self.add_widget(self.completed_btn)

    # def update_rect(self, *args):
    #     self.bg_rect.pos = self.completed_btn.pos
    #     self.bg_rect.size = self.completed_btn.size

    # def check(self):
    #     pass


