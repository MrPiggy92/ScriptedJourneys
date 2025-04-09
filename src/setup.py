# Scripted Journeys

#
# Copyright (C) 2024 MrPiggy92
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#

import config
import utils

import os
import sys
import json
import time

if sys.platform == "win32":
    try:
        app_root = sys._MEIPASS
    except:
        utils.output("Error in setup: sys._MEIPASS not found. Please file an issue on Github or look for an existing issue.", "red")
        time.sleep(5)
        raise SystemExit()
    copy = "robocopy /E /NFL /NDL /NJH /NJS /NC /NS"
else:
    app_root = "/app"
    copy = "cp -r"

#print(os.listdir(sys._MEIPASS))
#print(os.listdir(os.path.join(sys._MEIPASS, "lib")))
#print(os.listdir(os.path.join(sys._MEIPASS, "lib", "maps")))

if not config.started_setup:
    os.system(f"{copy} {os.path.join(app_root, 'lib', 'maps')} {config.maps_path}")
    os.system(f"{copy} {os.path.join(app_root, 'lib', 'LICENSE')} {config.data_home}")
    os.system(f"echo '' > {config.playerdata_path}" if sys.platform == "win32" else "touch $XDG_CONFIG_HOME/playerdata.json")
    utils.output("Welcome to Scripted Journeys, an enthralling text-based adventure where your decisions shape the narrative and uncover hidden mysteries across diverse realms. Each map teems with unique challenges, intricate plots, and fascinating characters, all waiting for you to explore and interact with. Your choices will determine your path, unlocking secrets, and altering the course of your journey in unexpected ways. Embark on a quest that combines storytelling, strategy, and imagination, where every script you write crafts your destiny. Are you ready to dive into a world where every decision is a step towards a new adventure?", "bold_pink")

need_to_write = False
name = config.player_name
colour = int(config.wants_colour)
scroll = int(config.wants_scroll)
opening = int(config.wants_opening_text)
hardcore = int(config.wants_hardcore)

if "name" not in config.playerdata.keys():
    utils.output("First, we need to update your preferences.", "cyan")
    name = ''
    while name == '':
        utils.output("What is your name, brave adventurer?", "magenta")
        print(utils.colourify("magenta"))
        name = utils.cinput()
        print(utils.colourify("clear"))
        if name == '':
            utils.output("You have to have a name.", "magenta")
    utils.output(f"Greetings {name}!\n\n", "magenta")
    need_to_write = True

if "colour" not in config.playerdata.keys():
    if not need_to_write:
        utils.output("First, we need to update your preferences.", "cyan")
    colour = ''
    while colour.lower() not in ['y', 'n']:
        utils.output("Would you like colour, brave adventurer? [Y/n]", "magenta")
        print(utils.colourify("magenta"))
        colour = utils.cinput()
        print(utils.colourify("clear"))
        if colour.lower() not in ['y', 'n']:
            utils.output("Please enter y or n", "magenta")
    colour = 0 if colour.lower() == 'n' else 1
    need_to_write = True

if "scroll" not in config.playerdata.keys():
    if not need_to_write:
        utils.output("First, we need to update your preferences.", "cyan")
    scroll = ''
    while scroll.lower() not in ['y', 'n']:
        utils.output("Would you like this scrolling effect, brave adventurer? [Y/n]", "magenta")
        print(utils.colourify("magenta"))
        scroll = utils.cinput()
        print(utils.colourify("clear"))
        if scroll.lower() not in ['y', 'n']:
            utils.output("Please enter y or n", "magenta")
    scroll = 0 if scroll.lower() == 'n' else 1
    need_to_write = True
if "opening" not in config.playerdata.keys():
    if not need_to_write:
        utils.output("First, we need to update your preferences.", "cyan")
    opening = ''
    while opening.lower() not in ['y', 'n']:
        utils.output("Would you like a short paragraph of lore for each map, brave adventurer? [Y/n]", "magenta")
        print(utils.colourify("magenta"))
        opening = utils.cinput()
        print(utils.colourify("clear"))
        if opening.lower() not in ['y', 'n']:
            utils.output("Please enter y or n", "magenta")
    opening = 0 if opening.lower() == 'n' else 1
    need_to_write = True
if "hardcore" not in config.playerdata.keys():
    if not need_to_write:
        utils.output("First, we need to update your preferences.", "cyan")
    hardcore = ''
    while hardcore.lower() not in ['y', 'n']:
        utils.output("Would you like hardcore mode (1 life per map instead of 3), brave adventurer? [Y/n]", "magenta")
        print(utils.colourify("magenta"))
        hardcore = utils.cinput()
        print(utils.colourify("clear"))
        if hardcore.lower() not in ['y', 'n']:
            utils.output("Please enter y or n", "magenta")
    hardcore = 0 if hardcore.lower() == 'n' else 1
    need_to_write = True

if need_to_write:
    playerdata = {"name": name, "colour": colour, "scroll": scroll, "opening": opening, "hardcore": hardcore}
    with open(config.playerdata_path, 'w') as file:
        json.dump(playerdata, file)
    utils.output("Your preferences have been saved", "cyan")
    time.sleep(1.5)

