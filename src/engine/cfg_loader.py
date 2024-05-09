import json

ASSET_PATH = 'assets/cfg'


def window_cfg() -> any:
    with open(f"{ASSET_PATH}/window.json") as window_file:
        window = json.load(window_file)
        return window['title'], window['size'], window['framerate'], window['bg_color']


def interface_cfg() -> any:
    with open(f"{ASSET_PATH}/interface.json") as interface_file:
        return json.load(interface_file)


def starfield_cfg() -> any:
    with open(f"{ASSET_PATH}/starfield.json") as starfield_file:
        return json.load(starfield_file)


def player_cfg() -> any:
    with open(f"{ASSET_PATH}/player.json") as player_file:
        return json.load(player_file)


def level_cfg(file: str) -> any:
    with open(f"{ASSET_PATH}/{file}") as level_file:
        return json.load(level_file)
