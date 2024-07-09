import utils, items

def showhpbar(player):
    # Calculate the percentage of hit points
    progress = player.hp / 10.0 * 100

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
    utils.output(f"HP: [{bar}] {player.hp}/10 HP", hp_color)
    return


def trytomove(direction, player):
    current_room = player.currentroom
    exits = current_room.exits
    
    direction = direction[0]

    if direction in ['N', 'S', 'E', 'W']:
        direction_index = ['N', 'S', 'E', 'W'].index(direction)
        if exits[direction_index] is not None:
            new_room = exits[direction_index]
            player.currentroom = new_room
            return
    utils.output("You can't go that way.", "magenta")


def tutorial():
    utils.output("To move, type 'MOVE <direction>'", "green")
    utils.output(' ', "green")
    utils.output("To fight, type 'FIGHT <enemy>", "green")
    utils.output(' ', "green")
    utils.output("To take an item in the room you're in, type 'TAKE <item>'. To use an item in your inventory, type 'USE <item>'. And to have a closer look at an item in the room, type 'LOOK <item>'.", "green")
    utils.output(' ', "green")
    utils.output("To list your inventory, just type 'INVENTORY'. This will show all your items, your HP, and your current weapon.", "green")
    utils.output(' ', "green")


def checkkeys(player):
    currentroom = player.currentroom
    if currentroom.key != None and currentroom.key in player.keyring:
        utils.output(currentroom.key.keyusedesc, "blue")
        currentroom.description = currentroom.key.keyroomdesc
        currentroom.exits = currentroom.key.keyexits
        currentroom.key = None


def listexits(player):
    if player.currentroom.exits[0] != None:
        utils.output("You see an exit to the North.", "blue")
    if player.currentroom.exits[1] != None:
        utils.output("You see an exit to the South.", "blue")
    if player.currentroom.exits[2] != None:
        utils.output("You see an exit to the East.", "blue")
    if player.currentroom.exits[3] != None:
        utils.output("You see an exit to the West.", "blue")


def fight(enemy_name, player):
    current_room = player.currentroom
    enemy = None

    if player.weapon is None:
        utils.output("You can't fight without a weapon!", "magenta")
        return

    for room_enemy in current_room.enemies:
        if room_enemy.name.lower() == enemy_name.lower():
            enemy = room_enemy
            break

    if enemy and enemy.alive:
        utils.output(f"A battle begins with the {enemy.name}!", "red")
        while enemy.alive and player.hp > 0:
            # Player's turn
            player_damage = player.weapon.damage
            enemy.hp -= player_damage
            utils.output(f"You hit the {enemy.name} with your {player.weapon.name}. It causes {player_damage} damage.", "green")

            # Check enemy's HP
            if enemy.hp <= 0:
                enemy.alive = False
                utils.output(f"The {enemy.name} has been defeated!", "red")
                lootbody(enemy, player)
                break

            # Enemy's turn
            enemy_damage = enemy.weapon.damage
            player.hp -= enemy_damage
            utils.output(f"The {enemy.name} hits you with its {enemy.weapon.name}. It causes {enemy_damage} damage.", "red")
            showhpbar(player)

            # Check player's HP
            checkhp(player)

        if player.hp <= 0:
            utils.output(f"You have been defeated! Game Over.", "red")
            exit(0)
    else:
        utils.output("There is no such enemy here.", "magenta")


def lootbody(enemy, player):
    current_room = player.currentroom

    utils.output(f"You defeated the {enemy.name} in combat!", "bright_yellow")
    utils.output(f"You find the following items on the {enemy.name}'s body:", "clear")

    if enemy.weapon != None:
        current_room.items.append(enemy.weapon)
        utils.output(f"- {enemy.weapon.name}", "yellow")

    if enemy.loot is not None:
        for item in enemy.loot:
            current_room.items.append(item)
            utils.output(f"- {item.name}", "yellow")

    # Remove the enemy from the room
    current_room.enemies.remove(enemy)


def checkhp(player):
    if player.hp > 10:
        player.hp = 10
    elif player.hp <= 0:
        utils.output("You have been killed! Game Over.", "bright_red")
        exit(0)


def listroomitems(player):
    current_room = player.currentroom
    if current_room.items:
        utils.output(f"You see the following items:", "clear")
        for item in current_room.items:
            utils.output("- " + item.name, "yellow")
    else:
        utils.output("There are no items here.", "blue")


def trytotake(item, player):
    current_room = player.currentroom

    for room_item in current_room.items:

        if room_item.name.lower() == item.lower():
            if isinstance(room_item, items.StatItem):
                player.hp += room_item.hp_change
                utils.output(room_item.usedesc, "green")
                current_room.items.remove(room_item)
                return

            if isinstance(room_item, items.Weapon):
                utils.output(f"You have taken the {room_item.name}.", "blue")
                player.weapon = room_item
                current_room.items.remove(room_item)
                return

            if room_item.portable:
                player.inventory.append(room_item)
                current_room.items.remove(room_item)
                utils.output(f"You have taken the {room_item.name}.", "blue")
                if room_item.updroomdesc is not None:
                    current_room.description = room_item.updroomdesc
            else:
                utils.output(f"You can't pick up the {room_item.name}. It can't be moved.", "magenta")
            return

    utils.output(f"There is no {item} here.", "magenta")


def listinventory(player):
    # utils.output player information in a colored section
    utils.output(player.name, "green")

    showhpbar(player)

    if player.weapon is not None:
        utils.output("Current weapon:" + player.weapon.name, "blue")
    else:
        utils.output("Current weapon: None", "blue")

    # utils.output the inventory items in a colored section
    utils.output("You are carrying:", "clear")
    if not player.inventory:
        utils.output("Nothing.", "yellow")
    else:
        for item in player.inventory:
            utils.output(f"- {item.name}", "yellow")


def listenemies(player):
    current_room = player.currentroom

    if current_room.enemies == None:
        utils.output("There are no enemies here.", "blue")
        return

    for enemy in current_room.enemies:
        if enemy.alive:
            utils.output(enemy.description, "red")
        else:
            utils.output(enemy.deaddesc, "red")


def lookat(item, player):
    for room_item in player.currentroom.items:
        if room_item.name.lower() == item.lower():
            utils.output(room_item.itemdesc, "bright_yellow")
            if room_item.revealsitem is not None:
                player.currentroom.items.append(room_item.revealsitem)
                utils.output(f"You also see {room_item.revealsitem.name}.", "yellow")
                player.currentroom.items[player.currentroom.items.index(room_item)].revealsitem = None
            return

    for inventory_item in player.inventory:
        if inventory_item.name.lower() == item.lower():
            utils.output(inventory_item.itemdesc)
            return

    utils.output(f"There is no {item} here.", "magenta")


def trytouse(item, player):
    current_room = player.currentroom

    for inventory_item in player.inventory:
        if inventory_item.name.lower() == item.lower():
            if inventory_item.usedin == current_room.number or inventory_item.usedin == None:
                if isinstance(inventory_item, items.StatItem):
                    player.hp += inventory_item.hp_change
                if inventory_item.removesroomitem is not None:
                    print(inventory_item.removesroomitem)
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
                utils.output(f"You can't use the {inventory_item.name} again here.", "magenta")
                return
            else:
                utils.output(f"You can't use the {inventory_item.name} here.", "magenta")
                return

    utils.output(f"You don't have the {item}.", "magenta")
