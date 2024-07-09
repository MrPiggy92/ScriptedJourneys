# Text adventure

# Room
class Room:
    def __init__(self, number, name, description, exits, key, items, enemies):
        self.number = number
        self.name = name
        self.description = description
        self.exits = exits
        self.key = key
        self.items = items
        self.enemies = enemies
