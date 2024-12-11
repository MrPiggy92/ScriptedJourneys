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

# Player
import items


class Player:
    def __init__(self, name, currentroom, hp=10, inventory=[]):
        """
        Initializes the Player object.

        Attributes:
            name (str): The player's name.
            currentroom: The starting room for the player.
            hp (int): The player's health points.
            inventory (list): A list of items in the player's possession.
        """
        self.name = name
        self.currentroom = currentroom
        self.hp = hp
        self.inventory = inventory
        self.weapon = items.Weapon(
            id=0,
            name="Fists",
            description="Your fists, ready for punching.",
            updroomdesc=None,
            portable=True,
            revealsitem=None,
            usedin=None,
            usedesc=None,
            removesroomitem=None,
            addsroomitem=None,
            useroomdesc=None,
            disposable=False,
            damage=0.5,  # Base damage for fists
        )
