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

import utils, items
import enemy as enemyObject
import config

from random import random
from time import sleep
import json
import pickle
import os

def showhpbar(player):
    # Calculate the percentage of hit points
    progress = player.hp / 10.0 * 100 if player.hp > 0 else 0

    # Determine the color based on HP value
    if player.hp >= 7:
        hp_color = "green"
    elif 4 <= player.hp <= 6:
        hp_color = "orange"
    else:
        hp_color = "red"

    # Create the progress bar string manually
    bar_length = 20
    filled_length = int(bar_length * progress // 100)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)

    # Print the progress bar with the appropriate color
    utils.output(f"HP: [{bar}] {player.hp if player.hp > 0 else 0}/10 HP", hp_color)
    return


def trytomove(direction, player, map):
    current_room = player.currentroom
    exits = current_room.exits
    
    direction = direction[0].upper() if direction != '' else ''

    if direction in ['N', 'S', 'E', 'W']:
        direction_index = ['N', 'S', 'E', 'W'].index(direction)
        if exits[direction_index] is not None:
            new_room = exits[direction_index]
            player.currentroom = new_room
            return
    utils.output("You can't go that way.", "magenta")




def listexits(player):
    if player.currentroom.exits[0] != None:
        utils.output("You see an exit to the North.", "clear")
    if player.currentroom.exits[1] != None:
        utils.output("You see an exit to the South.", "clear")
    if player.currentroom.exits[2] != None:
        utils.output("You see an exit to the East.", "clear")
    if player.currentroom.exits[3] != None:
        utils.output("You see an exit to the West.", "clear")


def fight(enemy_name, player, map):
    current_room = player.currentroom
    enemy = None

    if player.weapon is None:
        utils.output("You can't fight without a weapon!", "magenta")
        return

    for room_enemy in current_room.enemies:
        if utils.levenshteinDistance(room_enemy.name.lower(), enemy_name.lower()) < 3:
            #utils.output(f"Assuming you mean {room_enemy.name}.")
            enemy = room_enemy
            break
    #print(enemy.hp)

    if enemy and enemy.alive:
        utils.output(f"A battle begins with the {enemy.name}!", "red")
        while enemy.alive and player.hp > 0:
            # Player's turn
            player_damage = player.weapon.damage
            hit_or_miss = random()
            if hit_or_miss > 0.9:
                player_damage += 1
            elif hit_or_miss < 0.1:
                player_damage -= 1
                player_damage = 0 if player_damage < 0 else player_damage
            else:
                pass
                
            enemy.hp -= player_damage
            if player.weapon.damage != player_damage:
                utils.output(f"You hit the {enemy.name} with your {player.weapon.name}. {'Critical hit!' if player_damage > player.weapon.damage else 'Just a scratch.'} It causes {player_damage} damage.", "green")
            else:
                utils.output(f"You hit the {enemy.name} with your {player.weapon.name}. It causes {player_damage} damage.", "green")

            # Check enemy's HP
            if enemy.hp <= 0:
                enemy.alive = False
                utils.output(enemy.deaddesc, "red")
                lootbody(enemy, player, map)
                break

            # Enemy's turn
            enemy_damage = enemy.weapon.damage
            player.hp -= enemy_damage
            utils.output(f"The {enemy.name} hits you with its {enemy.weapon.name}. It causes {enemy_damage} damage.", "red")
            showhpbar(player)

            # Check player's HP
            if checkhp(player, map) <= 0:
                break
            
            utils.output("Continue?", "magenta")
            run = utils.cinput().lower()
            if run.startswith('n'):
                utils.output(f"You have run away from the {enemy.name}.", "magenta")
                break

        if player.hp <= 0:
            die(player, map)
    else:
        utils.output("There is no such enemy here.", "magenta")


def lootbody(enemy, player, map):
    current_room = player.currentroom

    utils.output(f"You defeated the {enemy.name} in combat!", "bright_yellow")
    utils.output(f"You find the following items on the {enemy.name}'s body:", "clear")

    if enemy.weapon is not None:
        current_room.items.append(enemy.weapon)
        utils.output(f"- {enemy.weapon.name}", "yellow")

    if enemy.loot is not None:
        #print(enemy.loot)
        for item in enemy.loot:
            current_room.items.append(item)
            utils.output(f"- {item.name}", "yellow")

    # Remove the enemy from the room
    current_room.enemies.remove(enemy)
    if isinstance(enemy, enemyObject.Boss):
        
        if map.level == map.all_levels:
            utils.output("That was the final boss of this map! Type `next` to finish.", "bright_green")
        else:
            utils.output("That was the boss of this level! To move to the next level, type `next`.", "bright_green")
        map.bossDefeated = True


def checkhp(player, map):
    hp = player.hp
    if player.hp > 10:
        player.hp = 10
    elif player.hp <= 0:
        die(player, map)
    return hp


def listroomitems(player):
    current_room = player.currentroom
    if current_room.items:
        utils.output(f"You see the following items:", "clear")
        for item in current_room.items:
            utils.output("- " + item.name, "yellow")
    else:
        utils.output("There are no items here.", "clear")


def trytotake(item, player, map):
    current_room = player.currentroom
    taken = False
    new_items = list(current_room.items)
    
    #print(current_room.items)
    for room_item in current_room.items:
        #print(room_item.name)
        if utils.levenshteinDistance(room_item.name.lower(), item.lower()) < 3 or item.lower() == "all":
            taken = True
            if room_item.portable:
                if len(player.inventory) >= 3:
                    utils.output("You can't have more than 3 items in your inventory.", "magenta")
                    continue
                player.inventory.append(room_item)
                new_items.remove(room_item)
                utils.output(f"You have taken the {room_item.name}.", "clear")
                if room_item.updroomdesc is not None:
                    current_room.description = room_item.updroomdesc
            else:
                utils.output(f"You can't pick up the {room_item.name}. It can't be moved.", "magenta")
        #print([item.name for item in current_room.items])
    if not taken:
        utils.output(f"There is no {item} here.", "magenta")
    else:
        player.currentroom.items = list(new_items)

def trytoequip(item, player, map):
    for playeritem in player.inventory:
        if utils.levenshteinDistance(item.lower(), playeritem.name.lower()) < 3 and type(playeritem) == items.Weapon:
            if player.weapon.name.lower() != "fists":
                player.inventory.append(player.weapon)
            player.weapon = playeritem
            player.inventory.remove(playeritem)
            utils.output(f"You have equipped the {playeritem.name}.", "clear") 
            return
    utils.output(f"You don't have a weapon called {item}.", "magenta")
def trytodrop(item, player, map):
    current_room = player.currentroom
    dropped = False
    new_items = list(player.inventory)
    
    #print(current_room.items)
    for player_item in player.inventory:
        #print(room_item.name)
        if utils.levenshteinDistance(player_item.name.lower(), item.lower()) < 3 or item.lower() == "all":
            dropped = True
            new_items.remove(player_item)
            current_room.items.append(player_item)
            utils.output(f"You have dropped the {player_item.name}.", "clear")
    if not dropped:
        utils.output(f"You don't have a {item}.", "magenta")
    else:
        player.inventory = list(new_items)
def listinventory(player, map):
    # utils.output player information in a colored section
    utils.output(player.name, "green")

    showhpbar(player)

    if player.weapon is not None:
        utils.output("Current weapon:" + player.weapon.name, "clear")
    else:
        utils.output("Current weapon: None", "clear")

    # utils.output the inventory items in a colored section
    utils.output("You are carrying:", "clear")
    if not player.inventory:
        utils.output("Nothing.", "yellow")
    else:
        for item in player.inventory:
            utils.output(f"- {item.name}", "yellow")


def listenemies(player, map):
    current_room = player.currentroom

    if current_room.enemies == None:
        utils.output("There are no enemies here.", "clear")
        return

    for enemy in current_room.enemies:
        if enemy.alive:
            if isinstance(enemy, enemyObject.Boss):
                if map.level == map.all_levels:
                    utils.output(enemy.description + " It is the final boss.", "red")
                else:
                    utils.output(enemy.description + " It is the boss of this level.", "red")
            else:
                utils.output(enemy.description, "red")
        else:
            utils.output(enemy.deaddesc, "red")


def lookat(item, player, map):
    for room_item in player.currentroom.items:
        if utils.levenshteinDistance(room_item.name.lower(), item.lower()) < 3:
            utils.output(room_item.itemdesc, "bright_yellow")
            if room_item.revealsitem is not None:
                player.currentroom.items.append(room_item.revealsitem)
                utils.output(f"You also see {room_item.revealsitem.name}.", "yellow")
                player.currentroom.items[player.currentroom.items.index(room_item)].revealsitem = None
            return

    for inventory_item in player.inventory:
        if inventory_item.name.lower() == item.lower():
            utils.output(inventory_item.itemdesc, "bright_yellow")
            return

    utils.output(f"There is no {item} here.", "magenta")


def trytouse(item, player, map):
    current_room = player.currentroom

    for inventory_item in player.inventory:
        if utils.levenshteinDistance(inventory_item.name.lower(), item.lower()) < 3:
            if inventory_item.usedin == current_room.number or inventory_item.usedin == None:
                if isinstance(inventory_item, items.StatItem):
                    player.hp += inventory_item.hp_change
                    checkhp(player, map)
                if inventory_item.removesroomitem is not None:
                    current_room.items.remove(inventory_item.removesroomitem)
                if inventory_item.addsroomitem is not None:
                    current_room.items.append(inventory_item.addsroomitem)
                utils.output(inventory_item.usedesc, "yellow")
                inventory_item.usedin = 9999
                if inventory_item.useroomdesc != None:
                    current_room.description = inventory_item.useroomdesc
                if inventory_item.disposable == 1:
                    player.inventory.remove(inventory_item)
                return
            elif inventory_item.usedin == 9999:
                utils.output(f"You can't use the {inventory_item.name} again.", "magenta")
                return
            else:
                utils.output(f"You can't use the {inventory_item.name} here.", "magenta")
                return

    utils.output(f"You don't have the {item}.", "magenta")

def die(player, map):
    player.lives_remaining -= 1
    if player.lives_remaining == 0:
        utils.output("You have been defeated! You lose.", "bright_red")
        raise RuntimeError()
    utils.output(f"You have been defeated! Try again.", "bright_red")
    for item in player.inventory:
        player.currentroom.items.append(item)
    if player.weapon.name != "Fists":
        player.currentroom.items.append(player.weapon)
    player.inventory = []
    player.weapon = items.Weapon(0, "Fists", "Your fists, ready for punching", None, True, None, 0, None, None, None, None, 0, 0.5)
    player.hp = 10
    player.currentroom = map.rooms[0]
    sleep(0.5)

def castspell(spell, player, map):
    for mapspell in map.spells:
        if utils.levenshteinDistance(mapspell.name.lower(), spell.lower()) < 3:
            spell = mapspell
            break
    if type(spell) == str:
        utils.output("This spell does not exist.", "magenta")
        return
    if safetorun(spell):
        #print(spell.effect)
        utils.output(spell.description, "blue")
        exec(spell.effect)
        checkhp(player, map)
    else:
        utils.output("This spell has been disabled due to a potential security hazard.", "magenta")

def safetorun(spell):
    spell = spell.effect
    if "import" in spell or "utils.os" in spell or "utils.sys" in spell or "os" in spell or "pickle" in spell:
        return False
    return True

def settings():
    while True:
        utils.output("Settings", "cyan")
        for item in config.playerdata:
            if type(config.playerdata[item]) == str:
                utils.output(f" {item}: {config.playerdata[item]}", "bright_yellow")
            else:
                utils.output(f" {item}: {'Y' if config.playerdata[item] == 1 else 'n'}", "bright_yellow")
        
        utils.output(f"What would you like to change? (q to quit settings)", "clear")
        choice = utils.cinput().lower()
        
        if choice == 'q':
            raise RuntimeError()
        try:
            current_option = config.playerdata[choice]
        except:
            utils.output("That is not an option.", "magenta")
            continue
        
        if type(current_option) == int:
            new_entry = ''
            while new_entry.lower() not in ['y', 'n']:
                utils.output(f"Setting: {choice}\nCurrent entry: {'Y' if current_option == 1 else 'n'}\nNew entry: [Y/n]", "magenta")
                new_entry = utils.cinput()
                if new_entry.lower() not in ['y', 'n']:
                    utils.output("Please enter y or n", "magenta")
            new_entry = 0 if new_entry.lower() == 'n' else 1
        else:
            new_entry = ''
            while new_entry == '':
                utils.output(f"Setting: {choice}\nCurrent entry: {current_option}\nNew entry: ", "magenta")
                new_entry = utils.cinput()
                if new_entry == '':
                    utils.output("You have to have a name.", "magenta")
        
        config.playerdata[choice] = new_entry
        with open(config.playerdata_path, 'w') as file:
            json.dump(config.playerdata, file)
        config.playerdata, config.player_name, config.wants_colour, config.wants_scroll, config.wants_opening_text, config.wants_hardcore = config.load_preferences()

def save(player, map):
    dataToSave = [player, map]
    with open(os.path.join(config.config_home, "saveGame.pkl"), "wb") as saveFile:
        pickle.dump(dataToSave, saveFile)
    utils.output("Your game has been saved.", "magenta")
