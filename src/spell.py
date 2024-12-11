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

class Spell:
    """
    Class to represent a spell
    
    Attributes:
        id (int): Unique identifier of this spell
        name (str): name of the spell
        description (str): Text outputted when spell is used
        effect (str): Python code run when spell is cast
    """
    def __init__(self, id, name, description, effect):
        self.id = id
        self.name = name
        self.description = description
        self.effect = effect
