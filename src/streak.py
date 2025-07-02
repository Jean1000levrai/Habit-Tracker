import database as db
import json
from functions import resource_path2
from const import user_const


def streak(*args):
    """function the determines how many days 
    in row the user has been completing his daily habits.
    called at the start of the app. stores the result in config.json
    """
    with open(resource_path2("data/config.json"), "r") as f:
            config = json.load(f)
    user = user_const()
    accept=0.5              # the acceptance,e.g. 0.5 -> if half of habs done, the streak continues
    all_dates = db.get_all_dates()[::-1]    # every dates in the logs, sort from the newest
    lst_hab = db.get_all_habits()   # a list of every habits in db (id, name)
    streak = 0  # the streak that will be returned, the final answer
    i=0         # the index of the loop

    # loops until accept > a
    while True:
        a = 0
        nb_hab = len(db.habits_has_date(all_dates[i], user))
        if nb_hab <= 0:
            break

        for hab in lst_hab:
            if db.check_log(hab[0], all_dates[i], user):
  
                a = a + 1

        a = a/nb_hab    # the rate of habs done // nb_total of the day

        # break the loop if the logs has been looped in its enterety
        # or if a < accept
        if a < accept or i >= len(all_dates)-1:
            break
        streak = streak + 1
        i = i + 1

    config["streak"] = streak
    with open(resource_path2("data/config.json"), "w") as f:
            json.dump(config, f, indent=1)

    return streak


