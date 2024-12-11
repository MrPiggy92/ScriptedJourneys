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

# Room
class Room:
    """
    Represents a room in-game
    
    Attributes:
        id (int): Unique identifier of the room
        name (str): Room name
        description (str): Description of the room
        exits (list): The exits from the room to other rooms
        items (list): The items contained in the room
        enemies (list): Any enemies found in this room
    """
    
    def __init__(self, id, name, description, exits, items, enemies):
        self.id = id
        self.name = name
        self.description = description
        self.exits = exits
        self.items = items
        self.enemies = enemies
    
    def __repr__(self):
        """
        Returns a string representation of the room.
        """
        return f"Room(id={self.id}, name='{self.name}')"
