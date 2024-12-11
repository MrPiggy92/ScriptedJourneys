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
import json

# Get environment paths with fallback defaults
config_home = os.environ.get("XDG_CONFIG_HOME")
data_home = os.environ.get("XDG_DATA_HOME")

# Paths
maps_path = os.path.join(data_home, "maps")
playerdata_path = os.path.join(config_home, "playerdata.json")

# Check if setup has started
started_setup = os.path.exists(maps_path)

# License and warranty information
license_text = (
    "Scripted Journeys version 1.1.0\n\n"
    "Copyright (C) 2024 MrPiggy92. Scripted Journeys comes with ABSOLUTELY NO WARRANTY.\n"
    "This is free software, and you are welcome to redistribute it under certain conditions.\n"
    "See the GNU General Public License for more details.\n\n"
    f"You should have received a copy of the GNU General Public License along with this program.\n"
    f"It can be found at {os.path.join(data_home, 'LICENSE')}.\n"
    "If not, see <http://www.gnu.org/licenses/>."
)

warranty_text = (
    "This program is distributed in the hope that it will be useful,\n"
    "but WITHOUT ANY WARRANTY; without even the implied warranty of\n"
    "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the\n"
    "GNU General Public License for more details."
)

license_link = (
    "To read the full GPL-3.0 license, please visit https://www.gnu.org/licenses/gpl-3.0.txt "
    f"or view {os.path.join(data_home, 'LICENSE')}."
)

def show(option, _player, _map):
    """Show section of license, either warranty or link to full license.
    
    Attributes:
        option (str): w to show warranty text, anything else to show link to full license.
        _player NOT USED, just to simplify main game loop.
        _map NOT USED, just to simplify main game loop.
    """
    
    if option == "w":
        print(warranty_text)
    else:
        print(license_link)

def load_preferences():
    """Load player preferences from the JSON configuration file."""
    # Initialize default preferences
    defaults = {
        "name": "",
        "colour": True,
        "scroll": True,
    }

    # Attempt to load player data
    if os.path.exists(playerdata_path):
        try:
            with open(playerdata_path, "r", encoding="utf-8") as f:
                playerdata = json.load(f)
                if not isinstance(playerdata, dict):
                    raise ValueError("Invalid data format in playerdata.json")
        except (IOError, json.JSONDecodeError, ValueError) as e:
            print(f"Error loading preferences: {e}")
            playerdata = {}
    else:
        playerdata = {}

    # Populate preferences with defaults
    player_name = playerdata.get("name", defaults["name"])
    wants_colour = playerdata.get("colour", defaults["colour"])
    wants_scroll = playerdata.get("scroll", defaults["scroll"])

    return playerdata, player_name, wants_colour, wants_scroll


# Load player preferences
playerdata, player_name, wants_colour, wants_scroll = load_preferences()
