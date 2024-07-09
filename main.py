#from colorama import Fore, Style
import time


class Room:
    def __init__(self, number, name, description, exits, key, items, enemies):
        self.number = number
        self.name = name
        self.description = description
        self.exits = exits
        self.key = key
        self.items = items
        self.enemies = enemies


class Player:
    def __init__(self, name, currentroom, keyring, hp, inventory, weapon):
        self.name = name
        self.currentroom = currentroom
        self.keyring = keyring
        self.hp = hp
        self.inventory = inventory
        self.weapon = weapon


class Item:
    def __init__(self, name, itemdesc, updroomdesc, portable, revealsitem, usedin, usedesc, removesroomitem,
                 addsroomitem, useroomdesc, disposable):
        self.name = name
        self.itemdesc = itemdesc
        self.updroomdesc = updroomdesc
        self.portable = portable
        self.revealsitem = revealsitem
        self.usedin = usedin
        self.usedesc = usedesc
        self.removesroomitem = removesroomitem
        self.addsroomitem = addsroomitem
        self.useroomdesc = useroomdesc
        self.disposable = disposable


class StatItem(Item):
    def __init__(self, name, itemdesc, updroomdesc, portable, revealsitem, usedin, usedesc, removesroomitem,
                 addsroomitem, useroomdesc, disposable, hp_change):
        super().__init__(name, itemdesc, updroomdesc, portable, revealsitem, usedin, usedesc, removesroomitem,
                         addsroomitem, useroomdesc, disposable)
        self.hp_change = hp_change


class Weapon(Item):
    def __init__(self, name, itemdesc, updroomdesc, portable, revealsitem, usedin, usedesc, removesroomitem,
                 addsroomitem, useroomdesc, disposable, damage, sound_path):
        super().__init__(name, itemdesc, updroomdesc, portable, revealsitem, usedin, usedesc, removesroomitem,
                         addsroomitem, useroomdesc, disposable)
        self.damage = damage
        self.sound_path = sound_path


class Enemy:
    def __init__(self, name, alive, description, deaddesc, weapon, hp, loot):
        self.name = name
        self.alive = alive
        self.description = description
        self.deaddesc = deaddesc
        self.weapon = weapon
        self.hp = hp
        self.loot = loot


def typewriter_effect(text, delay=0.01):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()


# Define the rooms, adding a name and description. No exits are set until all the rooms are declared.
rooms = [None for _ in range(12)]

rooms[0] = Room(0,'Entrance','You are standing in a cave entrance, many stalactites looming over your head.', [None,None,None,None], None, None, None)
rooms[1] = Room(1, 'Chamber', "You're standing in a dark cavern. You hear the sound of dripping water.")

# Define the items
bread = StatItem("Bread", "A loaf of fine Dwarfish Sabmel bread.", None, True, None, 0,"You eat the Sabmel bread. It's very refreshing. Gain 2HP.", None, None, None, True, 2)


#typewriter_effect(f"{Fore.GREEN}Type TUTORIAL for instructions{Style.RESET_ALL}\n\n")
typewriter_effect("What is your name, brave adventurer? ")
player_name = input()
typewriter_effect(f"Greetings {player_name}!")

player = Player(player_name, rooms[0], [], 10, [bread], None)


def showhpbar():
    # Calculate the percentage of hit points
    progress = player.hp / 10.0 * 100

    # Determine the color based on HP value
    if player.hp >= 7:
        hp_color = Fore.GREEN
    elif 4 <= player.hp <= 6:
        hp_color = Fore.YELLOW
    else:
        hp_color = Fore.RED
    hp_color = ''

    # Create the progress bar string manually
    bar_length = 20
    filled_length = int(bar_length * progress // 100)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)

    # Print the progress bar with the appropriate color
    typewriter_effect(hp_color + f"HP: [{bar}] {player.hp}/10 HP")
    return


def trytomove(direction):
    current_room = player.currentroom
    exits = current_room.exits

    if direction in ['N', 'S', 'E', 'W']:
        direction_index = ['N', 'S', 'E', 'W'].index(direction)
        if exits[direction_index] is not None:
            new_room = exits[direction_index]
            player.currentroom = new_room
            return
    typewriter_effect("You can't go that way.")


def tutorial():
    typewriter_effect("To move, type 'MOVE <direction>'")
    typewriter_effect(' ')
    typewriter_effect("To fight, type 'FIGHT <enemy>")
    typewriter_effect(' ')
    typewriter_effect(
        "To take an item in the room you're in, type 'TAKE <item>'. To use an item in your inventory, type 'USE <item>'. And to have a closer look at an item in the room, type 'LOOK <item>'.")
    typewriter_effect(' ')
    typewriter_effect(
        "To list your inventory, just type 'INVENTORY'. This will show all your items, your HP, and your current weapon.")
    typewriter_effect(' ')


def checkkeys():
    currentroom = player.currentroom
    if currentroom.key != None and currentroom.key in player.keyring:
        typewriter_effect(currentroom.key.keyusedesc)
        currentroom.description = currentroom.key.keyroomdesc
        currentroom.exits = currentroom.key.keyexits
        currentroom.key = None


checkkeys()


def listexits():
    if player.currentroom.exits[0] != None:
        typewriter_effect("You see an exit to the North.")
    if player.currentroom.exits[1] != None:
        typewriter_effect("You see an exit to the South.")
    if player.currentroom.exits[2] != None:
        typewriter_effect("You see an exit to the East.")
    if player.currentroom.exits[3] != None:
        typewriter_effect("You see an exit to the West.")


listexits()


def fight(enemy_name):
    current_room = player.currentroom
    enemy = None

    if player.weapon is None:
        typewriter_effect("You can't fight without a weapon!")
        return

    for room_enemy in current_room.enemies:
        if room_enemy.name.lower() == enemy_name.lower():
            enemy = room_enemy
            break

    if enemy and enemy.alive:
        #typewriter_effect(f"{Fore.RED}A battle begins with the {enemy.name}!{Style.RESET_ALL}")
        typewriter_effect(f"A battle begins with the {enemy.name}!")
        while enemy.alive and player.hp > 0:
            # Player's turn
            player_damage = player.weapon.damage
            enemy.hp -= player_damage
            # play_player_weapon_sound()
            #typewriter_effect(
            #    f"{Fore.GREEN}You hit the {enemy.name} with your {player.weapon.name}. It causes {player_damage} damage.{Style.RESET_ALL}")
            typewriter_effect(
                f"You hit the {enemy.name} with your {player.weapon.name}. It causes {player_damage} damage.")

            # Check enemy's HP
            if enemy.hp <= 0:
                enemy.alive = False
                #typewriter_effect(f"{Fore.RED}The {enemy.name} has been defeated!{Style.RESET_ALL}")
                typewriter_effect(f"The {enemy.name} has been defeated!")
                lootbody(enemy)
                break

            # Enemy's turn
            enemy_damage = enemy.weapon.damage
            player.hp -= enemy_damage
            # play_enemy_weapon_sound()
            #typewriter_effect(
            #    f"{Fore.RED}The {enemy.name} hits you with its {enemy.weapon.name}. It causes {enemy_damage} damage.{Style.RESET_ALL}")
            typewriter_effect(
                f"The {enemy.name} hits you with its {enemy.weapon.name}. It causes {enemy_damage} damage.")
            showhpbar()

            # Check player's HP
            checkhp()

        if player.hp <= 0:
            #typewriter_effect(f"{Fore.RED}You have been defeated! Game Over.{Style.RESET_ALL}")
            typewriter_effect(f"You have been defeated! Game Over.")
            exit(0)
    else:
        typewriter_effect("There is no such enemy here.")


def lootbody(enemy):
    current_room = player.currentroom

    typewriter_effect(f"You defeated the {enemy.name} in combat!")
    typewriter_effect(f"You find the following items on the {enemy.name}'s body:")

    if enemy.weapon != None:
        current_room.items.append(enemy.weapon)
        typewriter_effect(f"- {enemy.weapon.name}")

    if enemy.loot is not None:
        for item in enemy.loot:
            current_room.items.append(item)
            typewriter_effect(f"- {item.name}")

    # Remove the enemy from the room
    current_room.enemies.remove(enemy)


def checkhp():
    if player.hp > 10:
        player.hp = 10
    elif player.hp <= 0:
        typewriter_effect("You have been killed! Game Over.")
        exit(0)


def listroomitems():
    current_room = player.currentroom
    if current_room.items:
        typewriter_effect(f"You see the following items:{Fore.YELLOW}")
        for item in current_room.items:
            typewriter_effect("- " + item.name)
        print(Style.RESET_ALL)
    else:
        typewriter_effect("There are no items in this area.")


def trytotake(item):
    current_room = player.currentroom

    for room_item in current_room.items:

        if room_item.name.lower() == item.lower():
            if isinstance(room_item, StatItem):
                player.hp += room_item.hp_change
                typewriter_effect(room_item.usedesc)
                return

            if isinstance(room_item, Weapon):
                typewriter_effect(f"You have taken the {room_item.name}.")
                player.weapon = room_item
                current_room.items.remove(room_item)
                return

            if room_item.portable:
                player.inventory.append(room_item)
                current_room.items.remove(room_item)
                typewriter_effect(f"You have taken the {room_item.name}.")
                if room_item.updroomdesc is not None:
                    current_room.description = room_item.updroomdesc
            else:
                typewriter_effect(f"You can't pick up the {room_item.name}. It can't be moved.")
            return

    typewriter_effect(f"There is no {item} here.")


def listinventory():
    # typewriter_effect player information in a colored section
    #typewriter_effect(Fore.YELLOW + player.name)
    typewriter_effect(player.name)

    showhpbar()

    if player.weapon is not None:
        #typewriter_effect(Fore.BLUE + "Current weapon:" + player.weapon.name)
        typewriter_effect("Current weapon:" + player.weapon.name)
    else:
        #typewriter_effect(Fore.BLUE + "Current weapon: None")
        typewriter_effect("Current weapon: None")

    typewriter_effect(Style.RESET_ALL)

    # typewriter_effect the inventory items in a colored section
    typewriter_effect("You are carrying:")
    if not player.inventory:
        typewriter_effect("Nothing.")
    else:
        for item in player.inventory:
            typewriter_effect(f"- {item.name}")
    typewriter_effect(Style.RESET_ALL)


def listenemies():
    current_room = player.currentroom

    if current_room.enemies == None:
        typewriter_effect("There are no enemies here.")
        return

    for enemy in current_room.enemies:
        if enemy.alive:
            typewriter_effect(enemy.description)
        else:
            typewriter_effect(enemy.deaddesc)


def lookat(item):
    for room_item in player.currentroom.items:
        if room_item.name.lower() == item.lower():
            typewriter_effect(room_item.itemdesc)
            if room_item.revealsitem is not None:
                player.currentroom.items.append(room_item.revealsitem)
                typewriter_effect(f"You also see {room_item.revealsitem.name}.")
                player.currentroom.items[player.currentroom.items.index(room_item)].revealsitem = None
            return

    for inventory_item in player.inventory:
        if inventory_item.name.lower() == item.lower():
            typewriter_effect(inventory_item.itemdesc)
            return

    typewriter_effect(f"There is no {item} here.")


def trytouse(item):
    current_room = player.currentroom

    for inventory_item in player.inventory:
        if inventory_item.name.lower() == item.lower():
            if inventory_item.usedin == current_room.number or inventory_item.usedin == 0:
                if isinstance(inventory_item, StatItem):
                    player.hp += inventory_item.hp_change
                if inventory_item.removesroomitem is not None:
                    current_room.items.remove(inventory_item.removesroomitem)
                if inventory_item.addsroomitem is not None:
                    current_room.items.append(inventory_item.addsroomitem)
                typewriter_effect(inventory_item.usedesc)
                inventory_item.usedin = 9999
                if inventory_item.useroomdesc != None:
                    current_room.description = inventory_item.useroomdesc
                if inventory_item.disposable == True:
                    player.inventory.remove(inventory_item)
                return
            else:
                typewriter_effect(f"You can't use the {inventory_item.name} here.")
                return

    typewriter_effect(f"You don't have the {item}.")



while True:
    checkhp()
    #typewriter_effect(Fore.CYAN + Style.BRIGHT + player.currentroom.name + Style.RESET_ALL)
    #typewriter_effect(Fore.WHITE + player.currentroom.description)
    typewriter_effect(player.currentroom.name)
    typewriter_effect(player.currentroom.description)
    checkkeys()
    listroomitems()
    listenemies()
    listexits()

    action_input = input("What would you like to do? ")

    if action_input.lower().startswith("take "):
        item_name = action_input[5:]
        trytotake(item_name)
    elif action_input.lower() == "inventory":
        listinventory()
    elif action_input.lower().startswith("look "):
        item_name = action_input[5:]
        lookat(item_name)
    elif action_input.lower().startswith("use "):
        item_name = action_input[4:]
        trytouse(item_name)
    elif action_input.lower().startswith("fight "):
        enemy_name = action_input[6:]
        fight(enemy_name)
    elif action_input.lower().startswith("move "):
        trytomove(action_input.upper()[5:])
    elif action_input.lower().startswith("quit"):
        raise SystemExit()
    elif action_input.lower().startswith("tutorial"):
        tutorial()
    else:
        typewriter_effect("You can't do that.")
