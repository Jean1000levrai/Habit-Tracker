# scripts
import habit_mgr as hmgr
import database as db
from functions import *
from datetime import *

from login.login_script import *
from login.login_ui_script import *

from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle, RoundedRectangle


class HabitRow(BoxLayout):
    def __init__(self, habit_name, app, on_btn_release, dell, details_btn_release, **kwargs):
        super().__init__(orientation='horizontal', size_hint_y=None, height=60, **kwargs)
        self.app = app
        self.habit_name = habit_name
        with open(resource_path2("data/config.json")) as f:
            config = json.load(f)
        self.user = config["name"]

        date = datetime.today().strftime("%Y-%m-%d")
        hab_id = db.get_info_hab(habit_name, 'id', self.user)

        # Background
        if db.check_log(hab_id, date, self.user):
            color = (0, 1, 0, 0.5)
        else:
            color = app.button_color

        with self.canvas.before:
            self.bg_color = Color(*color)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size)

        self.bind(pos=self.update_rect, size=self.update_rect)
        self.set_background_color(color)
        
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
        with open(resource_path2("data/config.json")) as f:
            config = json.load(f)
        self.user = config["name"]
        self.app = App.get_running_app()
        self.hab_name = ''
        self.lst_btn = []
        self.lst_bg_btn = []
        self.lst_btn_dell = []
        self.lst_btn_details = []
        # self.load_all()
        Clock.schedule_once(lambda dt: self.load_all(), 0.5)

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

        # displays the name of the user at the top
        self.ids.title_app.text = self.user

        # adds the default height of the scrollview
        self.ids.labelled_habits.height = 0

        match config["sort"]: 
            case "Last created":
                sort = db.show_habit_for_gui('*',self.user)
            case "Alphabetical":
                sort = db.sort_by_alpha('*', self.user)
            case "Time":
                sort = db.sort_by_time('*', self.user)

        # displays all the habits from the db
        # by loop on all the db and displays it with a button
        for row in sort:

            habit_name = row[1]

            habit_row = HabitRow(habit_name, self.app, self.on_btn_release, self.sure_del_popup, self.details_btn_release)

            # Store references (optional)
            self.lst_btn.append(habit_row.btn)
            self.lst_btn_dell.append(habit_row.btn_dell)
            self.lst_btn_details.append(habit_row.btn_detail)
            self.lst_bg_btn.append(habit_row)

            self.ids.labelled_habits.add_widget(habit_row)
            self.ids.labelled_habits.height += habit_row.height + 10
        # Use canvas to draw a rounded rectangle behind the ADD button for rounded edges
        self.add = Button(
            text="ADD",
            size_hint_x=None,
            size_hint_y=None,
            height=50,
            width=100,
            background_color=(0, 0, 0, 0),  # Transparent, so we can draw our own bg
            background_normal='',
            color=self.app.text_color,
            halign="left",
            valign="middle",
            padding=(10, 10),
            pos_hint={"center_x": 0.5},
            on_release=self.app.popup
        )
        # the bg
        with self.add.canvas.before:
            self.add_bg_color = Color(*self.app.sbutton_color)
            self.add_bg_rect = RoundedRectangle(
            pos=self.add.pos,
            size=self.add.size,
            radius=[10, 10, 10, 10]
            )
        self.add.bind(pos=lambda instance, value: setattr(self.add_bg_rect, 'pos', value))
        self.add.bind(size=lambda instance, value: setattr(self.add_bg_rect, 'size', value))
        
        self.app.bind(text_color=lambda _, value: setattr(self.add, 'color', value))
        self.ids.labelled_habits.add_widget(self.add)
        self.ids.labelled_habits.height += self.add.height + 20

    def delete_habit(self, hab_name):
        
        print(hab_name)
        db.delete_habit(hab_name, self.user)
        
        self.manager.get_screen("main").empty_hab()
        self.manager.get_screen("main").load_all()

    def validate(self, name, user, yes = True):
        if yes:
            db.valid(hab_name=name, user= user)
            self.empty_hab()
            self.load_all()
        self.manager.transition.direction = "left"
        self.manager.current = "main"

    def on_btn_release(self, instance):
        print("checking in process ...")
        # recovers the name of the clicked btn
        self.hab_name = instance.parent.btn.text
        print(instance.parent.btn.text)
        self.manager.get_screen('validHab').ids.back.text = self.manager.get_screen('validHab').ids.back.text[:3] + self.hab_name

        is_m = db.get_info_hab(self.hab_name, "is_measurable", self.user)
        if is_m:
            self.manager.transition.direction = "left"
            self.manager.current = "validHabM"
            thres = db.get_info_hab(self.hab_name, "threshold", self.user)
            unit = db.get_info_hab(self.hab_name, "unit", self.user)
            hab_id = db.get_info_hab(self.hab_name, "id", self.user)
            quantity = db.get_quantity(hab_id, user=self.user)
            self.manager.get_screen("validHabM").ids.threshold.text = "/ " + str(int(thres)) + ' ' + str(unit)
            self.manager.get_screen("validHabM").ids.quant_input.text = str(quantity)
            self.manager.get_screen("validHabM").current_hab_name = self.hab_name
            self.manager.get_screen("validHabM").current_threshold = thres
            self.manager.get_screen("validHabM").current_unit = unit
        else:
            self.manager.transition.direction = "left"
            self.manager.current = "validHab"
            self.manager.get_screen("validHab").current_hab_name = self.hab_name

    def details_btn_release(self, instance):
        # recovers the name of the clicked btn
        self.hab_name = instance.parent.btn.text
        print(instance.parent.btn.text)

        is_m = db.get_info_hab(self.hab_name, "is_measurable", self.user)
        if is_m:
            self.add_the_info_m()

            # handles the window change
            self.manager.transition.direction = "left"
            self.manager.current = "habMeasurable"

            self.manager.get_screen("habMeasurable").current_hab_name = self.hab_name
            self.manager.get_screen("habMeasurable").edit_mode = True
        else:
            self.add_the_info()

            # handles the window change
            self.manager.transition.direction = "left"
            self.manager.current = "habYesNo"

            self.manager.get_screen("habYesNo").current_hab_name = self.hab_name
            self.manager.get_screen("habYesNo").edit_mode = True

    def add_the_info_m(self, edit = False):
        if not edit:
            self.manager.get_screen("habMeasurable").edit_mode = True
            self.manager.get_screen("habMeasurable").ids.name.text = self.hab_name

            question = db.get_info_hab(self.hab_name, "question", self.user)
            self.manager.get_screen("habMeasurable").ids.qu.text = question

            threshold = db.get_info_hab(self.hab_name, "threshold", self.user)
            self.manager.get_screen("habMeasurable").ids.threshold.text = str(threshold)

            unit = db.get_info_hab(self.hab_name, "unit", self.user)
            self.manager.get_screen("habMeasurable").ids.unit.text = str(unit)

            descr = db.get_info_hab(self.hab_name, "description", self.user)
            self.manager.get_screen("habMeasurable").ids.descr.text = str(descr)
        else:
            print('good')
            self.manager.get_screen("habMeasurable").ids.name.text = ''
            self.manager.get_screen("habMeasurable").ids.qu.text = ''
            self.manager.get_screen("habMeasurable").ids.threshold.text = ''
            self.manager.get_screen("habMeasurable").ids.unit.text = ''
            self.manager.get_screen("habMeasurable").ids.descr.text = ''
            self.manager.get_screen("habMeasurable").edit_mode = False
        
    def add_the_info(self, edit = False):
        if not edit:
            self.manager.get_screen("habYesNo").edit_mode = True
            self.manager.get_screen("habYesNo").ids.name.text = self.hab_name

            question = db.get_info_hab(self.hab_name, "question", self.user)
            self.manager.get_screen("habYesNo").ids.qu.text = question

            descr = db.get_info_hab(self.hab_name, "description", self.user)
            self.manager.get_screen("habYesNo").ids.descr.text = str(descr)

            # reminder = db.get_info_hab(self.hab_name, "reminder", self.user)
            # self.manager.get_screen("habYesNo").ids.rem_for_hab.text = str(reminder)

            # frequency = db.get_info_hab(self.hab_name, "frequency", self.user)
            # self.manager.get_screen("habYesNo").ids.freq_for_hab.text = str(frequency)

        else:
            self.manager.get_screen("habYesNo").ids.name.text = ''
            self.manager.get_screen("habYesNo").ids.qu.text = ''
            self.manager.get_screen("habYesNo").ids.descr.text = ''
            self.manager.get_screen("habYesNo").edit_mode = False

    def sure_del_popup(self, instance):
        hab_name = instance.parent.btn.text
        # -----create the whole layout-------
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        warning_label = Label(
            text="WARNING! ALL DATA RELATED TO THIS HABIT WILL BE DELETED WITH NO WAY TO RECOVER IT! ARE SURE YOU WANT TO CONTINUE",
            color=(1, 0, 0, 1),
            halign='center',
            valign='middle'
        )
        warning_label.bind(size=lambda instance, value: setattr(instance, 'text_size', (value[0], None)))

        # delete btn
        del_btn = Button(text="I UNDERSTAND",
                        size_hint=(1, 0.3), 
                        background_color=(1,0,0,0.8),
                        background_normal='')

        # cancel btn
        cancel_btn = Button(
            text="CANCEL",
            size_hint_x=None,
            size_hint_y=None,
            height=50,
            width=100,
            background_color=(0, 0, 0, 0),
            background_normal='',
            color=self.app.text_color,
            halign="left",
            valign="middle",
            padding=(10, 10),
            pos_hint={"center_x": 0.5})
        # the bg
        with self.add.canvas.before:
            self.add_bg_color = Color(*self.app.sbutton_color)
            self.add_bg_rect = RoundedRectangle(
            pos=self.add.pos,
            size=self.add.size,
            radius=[10, 10, 10, 10]
            )
        self.add.bind(pos=lambda instance, value: setattr(self.add_bg_rect, 'pos', value))
        self.add.bind(size=lambda instance, value: setattr(self.add_bg_rect, 'size', value))  
        self.app.bind(text_color=lambda _, value: setattr(self.add, 'color', value))

        # adds it to the layout
        layout.add_widget(warning_label)
        layout.add_widget(del_btn)
        layout.add_widget(cancel_btn)

        # creates the popup
        popup = Popup(title='',
                    content=layout,
                    size_hint=(0.6, 0.4))

        # binds the btns
        def d(hab_name):
            """will just call delete the hab and dismiss"""
            self.delete_habit(hab_name)
            popup.dismiss()
        cancel_btn.bind(on_press=popup.dismiss)
        del_btn.bind(on_release=lambda _ : d(hab_name))
        popup.open()


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

