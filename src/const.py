from functions import resource_path2
import json

def user_const():
    with open(resource_path2("data/config.json")) as f:
                config = json.load(f)
    return config["name"]