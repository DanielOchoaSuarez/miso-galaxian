import json

ASSET_PATH = 'assets/cfg'

def window_cfg() -> any:
    file = open(f"{ASSET_PATH}/window.json")
    window = json.load(file)
    return window['title'], window['size'], window['framerate'], window['bg_color']

def starfield_cfg() -> any:
    file = open(f"{ASSET_PATH}/starfield.json")
    starfield = json.load(file)
    return starfield

def player_cfg() -> any:
    file = open(f"{ASSET_PATH}/player.json")
    player = json.load(file)
    return player
