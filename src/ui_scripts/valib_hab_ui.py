from functions import *
import json
import database as db
from const import user_const

from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, RoundedRectangle
from kivy.app import App


class ValidHab(Screen):

    def on_enter(self):
        self.user = user_const()

    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = App.get_running_app()
        with open(resource_path2("data/config.json")) as f:
            config = json.load(f)
        self.user = user_const()
        self.current_hab_name = ''

        

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
            on_release=lambda instance: self.manager.get_screen('main').validate(self.current_hab_name, self.user)
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
        with open(resource_path2("data/config.json")) as f:
            config = json.load(f)
        self.user = user_const()
        self.current_hab_name = ''
        self.current_threshold = ''
        self.current_unit = ''

        self.completed_btn = Button(
            text="Completed!",
            size_hint=(0.4, 0.2),
            font_size='18sp',
            color=self.app.text_color,
            background_color=(0, 0, 0, 0),
            background_normal='',
            pos_hint={"x": 0.55, "y": 0.15},
        )

        def v(instance):
            try:
                if self.current_threshold <= int(self.ids.quant_input.text):
                    self.manager.get_screen('main').validate(self.current_hab_name, self.user)
            except:None
            self.manager.get_screen('main').validate(self.current_hab_name, self.user, yes=False)
            hab_id = db.get_info_hab(self.current_hab_name, 'id', user=self.user)
            db.update_quantity(hab_id, quantity=float(self.ids.quant_input.text))
            self.ids.quant_input.text = ''

        self.completed_btn.bind(
            on_release=v
        )
        with self.completed_btn.canvas.before:
            self.bg_color = Color(rgba=self.app.sbutton_color)
            self.bg_rect = RoundedRectangle(pos=self.completed_btn.pos, size=self.completed_btn.size)
        self.completed_btn.bind(pos=self.update_rect, size=self.update_rect)

        self.ids.panel.add_widget(self.completed_btn)

    def update_rect(self, *args):
        self.bg_rect.pos = self.completed_btn.pos
        self.bg_rect.size = self.completed_btn.size

    def clear(self):
        self.ids.quant_input.text = ''