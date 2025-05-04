

class HabitYesNo:
    def __init__(self, name="", colour = "#0000FF", qu="", reminder=False, descr=""):
        self.__name = name            # str
        self.__colour = colour        # #RRGGBB hex
        self.__question = qu          # str
        self.__reminder = reminder    # bool
        self.__description = descr    # str
        self.__frequency = None
        self.__completed = False
        self.__is_active = True


    # --------GET---------
    @property
    def name(self):
        return self.name
    
    @property
    def colour(self):
        return self.colour
    
    @property
    def question(self):
        return self.question
    
    @property
    def reminder(self):
        return self.reminder
    
    @property
    def description(self):
        return self.description
    
    @property
    def frequency(self):
        pass

    # ----------SET-----------
    @name.setter
    def name(self, val):
        if not val.strip():
            raise ValueError("Habit name cannot be empty.")
        self.name = val

    @colour.setter
    def colour(self, val):
        if not isinstance(val, str) or not val.startswith("#") or len(val) not in (7, 9):
            raise ValueError("Colour must be a hex string like '#RRGGBB'.")
        self.colour = val

    @question.setter
    def question(self, val):
        self.question = str(val)

    @reminder.setter
    def reminder(self, val):
        if not isinstance(val, bool):
            raise ValueError("Reminder must be a boolean.")
        self.reminder = val

    @description.setter
    def description(self, val):
        self.description = str(val)

    @frequency.setter
    def frequency(self, val):
        if not isinstance(val, tuple):
            raise ValueError("Reminder must be a tuple (int, str).")
        if not isinstance(val[0], int):
            raise ValueError("First value should be an integer.")
        allowed = {"daily", "weekly", "monthly", None}
        if val[1] not in allowed:
            raise ValueError(f"Frequency must be one of {allowed}.")
        self.frequency = val
                             

    


    