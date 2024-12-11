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

class Item:
    """
    Represents a general item in the game.

    Attributes:
        number (int): Unique identifier for the item.
        name (str): Name of the item.
        description (str): Detailed description of the item.
        updroomdesc (str): Description of the room after item is used.
        portable (bool): Whether the item can be carried.
        revealsitem (bool): Whether the item reveals another item upon use.
        usedin (str): The room or context where the item can be used.
        usedesc (str): Description of the item's usage.
        removesroomitem (list): Items to be removed from the room upon use.
        addsroomitem (list): Items to be added to the room upon use.
        useroomdesc (str): Room description after using the item.
        disposable (bool): Whether the item is consumed after use.
    """
    def __init__(self, id, name, description, updroomdesc, portable, 
                 revealsitem, usedin, usedesc, removesroomitem, addsroomitem, 
                 useroomdesc, disposable):
        self.id = id
        self.name = name
        self.description = description
        self.updroomdesc = updroomdesc
        self.portable = portable
        self.revealsitem = revealsitem
        self.usedin = usedin
        self.usedesc = usedesc
        self.removesroomitem = removesroomitem
        self.addsroomitem = addsroomitem
        self.useroomdesc = useroomdesc
        self.disposable = disposable

    def __str__(self):
        """
        Returns a string representation of the item.
        """
        return f"{self.name} (ID: {self.number}): {self.description}"


class StatItem(Item):
    """
    Represents an item that affects player statistics.

    Attributes:
        hp_change (int): Amount of HP the item changes (positive or negative).
    """
    def __init__(self, id, name, description, updroomdesc, portable, 
                 revealsitem, usedin, usedesc, removesroomitem, addsroomitem, 
                 useroomdesc, disposable, hp_change):
        super().__init__(id, name, description, updroomdesc, portable, 
                         revealsitem, usedin, usedesc, removesroomitem, 
                         addsroomitem, useroomdesc, disposable)
        self.hp_change = hp_change


class Weapon(Item):
    """
    Represents a weapon item.

    Attributes:
        damage (int): The damage dealt by the weapon.
    """
    def __init__(self, id, name, description, updroomdesc, portable, 
                 revealsitem, usedin, usedesc, removesroomitem, addsroomitem, 
                 useroomdesc, disposable, damage, sound_path=None):
        super().__init__(id, name, description, updroomdesc, portable, 
                         revealsitem, usedin, usedesc, removesroomitem, 
                         addsroomitem, useroomdesc, disposable)
        self.damage = damage
