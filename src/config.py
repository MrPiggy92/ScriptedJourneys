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

import os
import sys
import json

if sys.platform == "win32":
    config_home = data_home = os.path.join(os.path.expandvars("%LOCALAPPDATA%"), "ScriptedJourneys")
elif os.path.expandvars("$XDG_DATA_HOME") != "$XDG_DATA_HOME":
    config_home = os.path.expandvars("$XDG_CONFIG_HOME")
    data_home = os.path.expandvars("$XDG_DATA_HOME")
else:
    config_home = data_home = os.path.expandvars("$HOME/.config/ScriptedJourneys")

maps_path = os.path.join(data_home, "maps")

playerdata_path = os.path.join(config_home, "playerdata.json")

started_setup = os.path.exists(maps_path)

license_text = f"""Scripted Journeys version 1.2.1

Copyright (C) 2024 MrPiggy92. Scripted Journeys comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it under certain conditions.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.
It can be found at {os.path.join(data_home, 'LICENSE')}.
If not, see <http://www.gnu.org/licenses/>."""

warranty_text = """This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details."""

license_link = f"To read the full GPL-3.0 license, please visit https://www.gnu.org/licenses/gpl-3.0.txt or view {os.path.join(data_home, 'LICENSE')}"

def show(type):
    if type == 'w':
        print(warranty_text)
    else:
        print(license_link)

def load_preferences():
    try:
        with open(playerdata_path) as playerdata:
            playerdata = json.load(playerdata)
    except:
        playerdata = {}
        player_name = ''
        wants_colour = True
        wants_scroll = True
    try:
        player_name = playerdata["name"]
    except:
        player_name = ''
    try:
        wants_colour = bool(playerdata["colour"])
    except:
        wants_colour = True
    try:
        wants_scroll = bool(playerdata["scroll"])
    except:
        wants_scroll = True
    return playerdata, player_name, wants_colour, wants_scroll

playerdata, player_name, wants_colour, wants_scroll = load_preferences()
