from kivy.uix.widget import Widget
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.colorpicker import ColorPicker



class ColorPickerWidget(ColorPicker):
    pass

class MainPicker(Widget):

    selected_colour = [0, 0, 1, 1]

