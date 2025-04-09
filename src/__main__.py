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
import pickle

import utils
import map
import player
import config
from playFunctions import *

import setup

config.playerdata, config.player_name, config.wants_colour, config.wants_scroll, config.wants_opening_text, config.wants_hardcore = config.load_preferences()

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
    "q": {"func": None, "args": 0, "desc": "Quit the game"},
    #"tutorial": {"func": tutorial, "args": 0, "desc": "Show tutorial"},
    "cast": {"func": castspell, "args": 1, "desc": "Cast a spell"},
    "c": {"func": castspell, "args": 1, "desc": "Cast a spell (shorthand)"},
    "equip": {"func": trytoequip, "args": 1, "desc": "Equip a weapon"},
    "e": {"func": trytoequip, "args": 1, "desc": "Equip a weapon (shorthand)"},
    "drop": {"func": trytodrop, "args": 1, "desc": "Drop an item"},
    "d": {"func": trytodrop, "args": 1, "desc": "Drop an item (shorthand"},
    "save": {"func": save, "args": 0, "desc": "Save game"},
    "s": {"func": save, "args": 0, "desc": "Save game (shorthand)"},
    "next": {"func": lambda player, game_map: game_map.next_level(player), "args": 0, "desc": "Move to the next level"},
    "show": {"func": config.show, "args": 1, "desc": "Show license"},
}

def devcheats(cheat, player, map):
    cheat = cheat[12:]
    print(cheat)
    map.cheats_used = True
    if cheat.startswith("kill"):
        player.currentroom.enemies[0].hp = 0
    elif cheat.startswith("next"):
        map.bossDefeated = True
        map.next_level(player)

# --- Game Functions ---
def display_room(player, map):
    """
    Displays the current room's state.
    """
    utils.output(player.currentroom.name, "bright_cyan")
    utils.output(player.currentroom.description, "clear")
    listroomitems(player)
    listenemies(player, map)
    listexits(player)


def parse_action(action_input, player, game_map):
    """
    Parses and executes the player's action.
    """
    parts = action_input.strip().lower().split(" ", 1)
    command = parts[0]
    command = utils.fuzzy_match(command, list(COMMANDS.keys()))
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


def play(name, my_map=None, my_player=None):
    """
    Main gameplay loop.
    """
    if not my_map:
        my_map = map.Map(name)
        my_player = player.Player(config.player_name, my_map.rooms[0], 10, [])
    if config.wants_opening_text:
        utils.output(my_map.opening_text, "bold_pink", 0.03)
    time.sleep(0.5)

    while True:
        utils.output("\n", "clear")
        checkhp(my_player, my_map)
        display_room(my_player, my_map)

        action_input = utils.cinput()
        utils.output("", "clear")
        
        if action_input.startswith("@dev.cheats"):
            devcheats(action_input, my_player, my_map)

        try:
            parse_action(action_input, my_player, my_map)
        except RuntimeError:
            print()
            break
        #except Exception as e:
        #    utils.output(f"Error: {e}", "magenta")


def control():
    """
    Control center for the game.
    """
    utils.output("To play a map, type `play mapname`.", "bright_yellow")
    utils.output("To list maps, type `list`.", "bright_yellow")
    utils.output("To resume your savegame, type `resume`.", "bright_yellow")
    utils.output("To edit settings, type `settings`.", "bright_yellow")
    utils.output("To quit, type `quit`.", "bright_yellow")
    
    while True:
        utils.output("Control Centre", "bright_cyan")
        action_input = utils.cinput()
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
                if ("_NotVisible_" not in file) and ("<NotVisible>" not in file)
            ]
            utils.output("Maps:\n" + "\n".join(maps), "bright_yellow")
        elif action_input.lower() == "settings":
            try:
                settings()
            except RuntimeError:
                pass
        elif action_input.lower() == "quit":
            utils.output("Quitting", "magenta")
            time.sleep(1.5)
            break
        elif action_input.lower() == "resume":
            utils.output("Loading save game...", "magenta")
            name = os.path.join(config.config_home, "saveGame.pkl")
            if os.path.exists(name):
                with open(name, "rb") as saveFile:
                    player, my_map = pickle.load(saveFile)
                play(None, my_map, player)
            else:
                utils.output("You have no save game.", "magenta")
        else:
            utils.output("You can't do that.", "magenta")


# --- Run Control Center ---
if __name__ == "__main__":
    print(config.license_text)
    control()
