

class HabitYesNo:
    def __init__(self, name="New Habit", colour = "[1, 1, 1, 1]", qu="", reminder=False, descr=""):
        self.__name = name            # str
        self.__colour = colour        # #RRGGBB hex
        self.__question = qu          # str
        self.__reminder = reminder    # bool
        self.__description = descr    # str
        self.__frequency = None
        self.completed = False
        self.is_active = True

    # --------GET---------
    @property
    def name(self):
        return self.__name
    
    @property
    def colour(self):
        return self.__colour
    
    @property
    def question(self):
        return self.__question
    
    @property
    def reminder(self):
        return self.__reminder
    
    @property
    def description(self):
        return self.__description
    
    @property
    def frequency(self):
        return self.__frequency

    # ----------SET-----------
    @name.setter
    def name(self, val):
        if not val.strip():
            raise ValueError("Habit name cannot be empty.")
        self.__name = val

    @colour.setter
    def colour(self, val):
        self.__colour = val

    @question.setter
    def question(self, val):
        self.__question = str(val)

    @reminder.setter
    def reminder(self, val):
        if not isinstance(val, bool):
            raise ValueError("Reminder must be a boolean.")
        self.__reminder = val

    @description.setter
    def description(self, val):
        self.__description = str(val)

    @frequency.setter
    def frequency(self, val):
        if not isinstance(val, list):
            raise ValueError("Reminder must be a tuple (int, str).")
        if not isinstance(val[0], int):
            raise ValueError("First value should be an integer.")
        allowed = {"daily", "weekly", "monthly", None}
        if val[1] not in allowed:
            raise ValueError(f"Frequency must be one of {allowed}.")
        
        self.__frequency = val


class HabitMeasurable:
    def __init__(self, name="New Habit", colour = "[1, 1, 1, 1]", qu='', reminder=False, descr='', unit=''):
        self.__name = name            # str
        self.__colour = colour        # #RRGGBB hex
        self.__question = qu          # str
        self.__reminder = reminder    # bool
        self.__description = descr    # str
        self.__frequency = None
        self.unit = ''
        self.threshold = 0
        self.quantity = 0
        self.is_active = True

    # --------GET---------
    @property
    def name(self):
        return self.__name
    
    @property
    def colour(self):
        return self.__colour
    
    @property
    def question(self):
        return self.__question
    
    @property
    def reminder(self):
        return self.__reminder
    
    @property
    def description(self):
        return self.__description
    
    @property
    def frequency(self):
        return self.__frequency

    # ----------SET-----------
    @name.setter
    def name(self, val):
        if not val.strip():
            raise ValueError("Habit name cannot be empty.")
        self.__name = val

    @colour.setter
    def colour(self, val):
        self.__colour = val

    @question.setter
    def question(self, val):
        self.__question = str(val)

    @reminder.setter
    def reminder(self, val):
        if not isinstance(val, bool):
            raise ValueError("Reminder must be a boolean.")
        self.__reminder = val

    @description.setter
    def description(self, val):
        self.__description = str(val)

    @frequency.setter
    def frequency(self, val):
        if not isinstance(val, tuple):
            raise ValueError("Reminder must be a tuple (int, str).")
        if not isinstance(val[0], int):
            raise ValueError("First value should be an integer.")
        allowed = {"daily", "weekly", "monthly", None}
        if val[1] not in allowed:
            raise ValueError(f"Frequency must be one of {allowed}.")
        self.__frequency = val

if __name__ == "__main__":
    hab=HabitYesNo()

    


    