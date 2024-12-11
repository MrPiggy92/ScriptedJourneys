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

# Main script
import os
import sys
import time

import utils
import map
import player
import config
from playFunctions import *

import setup

config.playerdata, config.player_name, config.wants_colour, config.wants_scroll = config.load_preferences()

# --- Constants ---
COMMANDS = {
    "take": {"func": trytotake, "args": 1, "desc": "Take an item"},
    "t": {"func": trytotake, "args": 1, "desc": "Take an item (shorthand)"},
    "inventory": {"func": listinventory, "args": 0, "desc": "List inventory"},
    "i": {"func": listinventory, "args": 0, "desc": "List inventory (shorthand)"},
    "look": {"func": lookat, "args": 1, "desc": "Examine an item"},
    "l": {"func": lookat, "args": 1, "desc": "Examine an item (shorthand)"},
    "use": {"func": trytouse, "args": 1, "desc": "Use an item"},
    "u": {"func": trytouse, "args": 1, "desc": "Use an item (shorthand)"},
    "fight": {"func": fight, "args": 1, "desc": "Fight an enemy"},
    "f": {"func": fight, "args": 1, "desc": "Fight an enemy (shorthand)"},
    "move": {"func": trytomove, "args": 1, "desc": "Move to another room"},
    "m": {"func": trytomove, "args": 1, "desc": "Move to another room (shorthand)"},
    "quit": {"func": None, "args": 0, "desc": "Quit the game"},
    #"tutorial": {"func": tutorial, "args": 0, "desc": "Show tutorial"},
    "cast": {"func": castspell, "args": 1, "desc": "Cast a spell"},
    "c": {"func": castspell, "args": 1, "desc": "Cast a spell (shorthand)"},
    "next": {"func": lambda player, game_map: game_map.next_level(player), "args": 0, "desc": "Move to the next level"},
    "show": {"func": config.show, "args": 1, "desc": "Show warranty"},
    "show": {"func": config.show, "args": 1, "desc": "Show license"},
}

# --- Game Functions ---
def display_room(player):
    """
    Displays the current room's state.
    """
    utils.output(player.currentroom.name, "bright_cyan")
    utils.output(player.currentroom.description, "clear")
    listroomitems(player)
    listenemies(player)
    listexits(player)


def parse_action(action_input, player, game_map):
    """
    Parses and executes the player's action.
    """
    parts = action_input.strip().lower().split(" ", 1)
    command = parts[0]
    arg = parts[1] if len(parts) > 1 else None

    if command in COMMANDS:
        command_info = COMMANDS[command]
        if command_info["func"]:
            if command_info["args"] == 0:
                command_info["func"](player, game_map)
            elif command_info["args"] == 1 and arg:
                command_info["func"](arg, player, game_map)
            else:
                utils.output(f"Invalid usage of '{command}'.", "magenta")
        else:
            utils.output("Quitting", "magenta")
            raise RuntimeError()
    else:
        utils.output("You can't do that.", "magenta")


def play(name):
    """
    Main gameplay loop.
    """
    my_map = map.Map(name)
    my_player = player.Player(config.player_name, my_map.rooms[0], 10, [])
    #utils.output(my_map.opening_text, "bold_pink", 0.03)
    time.sleep(0.5)

    while True:
        utils.output("\n", "clear")
        checkhp(my_player, my_map)
        display_room(my_player)

        action_input = input(utils.colourify("magenta") + " > " + utils.colourify("clear"))
        utils.output("", "clear")

        try:
            parse_action(action_input, my_player, my_map)
        except RuntimeError:
            break
        except Exception as e:
            utils.output(f"Error: {e}", "magenta")


def control():
    """
    Control center for the game.
    """
    utils.output("To play a map, type `play mapname`.\nTo list maps, type `list`.\nTo edit settings, type `settings`.\nTo quit, type `quit`.", "bright_yellow")

    while True:
        utils.output("Control Centre", "bright_cyan")
        action_input = input(utils.colourify("magenta") + " > " + utils.colourify("clear"))
        utils.output("", "clear")

        if action_input.lower().startswith("play "):
            try:
                play(action_input[5:])
            except FileNotFoundError:
                utils.output("That map does not exist.", "magenta")
        elif action_input.lower() == "list":
            maps = [
                file
                for file in os.listdir(config.maps_path)
                if "<NotVisible>" not in file
            ]
            utils.output("Maps:\n" + "\n".join(maps), "bright_yellow")
        elif action_input.lower() == "settings":
            settings()
        elif action_input.lower() == "quit":
            utils.output("Quitting", "magenta")
            time.sleep(1.5)
            break
        else:
            utils.output("You can't do that.", "magenta")


# --- Run Control Center ---
if __name__ == "__main__":
    print(config.license_text)
    control()
