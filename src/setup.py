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
import json

if not config.started_setup:
    os.system("cp -r /app/lib/maps $XDG_DATA_HOME")
    os.system("cp /app/lib/LICENSE $XDG_DATA_HOME")
    os.system("touch $XDG_CONFIG_HOME/playerdata.json")
    utils.output("Welcome to Scripted Journeys, an enthralling text-based adventure where your decisions shape the narrative and uncover hidden mysteries across diverse realms. Each map teems with unique challenges, intricate plots, and fascinating characters, all waiting for you to explore and interact with. Your choices will determine your path, unlocking secrets, and altering the course of your journey in unexpected ways. Embark on a quest that combines storytelling, strategy, and imagination, where every script you write crafts your destiny. Are you ready to dive into a world where every decision is a step towards a new adventure?", "bold_pink")

need_to_write = False
if "name" not in config.playerdata:
    name = ''
    while name == '':
        utils.output("What is your name, brave adventurer?", "magenta")
        print(utils.colourify("magenta"))
        name = input(" > ")
        print(utils.colourify("clear"))
        if name == '':
            utils.output("You have to have a name.", "magenta")
    utils.output(f"Greetings {name}!\n\n", "magenta")
    need_to_write = True

if "colour" not in config.playerdata:
    colour = ''
    while colour.lower() not in ['y', 'n']:
        utils.output("Would you like colour, brave adventurer? [Y/n]", "magenta")
        print(utils.colourify("magenta"))
        colour = input(" > ")
        print(utils.colourify("clear"))
        if colour.lower() not in ['y', 'n']:
            utils.output("Please enter y or n", "magenta")
    colour = 0 if colour.lower() == 'n' else 1
    need_to_write = True

if need_to_write:
    playerdata = {"name": name, "colour": colour}
    with open(config.playerdata_path, 'w') as file:
        json.dump(playerdata, file)

