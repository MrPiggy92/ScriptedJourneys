import config
import utils

import os
import json

utils.output("Welcome to Scripted Journeys, an enthralling text-based adventure where your decisions shape the narrative and uncover hidden mysteries across diverse realms. Each map teems with unique challenges, intricate plots, and fascinating characters, all waiting for you to explore and interact with. Your choices will determine your path, unlocking secrets, and altering the course of your journey in unexpected ways. Embark on a quest that combines storytelling, strategy, and imagination, where every script you write crafts your destiny. Are you ready to dive into a world where every decision is a step towards a new adventure?", "bold_pink", 0.02)

utils.output("What is your name, brave adventurer?", "magenta")
print(utils.colourify("magenta"))
name = input(" > ")
print(utils.colourify("clear"))
utils.output(f"Greetings {name}!\n\n", "magenta")

playerdata = {"name": name}

with open(os.path.join(config.playerdata_path, "playerdata.json"), 'w') as file:
    json.dump(playerdata, file)

