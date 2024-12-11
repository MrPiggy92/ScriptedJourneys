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

class Enemy:
    """
    Represents a basic enemy in the game.

    Attributes:
        id (int): Unique identifier for the enemy.
        name (str): The name of the enemy.
        alive (bool): Whether the enemy is alive.
        description (str): A description of the enemy when alive.
        deaddesc (str): A description of the enemy when defeated.
        weapon (str): The weapon the enemy wields.
        hp (int): The health points of the enemy.
        loot (list): Items dropped by the enemy when defeated.
    """

    def __init__(self, id, name, alive, description, deaddesc, weapon, hp, loot):
        self.id = id
        self.name = name
        self.alive = alive
        self.description = description
        self.deaddesc = deaddesc
        self.weapon = weapon
        self.hp = hp
        self.loot = loot

    def __str__(self):
        """
        Returns a string representation of the enemy's current state.
        """
        status = "Alive" if self.alive else "Defeated"
        return f"{self.name} ({status}) - HP: {self.hp}"


class Boss(Enemy):
    """
    Represents a boss enemy in the game. Bosses inherit from the Enemy class.

    Attributes:
        id (int): Unique identifier for the boss.
        name (str): The name of the boss.
        alive (bool): Whether the boss is alive.
        description (str): A description of the boss when alive.
        deaddesc (str): A description of the boss when defeated.
        weapon (str): The weapon the boss wields.
        hp (int): The health points of the boss.
        loot (list): Items dropped by the boss when defeated.
        special_attack (str): A unique attack used by the boss.
    """

    def __init__(self, id, name, alive, description, deaddesc, weapon, hp, loot):
        super().__init__(id, name, alive, description, deaddesc, weapon, hp, loot)

    def __str__(self):
        """
        Returns a string representation of the boss's current state.
        """
        status = "Alive" if self.alive else "Defeated"
        return f"Boss {self.name} ({status}) - HP: {self.hp}, Special Attack: {self.special_attack}"
