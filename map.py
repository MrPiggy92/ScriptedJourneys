# Text adventure

# Map
import rooms as roomsObject
import items
import enemy as enemyObject
import xml.etree.ElementTree as ET
import os

class Map:
    def __init__(self, folder):
        self.folder = folder
        self.items, self.rooms, self.enemies = self.load(folder)
        #self.rooms.append(room.Room(0, "chamber", "A big cave", [None, None, None, None], None, None, None))
        #self.rooms.append(room.Room(1, "room", "Another big cave", [None, None, None, None], None, None, None))
        #
        #self.rooms[0].exits = [self.rooms[1], None, None, None]
        #self.rooms[1].exits = [None, self.rooms[0], None, None]
    
    def load(self, folder):
        tree = ET.parse(os.path.join("/home/arco/Documents/Python/Text_adventure", folder, "lvl1.xml"))
        root = tree.getroot()
        
        mapitems = []
        for item in root.iter("item"):
            itemdata = []
            for data in item:
                try:
                    data.text = int(data.text)
                except:
                    pass
                itemdata.append(None if data.text == -1 else data.text)
                #print(None if data.text == -1 else data.text)
            #print(itemdata)
            mapitems.append(items.Item(itemdata[0], itemdata[1], itemdata[2], itemdata[3], itemdata[4], itemdata[5], itemdata[6], itemdata[7], itemdata[8], itemdata[9], itemdata[10], itemdata[11]))
        
        for item in mapitems:
            if item.revealsitem != None:
                item.revealsitem = mapitems[item.revealsitem]
            #if item.
        
        mapstatitems = []
        for statitem in root.iter("statitem"):
            statitemdata = []
            for data in statitem:
                try:
                    data.text = int(data.text)
                except:
                    pass
                statitemdata.append(None if data.text == -1 else data.text)
                #print(None if data.text == -1 else data.text)
            #print(statitemdata)
            mapstatitems.append(items.StatItem(statitemdata[0], statitemdata[1], statitemdata[2], statitemdata[3], statitemdata[4], statitemdata[5], statitemdata[6], statitemdata[7], statitemdata[8], statitemdata[9], statitemdata[10], statitemdata[11], statitemdata[12]))
        
        for statitem in mapstatitems:
            if statitem.revealsitem != None:
                statitem.revealsitem = mapstatitems[statitem.revealsitem]
            #if statitem.
        
        mapweapons = []
        for weapon in root.iter("weapon"):
            weapondata = []
            for data in weapon:
                try:
                    data.text = int(data.text)
                except:
                    pass
                weapondata.append(None if data.text == -1 else data.text)
                #print(None if data.text == -1 else data.text)
            #print(weapondata)
            #print(len(weapondata))
            mapweapons.append(items.Weapon(weapondata[0], weapondata[1], weapondata[2], weapondata[3], weapondata[4], weapondata[5], weapondata[6], weapondata[7], weapondata[8], weapondata[9], weapondata[10], weapondata[11], weapondata[12]))
        
        for weapon in mapweapons:
            if weapon.revealsitem != None:
                weapon.revealsitem = mapweapons[weapon.revealsitem]
        
        enemies = []
        for enemy in root.iter("enemy"):
            enemydata = []
            for data in enemy:
                if data.tag == "loot":
                    data.text = []
                    for item in data:
                        if item.tag == "lootitem":
                            data.text.append(mapitems[int(item.text)])
                try:
                    data.text = int(data.text)
                except:
                    pass
                enemydata.append(None if data.text == -1 else data.text)
                #print("hi")
            #print(len(enemydata))
            enemies.append(enemyObject.Enemy(enemydata[0], enemydata[1], True, enemydata[2], enemydata[3], mapweapons[enemydata[4]], enemydata[5], enemydata[6]))
        
        rooms = []
        for room in root.iter("room"):
            roomdata = []
            for data in room:
                if data.tag == "items":
                    data.text = []
                    for item in data:
                        if item.tag == "roomitem":
                            if item.text != "-1":
                                data.text.append(mapitems[int(item.text)])
                        elif item.tag == "roomstatitem":
                            if item.text != "-1":
                                data.text.append(mapstatitems[int(item.text)])
                        elif item.tag == "roomweapon":
                            if item.text != "-1":
                                data.text.append(mapweapons[int(item.text)])
                        else:
                            pass
                        
                elif data.tag == "exits":
                    data.text = []
                    for exit in data:
                        data.text.append(int(exit.text))
                elif data.tag == "enemies":
                    data.text = []
                    counter = 0
                    for enemy in data:
                        data.text.append(enemies[int(enemy.text)] if enemy.text != "-1" else None)
                        counter += 1
                    if counter == 0:
                        data.text = None
                else:
                    try:
                        data.text = int(data.text)
                    except:
                        pass
                roomdata.append(None if data.text == -1 else data.text)
            rooms.append(roomsObject.Room(roomdata[0], roomdata[1], roomdata[2], roomdata[3], roomdata[4], roomdata[5]))
        
        #print(f"h {rooms[1].exits}")
        for room in rooms:
            room.exits[0] = rooms[int(room.exits[0])] if room.exits[0] != -1 else None
            room.exits[1] = rooms[int(room.exits[1])] if room.exits[1] != -1 else None
            room.exits[2] = rooms[int(room.exits[2])] if room.exits[2] != -1 else None
            room.exits[3] = rooms[int(room.exits[3])] if room.exits[3] != -1 else None
        #print(rooms[0].exits)
        
        return mapitems, rooms, enemies
