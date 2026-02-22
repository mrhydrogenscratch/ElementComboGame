import pygame
import json
import math
import random
import os
import sys

pygame.init()

# ── Constants ──────────────────────────────────────────────────────────
WIDTH, HEIGHT = 1200, 700
CANVAS_W = 900
SIDEBAR_W = 300
INPUT_H = 50
CANVAS_H = HEIGHT - INPUT_H
FPS = 60

THEMES = {
    "dark": {
        "bg": (43, 43, 43), "sidebar_bg": (35, 35, 35), "input_bg": (50, 50, 50),
        "grid_dot": (55, 55, 55), "text": (255, 255, 255), "gold": (255, 215, 0),
        "text_secondary": (180, 180, 180), "text_dim": (100, 100, 100),
        "panel": (45, 45, 45), "panel_border": (100, 100, 100),
        "btn_bg": (80, 80, 80), "btn_border": (120, 120, 120),
        "row_bg": (55, 55, 55), "row_active": (65, 65, 75),
        "input_field": (60, 60, 60), "shadow": (20, 20, 20),
        "overlay": (0, 0, 0, 140), "close_btn": (120, 50, 50),
        "hint_text": (180, 220, 255),
    },
    "light": {
        "bg": (230, 230, 230), "sidebar_bg": (240, 240, 240), "input_bg": (220, 220, 220),
        "grid_dot": (210, 210, 210), "text": (30, 30, 30), "gold": (180, 140, 0),
        "text_secondary": (80, 80, 80), "text_dim": (160, 160, 160),
        "panel": (245, 245, 245), "panel_border": (180, 180, 180),
        "btn_bg": (200, 200, 200), "btn_border": (160, 160, 160),
        "row_bg": (225, 225, 225), "row_active": (210, 215, 230),
        "input_field": (235, 235, 235), "shadow": (180, 180, 180),
        "overlay": (255, 255, 255, 140), "close_btn": (200, 80, 80),
        "hint_text": (40, 80, 180),
    },
}

CATEGORY_COLORS_DARK = {
    "earth": (139, 90, 43),
    "fire": (200, 50, 30),
    "water": (40, 100, 200),
    "air": (135, 190, 220),
    "nature": (50, 160, 50),
    "life": (200, 170, 40),
    "arcane": (140, 70, 180),
    "material": (50, 150, 140),
    "machine": (120, 120, 130),
}

CATEGORY_COLORS_LIGHT = {
    "earth": (160, 110, 60),
    "fire": (210, 70, 50),
    "water": (50, 110, 210),
    "air": (100, 160, 200),
    "nature": (60, 170, 60),
    "life": (190, 160, 30),
    "arcane": (150, 80, 190),
    "material": (60, 160, 150),
    "machine": (130, 130, 140),
}

ELEMENT_CATEGORIES = {
    # Base (tier 0)
    "earth": "earth", "fire": "fire", "water": "water", "air": "air",
    # Tier 1
    "mud": "earth", "steam": "water", "lava": "fire", "dust": "earth",
    "rain": "water", "energy": "arcane", "stone": "earth", "smoke": "fire",
    "cloud": "air", "wave": "water", "ocean": "water", "bonfire": "fire",
    # Tier 2
    "plant": "nature", "sand": "earth", "glass": "material", "metal": "material",
    "clay": "earth", "obsidian": "earth", "brick": "material", "storm": "air",
    "lightning": "arcane", "ice": "water", "snow": "air", "geyser": "water",
    "volcano": "fire", "swamp": "nature",
    # Tier 3
    "tree": "nature", "flower": "nature", "algae": "nature", "moss": "nature",
    "life": "life", "fossil": "earth", "blade": "material", "wire": "material",
    "electricity": "arcane", "thunder": "air", "blizzard": "air", "mountain": "earth",
    "island": "earth", "beach": "earth",
    # Tier 4
    "wood": "nature", "paper": "material", "seed": "nature", "fruit": "nature",
    "animal": "life", "human": "life", "fish": "life", "bird": "life",
    "coal": "earth", "diamond": "earth", "sword": "machine", "tool": "machine",
    "battery": "machine", "magnet": "machine", "tsunami": "water",
    # Tier 5
    "house": "machine", "boat": "machine", "wheel": "machine", "engine": "machine",
    "computer": "machine", "phone": "machine", "book": "machine", "music": "arcane",
    "art": "arcane", "philosophy": "arcane", "love": "arcane",
    "dragon": "life", "unicorn": "life", "forest": "nature",
    # Tier 6
    "car": "machine", "airplane": "machine", "internet": "machine", "robot": "machine",
    "phoenix": "life", "city": "machine",
    # Tier 7
    "garden": "nature", "ash": "earth", "charcoal": "earth", "telescope": "machine",
    "star": "fire", "sun": "fire", "moon": "arcane", "skeleton": "arcane",
    "ghost": "arcane", "castle": "machine", "king": "life", "war": "arcane",
    "peace": "arcane", "glass bottle": "material", "potion": "arcane",
    "witch": "life", "werewolf": "life", "vampire": "life", "skeleton key": "material",
    "prison": "machine", "freedom": "arcane",

    # New elements for 2.0.0 update
    # Tier 1
    "light": "arcane",
    "heat": "fire",
    "pressure": "earth",
    "sound": "air",
    "energy": "arcane",
    # Tier 2
    "ash": "earth",
    "fog": "air",
    "swamp": "nature",
    "crystal": "material",
    "volcanic ash": "earth",
    "sandstorm": "air",
    "rainforest": "nature",
    "cave": "earth",
    "coral": "nature",
    "geyser": "water",
    # Tier 3
    "lightning rod": "machine",
    "storm cloud": "air",
    "quicksand": "earth",
    "lava flow": "fire",
    "tsunami": "water",
    "fossil fuel": "earth",
    "magma": "fire",
    "comet": "arcane",
    "meteor": "arcane",
    "aurora": "arcane",
    # Tier 4
    "obsidian blade": "material",
    "crystal ball": "arcane",
    "volcano eruption": "fire",
    "solar flare": "fire",
    "glacier": "water",
    "rainbow": "arcane",
    "hurricane": "air",
    "tornado": "air",
    "quarry": "earth",
    "mine": "earth",
    # Tier 5
    "robotic arm": "machine",
    "factory": "machine",
    "spaceship": "machine",
    "satellite": "machine",
    "black hole": "arcane",
    "nebula": "arcane",
    "constellation": "arcane",
    "time machine": "arcane",
    "magic wand": "arcane",
    "phoenix egg": "life",
    # Tier 6
    "artificial intelligence": "machine",
    "terraformer": "machine",
    "fusion reactor": "machine",
    "hoverboard": "machine",
    "force field": "arcane",
    "wormhole": "arcane",
    "parallel universe": "arcane",
    "time crystal": "arcane",
    "dragon egg": "life",
    "phoenix feather": "life",
    # Tier 7
    "quantum computer": "machine",
    "space station": "machine",
    "galaxy": "arcane",
    "multiverse": "arcane",
    "eternal flame": "fire",
    "life tree": "nature",
    "cosmic energy": "arcane",
    "stardust": "arcane",
    "supernova": "arcane",
    "universe": "arcane",
    # New elements for 2.1.0 update
    # Tier 3
    "obsidian": "material",
    "geyser steam": "water",
    "mudslide": "earth",
    "quartz": "material",
    "pearl": "material",
    "coral reef": "nature",
    "mossy rock": "nature",
    "lava stone": "earth",
    "volcanic glass": "material",
    "hot spring": "water",
    # Tier 4
    "meteorite": "earth",
    "fossil": "earth",
    "stalactite": "earth",
    "stalagmite": "earth",
    "cave painting": "arcane",
    "crystal shard": "material",
    "glacial ice": "water",
    "iceberg": "water",
    "desert rose": "nature",
    "oasis": "nature",
    # Tier 5
    "volcanic eruption": "fire",
    "lava tube": "earth",
    "fossilized tree": "earth",
    "ancient ruins": "arcane",
    "aurora borealis": "arcane",
    "storm surge": "water",
    "light prism": "arcane",
    "diamond shard": "material",
    "meteor shower": "arcane",
    "comet tail": "arcane",
    # Tier 6
    "black diamond": "material",
    "crystal cave": "arcane",
    "volcanic island": "earth",
    "supervolcano": "fire",
    "ice cave": "water",
    "frozen lake": "water",
    "enchanted forest": "nature",
    "ancient artifact": "arcane",
    "star fragment": "arcane",
    "cosmic storm": "arcane",
    "nebula cloud": "arcane",
    "wormhole portal": "arcane",
    "galactic core": "arcane",
}

RECIPES = {
    # Tier 1 - base combos
    frozenset(["earth", "water"]): "mud",
    frozenset(["fire", "water"]): "steam",
    frozenset(["earth", "fire"]): "lava",
    frozenset(["earth", "air"]): "dust",
    frozenset(["water", "air"]): "rain",
    frozenset(["fire", "air"]): "energy",
    frozenset(["air", "air"]): "cloud",
    frozenset(["water", "water"]): "ocean",
    frozenset(["fire", "fire"]): "bonfire",
    frozenset(["earth", "earth"]): "stone",
    frozenset(["energy", "water"]): "wave",
    frozenset(["energy", "air"]): "smoke",
    # Tier 2
    frozenset(["mud", "fire"]): "clay",
    frozenset(["mud", "plant"]): "swamp",
    frozenset(["rain", "earth"]): "plant",
    frozenset(["stone", "fire"]): "metal",
    frozenset(["stone", "air"]): "sand",
    frozenset(["sand", "fire"]): "glass",
    frozenset(["lava", "water"]): "obsidian",
    frozenset(["lava", "air"]): "stone",
    frozenset(["clay", "fire"]): "brick",
    frozenset(["cloud", "air"]): "storm",
    frozenset(["storm", "energy"]): "lightning",
    frozenset(["storm", "fire"]): "lightning",
    frozenset(["cloud", "water"]): "snow",
    frozenset(["rain", "rain"]): "storm",
    frozenset(["ocean", "air"]): "wave",
    frozenset(["water", "stone"]): "geyser",
    frozenset(["lava", "earth"]): "volcano",
    frozenset(["snow", "water"]): "ice",
    frozenset(["steam", "air"]): "cloud",
    frozenset(["smoke", "water"]): "cloud",
    frozenset(["bonfire", "earth"]): "coal",
    # Tier 3
    frozenset(["plant", "water"]): "tree",
    frozenset(["plant", "earth"]): "flower",
    frozenset(["plant", "ocean"]): "algae",
    frozenset(["plant", "stone"]): "moss",
    frozenset(["lightning", "ocean"]): "life",
    frozenset(["energy", "swamp"]): "life",
    frozenset(["stone", "stone"]): "mountain",
    frozenset(["ocean", "earth"]): "island",
    frozenset(["sand", "ocean"]): "beach",
    frozenset(["metal", "stone"]): "blade",
    frozenset(["metal", "lightning"]): "wire",
    frozenset(["wire", "energy"]): "electricity",
    frozenset(["storm", "storm"]): "thunder",
    frozenset(["snow", "storm"]): "blizzard",
    frozenset(["stone", "life"]): "fossil",
    # Tier 4
    frozenset(["tree", "fire"]): "coal",
    frozenset(["tree", "blade"]): "wood",
    frozenset(["wood", "water"]): "paper",
    frozenset(["flower", "water"]): "seed",
    frozenset(["tree", "water"]): "fruit",
    frozenset(["life", "earth"]): "animal",
    frozenset(["life", "clay"]): "human",
    frozenset(["life", "water"]): "fish",
    frozenset(["life", "air"]): "bird",
    frozenset(["coal", "earth"]): "diamond",
    frozenset(["blade", "wood"]): "sword",
    frozenset(["metal", "wood"]): "tool",
    frozenset(["electricity", "metal"]): "battery",
    frozenset(["electricity", "stone"]): "magnet",
    frozenset(["ocean", "storm"]): "tsunami",
    frozenset(["tree", "tree"]): "forest",
    # Tier 5
    frozenset(["brick", "wood"]): "house",
    frozenset(["wood", "ocean"]): "boat",
    frozenset(["stone", "tool"]): "wheel",
    frozenset(["metal", "energy"]): "engine",
    frozenset(["electricity", "glass"]): "computer",
    frozenset(["computer", "wave"]): "phone",
    frozenset(["paper", "human"]): "book",
    frozenset(["air", "human"]): "music",
    frozenset(["fire", "human"]): "art",
    frozenset(["human", "human"]): "love",
    frozenset(["human", "cloud"]): "philosophy",
    frozenset(["fire", "bird"]): "dragon",
    frozenset(["animal", "lightning"]): "dragon",
    frozenset(["animal", "diamond"]): "unicorn",
    # Tier 6
    frozenset(["engine", "wheel"]): "car",
    frozenset(["engine", "bird"]): "airplane",
    frozenset(["computer", "computer"]): "internet",
    frozenset(["computer", "human"]): "robot",
    frozenset(["fire", "dragon"]): "phoenix",
    frozenset(["house", "house"]): "city",
    # 21 new recipes
    frozenset(["flower", "flower"]): "garden",
    frozenset(["bonfire", "wood"]): "ash",
    frozenset(["ash", "fire"]): "charcoal",
    frozenset(["glass", "star"]): "telescope",
    frozenset(["energy", "fire"]): "star",
    frozenset(["star", "star"]): "sun",
    frozenset(["sun", "stone"]): "moon",
    frozenset(["fossil", "energy"]): "skeleton",
    frozenset(["skeleton", "air"]): "ghost",
    frozenset(["house", "stone"]): "castle",
    frozenset(["human", "castle"]): "king",
    frozenset(["sword", "sword"]): "war",
    frozenset(["love", "war"]): "peace",
    frozenset(["glass", "water"]): "glass bottle",
    frozenset(["glass bottle", "plant"]): "potion",
    frozenset(["human", "potion"]): "witch",
    frozenset(["animal", "moon"]): "werewolf",
    frozenset(["life", "moon"]): "vampire",
    frozenset(["skeleton", "metal"]): "skeleton key",
    frozenset(["brick", "metal"]): "prison",
    frozenset(["prison", "skeleton key"]): "freedom",
    # New recipes introduced in 1.1.0
    frozenset(["fire", "stone"]): "lava",  # Alternate way to create lava
    frozenset(["water", "fire"]): "steam",  # Alternate way to create steam
    frozenset(["fire", "cloud"]): "storm",  # Alternate way to create storm
    frozenset(["fire", "rain"]): "steam",  # Alternate way to create steam
    frozenset(["fire", "ice"]): "water",  # Melt ice into water
    frozenset(["air", "smoke"]): "cloud",  # Alternate way to create cloud
    frozenset(["earth", "smoke"]): "dust",  # Alternate way to create dust
    frozenset(["water", "sand"]): "mud",  # Alternate way to create mud
    frozenset(["fire", "metal"]): "tool",  # Alternate way to create tool
    frozenset(["fire", "wood"]): "coal",  # Alternate way to create coal
    frozenset(["water", "wood"]): "tree",  # Alternate way to create tree
    frozenset(["air", "wood"]): "smoke",  # Burn wood to create smoke
    frozenset(["earth", "wood"]): "forest",  # Alternate way to create forest
    frozenset(["water", "coal"]): "mud",  # Coal and water create mud
    frozenset(["fire", "coal"]): "ash",  # Alternate way to create ash
    frozenset(["air", "coal"]): "smoke",  # Alternate way to create smoke
    frozenset(["fire", "tool"]): "sword",  # Alternate way to create sword
    frozenset(["water", "tool"]): "magnet",  # Alternate way to create magnet
    frozenset(["air", "tool"]): "battery",  # Alternate way to create battery
    frozenset(["earth", "tool"]): "brick",  # Alternate way to create brick
    frozenset(["fire", "storm"]): "lightning",  # Alternate way to create lightning
    frozenset(["water", "storm"]): "tsunami",  # Alternate way to create tsunami
    frozenset(["air", "storm"]): "blizzard",  # Alternate way to create blizzard
    frozenset(["earth", "storm"]): "volcano",  # Alternate way to create volcano
    frozenset(["fire", "life"]): "phoenix",  # Alternate way to create phoenix
    frozenset(["air", "life"]): "bird",  # Alternate way to create bird
    frozenset(["water", "life"]): "fish",  # Alternate way to create fish
    frozenset(["earth", "life"]): "animal",  # Alternate way to create animal
    frozenset(["fire", "love"]): "art",  # Alternate way to create art
    frozenset(["air", "love"]): "music",  # Alternate way to create music
    frozenset(["earth", "love"]): "philosophy",  # Alternate way to create philosophy
    frozenset(["fire", "dragon"]): "phoenix",  # Alternate way to create phoenix
    frozenset(["fire", "flower"]): "ash",  # Burn flower to create ash
    frozenset(["water", "flower"]): "fruit",  # Alternate way to create fruit
    frozenset(["earth", "flower"]): "seed",  # Alternate way to create seed
    frozenset(["fire", "tree"]): "ash",  # Burn tree to create ash
    frozenset(["water", "tree"]): "fruit",  # Alternate way to create fruit
    frozenset(["earth", "tree"]): "forest",  # Alternate way to create forest
    frozenset(["fire", "ocean"]): "steam",  # Alternate way to create steam
    frozenset(["air", "ocean"]): "wave",  # Alternate way to create wave
    frozenset(["earth", "ocean"]): "island",  # Alternate way to create island
    frozenset(["fire", "mountain"]): "volcano",  # Alternate way to create volcano
    frozenset(["water", "mountain"]): "geyser",  # Alternate way to create geyser
    frozenset(["air", "mountain"]): "storm",  # Alternate way to create storm
    frozenset(["fire", "snow"]): "water",  # Melt snow into water
    frozenset(["air", "snow"]): "blizzard",  # Alternate way to create blizzard
    frozenset(["fire", "coal"]): "diamond",  # Alternate way to create diamond
    frozenset(["fire", "metal"]): "tool",  # Alternate way to create tool
    frozenset(["fire", "sword"]): "war",  # Alternate way to create war
    frozenset(["love", "war"]): "peace",  # Alternate way to create peace
    frozenset(["fire", "castle"]): "ash",  # Burn castle to create ash
    frozenset(["fire", "book"]): "ash",  # Burn book to create ash
    frozenset(["fire", "paper"]): "ash",  # Burn paper to create ash
    frozenset(["fire", "forest"]): "ash",  # Burn forest to create ash
    frozenset(["fire", "bird"]): "phoenix",  # Alternate way to create phoenix
    frozenset(["fire", "animal"]): "dragon",  # Alternate way to create dragon
    frozenset(["fire", "human"]): "ghost",  # Alternate way to create ghost
    frozenset(["fire", "love"]): "art",  # Alternate way to create art
    frozenset(["fire", "philosophy"]): "war",  # Alternate way to create war
    frozenset(["fire", "witch"]): "ash",  # Burn witch to create ash
    frozenset(["fire", "vampire"]): "ash",  # Burn vampire to create ash
    frozenset(["fire", "werewolf"]): "ash",  # Burn werewolf to create ash
    frozenset(["fire", "skeleton"]): "ash",  # Burn skeleton to create ash
    frozenset(["fire", "ghost"]): "ash",  # Burn ghost to create ash
    frozenset(["fire", "king"]): "ash",  # Burn king to create ash
    frozenset(["fire", "prison"]): "freedom",  # Burn prison to create freedom
    frozenset(["fire", "freedom"]): "ash",  # Burn freedom to create ash
    frozenset(["fire", "moon"]): "ash",  # Burn moon to create ash
    frozenset(["fire", "sun"]): "ash",  # Burn sun to create ash
    frozenset(["fire", "star"]): "ash",  # Burn star to create ash
    frozenset(["fire", "telescope"]): "ash",  # Burn telescope to create ash
    frozenset(["fire", "skeleton key"]): "ash",  # Burn skeleton key to create ash
    frozenset(["fire", "potion"]): "ash",  # Burn potion to create ash
    frozenset(["fire", "glass bottle"]): "ash",  # Burn glass bottle to create ash
    # new recipes introduced in 2.0.0 update
    # Tier 1
    frozenset(["fire", "air"]): "heat",
    frozenset(["earth", "earth"]): "pressure",
    frozenset(["air", "energy"]): "sound",
    frozenset(["light", "air"]): "energy",
    # Tier 2
    frozenset(["fire", "stone"]): "volcanic ash",
    frozenset(["sand", "wind"]): "sandstorm",
    frozenset(["rain", "forest"]): "rainforest",
    frozenset(["mountain", "stone"]): "cave",
    frozenset(["ocean", "flower"]): "coral",
    frozenset(["water", "stone"]): "geyser",
    frozenset(["light", "diamond"]): "crystal",
    frozenset(["fog", "light"]): "rainbow",
    # Tier 3
    frozenset(["lightning", "metal"]): "lightning rod",
    frozenset(["storm", "cloud"]): "storm cloud",
    frozenset(["sand", "water"]): "quicksand",
    frozenset(["lava", "water"]): "lava flow",
    frozenset(["ocean", "storm"]): "tsunami",
    frozenset(["coal", "pressure"]): "fossil fuel",
    frozenset(["volcano", "lava"]): "magma",
    frozenset(["star", "stone"]): "meteor",
    frozenset(["ice", "star"]): "comet",
    frozenset(["light", "storm"]): "aurora",
    # Tier 4
    frozenset(["crystal", "blade"]): "obsidian blade",
    frozenset(["crystal", "glass"]): "crystal ball",
    frozenset(["volcano", "eruption"]): "volcano eruption",
    frozenset(["sun", "fire"]): "solar flare",
    frozenset(["ice", "mountain"]): "glacier",
    frozenset(["rain", "light"]): "rainbow",
    frozenset(["storm", "ocean"]): "hurricane",
    frozenset(["storm", "sand"]): "tornado",
    frozenset(["mountain", "tool"]): "quarry",
    frozenset(["earth", "tool"]): "mine",
    # Tier 5
    frozenset(["robot", "tool"]): "robotic arm",
    frozenset(["robot", "factory"]): "factory",
    frozenset(["engine", "star"]): "spaceship",
    frozenset(["metal", "satellite"]): "satellite",
    frozenset(["black hole", "star"]): "nebula",
    frozenset(["star", "star"]): "constellation",
    frozenset(["time", "machine"]): "time machine",
    frozenset(["wand", "magic"]): "magic wand",
    frozenset(["fire", "egg"]): "phoenix egg",
    # Tier 6
    frozenset(["robot", "intelligence"]): "artificial intelligence",
    frozenset(["machine", "earth"]): "terraformer",
    frozenset(["energy", "reactor"]): "fusion reactor",
    frozenset(["tool", "air"]): "hoverboard",
    frozenset(["energy", "shield"]): "force field",
    frozenset(["black hole", "galaxy"]): "wormhole",
    frozenset(["galaxy", "galaxy"]): "parallel universe",
    frozenset(["crystal", "time"]): "time crystal",
    frozenset(["dragon", "egg"]): "dragon egg",
    frozenset(["phoenix", "fire"]): "phoenix feather",
    # Tier 7
    frozenset(["computer", "time"]): "quantum computer",
    frozenset(["spaceship", "satellite"]): "space station",
    frozenset(["galaxy", "star"]): "multiverse",
    frozenset(["fire", "galaxy"]): "eternal flame",
    frozenset(["tree", "life"]): "life tree",
    frozenset(["energy", "star"]): "cosmic energy",
    frozenset(["meteor", "star"]): "stardust",
    frozenset(["star", "explosion"]): "supernova",
    frozenset(["supernova", "galaxy"]): "universe",
    # New recipes for 2.1.0 update
    # Tier 3
    frozenset(["lava", "water"]): "obsidian",
    frozenset(["geyser", "steam"]): "geyser steam",
    frozenset(["mud", "landslide"]): "mudslide",
    frozenset(["crystal", "pressure"]): "quartz",
    frozenset(["oyster", "sand"]): "pearl",
    frozenset(["coral", "reef"]): "coral reef",
    frozenset(["moss", "rock"]): "mossy rock",
    frozenset(["lava", "stone"]): "lava stone",
    frozenset(["volcano", "glass"]): "volcanic glass",
    frozenset(["hot", "water"]): "hot spring",
    # Tier 4
    frozenset(["meteor", "earth"]): "meteorite",
    frozenset(["bone", "earth"]): "fossil",
    frozenset(["cave", "water"]): "stalactite",
    frozenset(["cave", "earth"]): "stalagmite",
    frozenset(["cave", "paint"]): "cave painting",
    frozenset(["crystal", "shard"]): "crystal shard",
    frozenset(["glacier", "ice"]): "glacial ice",
    frozenset(["ice", "ocean"]): "iceberg",
    frozenset(["desert", "flower"]): "desert rose",
    frozenset(["desert", "water"]): "oasis",
    # Tier 5
    frozenset(["volcano", "eruption"]): "volcanic eruption",
    frozenset(["lava", "cave"]): "lava tube",
    frozenset(["tree", "fossil"]): "fossilized tree",
    frozenset(["cave", "history"]): "ancient ruins",
    frozenset(["aurora", "north"]): "aurora borealis",
    frozenset(["storm", "ocean"]): "storm surge",
    frozenset(["light", "glass"]): "light prism",
    frozenset(["diamond", "shard"]): "diamond shard",
    frozenset(["meteor", "storm"]): "meteor shower",
    frozenset(["comet", "tail"]): "comet tail",
    # Tier 6
    frozenset(["diamond", "pressure"]): "black diamond",
    frozenset(["cave", "crystal"]): "crystal cave",
    frozenset(["volcano", "island"]): "volcanic island",
    frozenset(["volcano", "eruption"]): "supervolcano",
    frozenset(["cave", "ice"]): "ice cave",
    frozenset(["lake", "ice"]): "frozen lake",
    frozenset(["forest", "magic"]): "enchanted forest",
    frozenset(["artifact", "history"]): "ancient artifact",
    frozenset(["star", "meteor"]): "star fragment",
    frozenset(["storm", "galaxy"]): "cosmic storm",
    frozenset(["nebula", "cloud"]): "nebula cloud",
    frozenset(["wormhole", "portal"]): "wormhole portal",
    frozenset(["galaxy", "core"]): "galactic core",
}

SAVES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saves")
os.makedirs(SAVES_DIR, exist_ok=True)
BASE_ELEMENTS = {"earth", "fire", "water", "air"}
OVERLAP_THRESHOLD = 0.30
MERGE_SOUND_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "merge_sound.wav")

# ── Compute element tiers via BFS ──────────────────────────────────────
ELEMENT_TIERS = {n: 0 for n in BASE_ELEMENTS}
_changed = True
while _changed:
    _changed = False
    for _k, _v in RECIPES.items():
        if all(_n in ELEMENT_TIERS for _n in _k) and _v not in ELEMENT_TIERS:
            ELEMENT_TIERS[_v] = max(ELEMENT_TIERS[_n] for _n in _k) + 1
            _changed = True


# ── Element ────────────────────────────────────────────────────────────
class Element:
    FONT = None
    STAR_FONT = None
    HEIGHT = 40
    RADIUS = 10

    def __init__(self, name: str, x: float, y: float):
        self.name = name
        if Element.FONT is None:
            Element.FONT = pygame.font.SysFont("Arial", 18, bold=True)
        if Element.STAR_FONT is None:
            Element.STAR_FONT = pygame.font.SysFont("applesymbols,segoeui symbol,symbol", 11)
        self.tier = ELEMENT_TIERS.get(name, 0)
        self.stars = "\u2605" * self.tier
        tw, th = Element.FONT.size(name)
        sw, sh = Element.STAR_FONT.size(self.stars) if self.stars else (0, 0)
        self.w = max(tw, sw) + 24
        if self.stars:
            self.h = th + sh + 6  # 3px top + 3px bottom, no gap between
        else:
            self.h = self.HEIGHT
        self.x = x
        self.y = y
        self.vx = 0.0
        self.vy = 0.0
        self.cat = ELEMENT_CATEGORIES.get(name, "arcane")
        self.dragging = False
        self.drag_ox = 0
        self.drag_oy = 0

    def get_color(self, dark_mode):
        palette = CATEGORY_COLORS_DARK if dark_mode else CATEGORY_COLORS_LIGHT
        return palette.get(self.cat, (140, 70, 180))

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    BOX_ALPHA = 180

    def draw(self, surface, theme, dark_mode):
        color = self.get_color(dark_mode)
        r = self.rect
        box = pygame.Surface((r.w, r.h), pygame.SRCALPHA)
        # shadow
        pygame.draw.rect(box, (*theme["shadow"], self.BOX_ALPHA // 2),
                         pygame.Rect(2, 2, r.w, r.h), border_radius=self.RADIUS)
        # body
        pygame.draw.rect(box, (*color, self.BOX_ALPHA),
                         pygame.Rect(0, 0, r.w, r.h), border_radius=self.RADIUS)
        # border
        lighter = tuple(min(c + 40, 255) for c in color)
        pygame.draw.rect(box, (*lighter, self.BOX_ALPHA),
                         pygame.Rect(0, 0, r.w, r.h), width=2, border_radius=self.RADIUS)
        surface.blit(box, (r.x, r.y))
        # name text
        txt = Element.FONT.render(self.name, True, theme["text"])
        ty = r.y + 3 if self.stars else r.y + (r.h - txt.get_height()) // 2
        surface.blit(txt, (r.x + (r.w - txt.get_width()) // 2, ty))
        # stars
        if self.stars:
            star_surf = Element.STAR_FONT.render(self.stars, True, theme["gold"])
            surface.blit(star_surf, (r.x + (r.w - star_surf.get_width()) // 2,
                                     ty + txt.get_height()))

    def update(self, dt):
        if self.dragging:
            return
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vx *= 0.92
        self.vy *= 0.92
        if abs(self.vx) < 0.5:
            self.vx = 0
        if abs(self.vy) < 0.5:
            self.vy = 0
        # clamp to canvas
        self.x = max(0, min(self.x, CANVAS_W - self.w))
        self.y = max(0, min(self.y, CANVAS_H - self.h))

    def overlap_pct(self, other):
        r1 = self.rect
        r2 = other.rect
        clip = r1.clip(r2)
        if clip.w <= 0 or clip.h <= 0:
            return 0.0
        inter = clip.w * clip.h
        smaller = min(r1.w * r1.h, r2.w * r2.h)
        return inter / smaller if smaller > 0 else 0.0


# ── Game ───────────────────────────────────────────────────────────────
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Element Combo Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 18, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 14)
        self.input_font = pygame.font.SysFont("Arial", 20)

        self.dark_mode = True
        self.canvas_elements: list[Element] = []
        self.discovered: set[str] = set()
        self.dragged: Element | None = None

        # text input
        self.input_text = ""
        self.autocomplete_suggestion = ""

        # notification
        self.notification = ""
        self.notification_timer = 0.0

        # hint
        self.hint_text = ""
        self.hint_timer = 0.0
        self.hint_cooldown = 0.0

        # clear confirm
        self.clear_confirm = False
        self.clear_confirm_timer = 0.0

        # sidebar scroll
        self.sidebar_scroll = 0
        self.sidebar_max_scroll = 0

        # save manager
        self.current_save: str | None = None
        self.save_menu_open = False
        self.save_name_input = ""
        self.save_list_scroll = 0
        self.save_slots: list[dict] = []

        self.merge_sound = pygame.mixer.Sound(MERGE_SOUND_PATH)

        self._load_last_or_default()

    @property
    def t(self):
        return THEMES["dark" if self.dark_mode else "light"]

    def _save_path(self, name: str) -> str:
        return os.path.join(SAVES_DIR, f"{name}.json")

    def _list_saves(self) -> list[dict]:
        saves = []
        for f in sorted(os.listdir(SAVES_DIR)):
            if f.endswith(".json"):
                name = f[:-5]
                path = os.path.join(SAVES_DIR, f)
                try:
                    with open(path) as fh:
                        data = json.load(fh)
                    if isinstance(data, list):
                        count = len(data)
                    else:
                        count = len(data.get("discovered", []))
                except Exception:
                    count = 0
                saves.append({"name": name, "count": count})
        return saves

    def save(self):
        if not self.current_save:
            return
        data = {
            "discovered": list(self.discovered),
            "hint_cooldown": max(0, self.hint_cooldown),
        }
        with open(self._save_path(self.current_save), "w") as f:
            json.dump(data, f)

    def save_as(self, name: str):
        self.current_save = name
        self.save()

    def load_save(self, name: str):
        path = self._save_path(name)
        if os.path.exists(path):
            try:
                with open(path) as f:
                    raw = json.load(f)
                if isinstance(raw, list):
                    self.discovered = set(raw)
                    self.hint_cooldown = 0.0
                else:
                    self.discovered = set(raw.get("discovered", []))
                    self.hint_cooldown = raw.get("hint_cooldown", 0.0)
            except (json.JSONDecodeError, TypeError):
                self.discovered = set(BASE_ELEMENTS)
                self.hint_cooldown = 0.0
        else:
            self.discovered = set(BASE_ELEMENTS)
            self.hint_cooldown = 0.0
        self.current_save = name
        self.canvas_elements.clear()
        for i, n in enumerate(sorted(BASE_ELEMENTS)):
            self.canvas_elements.append(Element(n, 100 + i * 180, 250))

    def delete_save(self, name: str):
        path = self._save_path(name)
        if os.path.exists(path):
            os.remove(path)
        if self.current_save == name:
            self.current_save = None
            self.discovered = set(BASE_ELEMENTS)
            self.canvas_elements.clear()
            for i, n in enumerate(sorted(BASE_ELEMENTS)):
                self.canvas_elements.append(Element(n, 100 + i * 180, 250))

    def _load_last_or_default(self):
        if os.path.exists(self._save_path("default")):
            self.load_save("default")
        else:
            self.discovered = set(BASE_ELEMENTS)
            self.current_save = "default"
            for i, name in enumerate(sorted(BASE_ELEMENTS)):
                self.canvas_elements.append(Element(name, 100 + i * 180, 250))

    def spawn_element(self, name: str, x=None, y=None):
        if x is None:
            x = random.randint(40, CANVAS_W - 140)
        if y is None:
            y = random.randint(40, CANVAS_H - 60)
        self.canvas_elements.append(Element(name, x, y))

    def try_combine(self, a: Element, b: Element):
        key = frozenset([a.name, b.name])
        result = RECIPES.get(key)
        if result and result in ELEMENT_CATEGORIES:
            mx = (a.x + b.x) / 2
            my = (a.y + b.y) / 2
            self.canvas_elements.remove(a)
            self.canvas_elements.remove(b)
            new_el = Element(result, mx, my)
            self.canvas_elements.append(new_el)
            if result not in self.discovered:
                self.discovered.add(result)
                self.notification = f"Discovered: {result}!"
                self.notification_timer = 2.0
                self.merge_sound.play()  # Play merge sound effect
        else:
            dx = b.x - a.x
            dy = b.y - a.y
            dist = math.sqrt(dx * dx + dy * dy) or 1
            force = 300
            a.vx = -dx / dist * force
            a.vy = -dy / dist * force
            b.vx = dx / dist * force
            b.vy = dy / dist * force

    def get_hint(self):
        names = [el.name for el in self.canvas_elements]
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                if names[i] not in self.discovered or names[j] not in self.discovered:
                    continue
                key = frozenset([names[i], names[j]])
                result = RECIPES.get(key)
                if result and result not in self.discovered:
                    return f"You could make {result} using {random.choice([names[i], names[j]])}!"
        for name in set(names):
            if names.count(name) >= 2 and name in self.discovered:
                key = frozenset([name])
                result = RECIPES.get(key)
                if result and result not in self.discovered:
                    return f"You could make {result} using {name}!"
        for key, result in RECIPES.items():
            if result not in self.discovered and all(n in self.discovered for n in key):
                return f"You could make {result} using {random.choice(sorted(key))}!"
        return "No hints available — you've found everything reachable!"

    def get_autocomplete(self):
        if not self.input_text:
            return ""
        low = self.input_text.lower()
        for name in sorted(self.discovered):
            if name.lower().startswith(low) and name.lower() != low:
                return name
        return ""

    # ── Drawing ────────────────────────────────────────────────────────
    def draw_canvas_bg(self):
        t = self.t
        self.screen.fill(t["bg"], (0, 0, CANVAS_W, CANVAS_H))
        for gx in range(0, CANVAS_W, 30):
            for gy in range(0, CANVAS_H, 30):
                self.screen.set_at((gx, gy), t["grid_dot"])

    def draw_sidebar(self):
        t = self.t
        palette = CATEGORY_COLORS_DARK if self.dark_mode else CATEGORY_COLORS_LIGHT
        sidebar_rect = pygame.Rect(CANVAS_W, 0, SIDEBAR_W, CANVAS_H)
        self.screen.fill(t["sidebar_bg"], sidebar_rect)
        pygame.draw.line(self.screen, t["text_dim"], (CANVAS_W, 0), (CANVAS_W, CANVAS_H))

        total = len(ELEMENT_CATEGORIES)
        header_h = 44

        # draw chips first (behind header)
        sorted_disc = sorted(self.discovered)
        col_w = 140
        chip_h = 28
        pad = 5
        start_y = header_h + 4
        self.sidebar_chips = []

        for i, name in enumerate(sorted_disc):
            col = i % 2
            row = i // 2
            cx = CANVAS_W + 8 + col * col_w
            cy = start_y + row * (chip_h + pad) - self.sidebar_scroll

            if cy + chip_h < header_h or cy > CANVAS_H:
                self.sidebar_chips.append((name, pygame.Rect(cx, cy, col_w - 6, chip_h)))
                continue

            cat = ELEMENT_CATEGORIES.get(name, "arcane")
            color = palette.get(cat, (140, 70, 180))
            chip_rect = pygame.Rect(cx, cy, col_w - 6, chip_h)
            pygame.draw.rect(self.screen, color, chip_rect, border_radius=6)
            txt = self.small_font.render(name, True, t["text"])
            self.screen.blit(txt, (cx + 6, cy + (chip_h - txt.get_height()) // 2))
            self.sidebar_chips.append((name, chip_rect))

        # draw header on top with solid bg
        header_rect = pygame.Rect(CANVAS_W, 0, SIDEBAR_W, header_h)
        self.screen.fill(t["sidebar_bg"], header_rect)
        pygame.draw.line(self.screen, t["text_dim"], (CANVAS_W, 0), (CANVAS_W, header_h))
        header = self.font.render(f"Discovered ({len(self.discovered)}/{total})", True, t["gold"])
        self.screen.blit(header, (CANVAS_W + 15, 12))

        # max scroll
        total_rows = (len(sorted_disc) + 1) // 2
        content_h = total_rows * (chip_h + pad) + start_y
        self.sidebar_max_scroll = max(0, content_h - CANVAS_H + 10)

    def draw_input_bar(self):
        t = self.t
        bar_rect = pygame.Rect(0, CANVAS_H, WIDTH, INPUT_H)
        self.screen.fill(t["input_bg"], bar_rect)
        pygame.draw.line(self.screen, t["text_dim"], (0, CANVAS_H), (WIDTH, CANVAS_H))

        prompt = "> "
        prompt_surf = self.input_font.render(prompt, True, t["text_secondary"])
        self.screen.blit(prompt_surf, (10, CANVAS_H + 13))

        if self.autocomplete_suggestion:
            ghost = self.input_font.render(self.autocomplete_suggestion, True, t["text_dim"])
            self.screen.blit(ghost, (10 + prompt_surf.get_width(), CANVAS_H + 13))

        text_surf = self.input_font.render(self.input_text, True, t["text"])
        self.screen.blit(text_surf, (10 + prompt_surf.get_width(), CANVAS_H + 13))

        if pygame.time.get_ticks() % 1000 < 500:
            cx = 10 + prompt_surf.get_width() + text_surf.get_width() + 2
            pygame.draw.line(self.screen, t["text"], (cx, CANVAS_H + 12), (cx, CANVAS_H + 38))

        hint = self.small_font.render("Enter=spawn  Tab=complete", True, t["text_dim"])
        self.screen.blit(hint, (WIDTH - hint.get_width() - 10, CANVAS_H + 16))

    def _draw_button(self, rect, label, color=None):
        t = self.t
        if color is None:
            color = t["gold"]
        pygame.draw.rect(self.screen, t["btn_bg"], rect, border_radius=6)
        pygame.draw.rect(self.screen, t["btn_border"], rect, width=1, border_radius=6)
        txt = self.small_font.render(label, True, color)
        self.screen.blit(txt, (rect.x + (rect.w - txt.get_width()) // 2,
                                rect.y + (rect.h - txt.get_height()) // 2))

    def draw_top_buttons(self):
        t = self.t
        self.hint_btn = pygame.Rect(CANVAS_W - 80, 8, 70, 28)
        if self.hint_cooldown > 0:
            self._draw_button(self.hint_btn, f"{int(self.hint_cooldown)}s", t["text_dim"])
        else:
            self._draw_button(self.hint_btn, "Hint")
        self.saves_btn = pygame.Rect(CANVAS_W - 160, 8, 70, 28)
        self._draw_button(self.saves_btn, "Saves", t["text"])
        self.clear_btn = pygame.Rect(CANVAS_W - 240, 8, 70, 28)
        if self.clear_confirm:
            self._draw_button(self.clear_btn, "Sure?", (255, 80, 80))
        else:
            self._draw_button(self.clear_btn, "Clear", (200, 100, 100))
        self.sweep_btn = pygame.Rect(CANVAS_W - 320, 8, 70, 28)
        self._draw_button(self.sweep_btn, "Sweep", (180, 180, 100))
        self.theme_btn = pygame.Rect(CANVAS_W - 400, 8, 70, 28)
        self._draw_button(self.theme_btn, "Light" if self.dark_mode else "Dark", t["text_secondary"])

    def draw_save_menu(self):
        if not self.save_menu_open:
            return
        t = self.t
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill(t["overlay"])
        self.screen.blit(overlay, (0, 0))

        pw, ph = 500, 420
        px = (CANVAS_W - pw) // 2
        py = (CANVAS_H - ph) // 2
        panel = pygame.Rect(px, py, pw, ph)
        pygame.draw.rect(self.screen, t["panel"], panel, border_radius=10)
        pygame.draw.rect(self.screen, t["panel_border"], panel, width=2, border_radius=10)

        title = self.font.render("Save Files", True, t["text"])
        self.screen.blit(title, (px + 15, py + 12))

        cur = self.small_font.render(f"Current: {self.current_save or 'none'}", True, t["text_secondary"])
        self.screen.blit(cur, (px + 15, py + 38))

        self.save_close_btn = pygame.Rect(px + pw - 35, py + 8, 25, 25)
        pygame.draw.rect(self.screen, t["close_btn"], self.save_close_btn, border_radius=4)
        xtxt = self.small_font.render("X", True, t["text"])
        self.screen.blit(xtxt, (self.save_close_btn.x + 7, self.save_close_btn.y + 4))

        input_rect = pygame.Rect(px + 15, py + 60, pw - 120, 30)
        pygame.draw.rect(self.screen, t["input_field"], input_rect, border_radius=4)
        pygame.draw.rect(self.screen, t["panel_border"], input_rect, width=1, border_radius=4)
        inp_txt = self.input_font.render(self.save_name_input or "", True, t["text"])
        self.screen.blit(inp_txt, (input_rect.x + 8, input_rect.y + 4))
        if not self.save_name_input:
            ph_txt = self.small_font.render("Enter save name...", True, t["text_dim"])
            self.screen.blit(ph_txt, (input_rect.x + 8, input_rect.y + 8))
        if pygame.time.get_ticks() % 1000 < 500:
            cx = input_rect.x + 8 + inp_txt.get_width() + 2
            pygame.draw.line(self.screen, t["text"], (cx, input_rect.y + 5), (cx, input_rect.y + 25))

        self.save_new_btn = pygame.Rect(px + pw - 95, py + 60, 80, 30)
        self._draw_button(self.save_new_btn, "Save As")

        self.save_slots = self._list_saves()
        list_y = py + 105
        row_h = 36
        self.save_slot_btns = []

        for i, slot in enumerate(self.save_slots):
            ry = list_y + i * row_h
            if ry + row_h > py + ph - 10:
                break
            is_current = slot["name"] == self.current_save
            row_color = t["row_active"] if is_current else t["row_bg"]
            row_rect = pygame.Rect(px + 15, ry, pw - 30, row_h - 4)
            pygame.draw.rect(self.screen, row_color, row_rect, border_radius=4)

            name_txt = self.font.render(slot["name"], True, t["text"])
            self.screen.blit(name_txt, (px + 25, ry + 6))
            count_txt = self.small_font.render(f"{slot['count']} found", True, t["text_secondary"])
            self.screen.blit(count_txt, (px + 220, ry + 9))

            save_btn = pygame.Rect(px + pw - 220, ry + 4, 55, 24)
            self._draw_button(save_btn, "Save", t["gold"])
            load_btn = pygame.Rect(px + pw - 155, ry + 4, 55, 24)
            self._draw_button(load_btn, "Load", (130, 200, 130))
            del_btn = pygame.Rect(px + pw - 90, ry + 4, 55, 24)
            self._draw_button(del_btn, "Del", (200, 100, 100))

            self.save_slot_btns.append((slot["name"], save_btn, load_btn, del_btn))

    def draw_notification(self):
        t = self.t
        y = 20
        if self.notification_timer > 0:
            alpha = min(1.0, self.notification_timer / 0.5) * 255
            surf = self.font.render(self.notification, True, t["gold"])
            surf.set_alpha(int(alpha))
            x = (CANVAS_W - surf.get_width()) // 2
            self.screen.blit(surf, (x, y))
            y += 30
        if self.hint_timer > 0:
            alpha = min(1.0, self.hint_timer / 0.5) * 255
            surf = self.font.render(self.hint_text, True, t["hint_text"])
            surf.set_alpha(int(alpha))
            x = (CANVAS_W - surf.get_width()) // 2
            self.screen.blit(surf, (x, y))

    def draw(self):
        t = self.t
        self.draw_canvas_bg()
        for el in self.canvas_elements:
            el.draw(self.screen, t, self.dark_mode)
        self.draw_top_buttons()
        self.draw_sidebar()
        self.draw_input_bar()
        self.draw_notification()
        self.draw_save_menu()
        pygame.display.flip()

    # ── Main loop ──────────────────────────────────────────────────────
    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000.0
            if self.notification_timer > 0:
                self.notification_timer -= dt
            if self.hint_timer > 0:
                self.hint_timer -= dt
            if self.hint_cooldown > 0:
                self.hint_cooldown -= dt

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # ── Save menu events (intercept when open) ────────
                elif self.save_menu_open:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        mx, my = event.pos
                        if hasattr(self, 'save_close_btn') and self.save_close_btn.collidepoint(mx, my):
                            self.save_menu_open = False
                        elif hasattr(self, 'save_new_btn') and self.save_new_btn.collidepoint(mx, my):
                            name = self.save_name_input.strip()
                            if name:
                                self.save_as(name)
                                self.save_name_input = ""
                                self.notification = f"Saved as '{name}'"
                                self.notification_timer = 2.0
                        else:
                            for sname, save_btn, load_btn, del_btn in getattr(self, 'save_slot_btns', []):
                                if save_btn.collidepoint(mx, my):
                                    self.save_as(sname)
                                    self.notification = f"Saved to '{sname}'"
                                    self.notification_timer = 2.0
                                    break
                                if load_btn.collidepoint(mx, my):
                                    self.load_save(sname)
                                    self.save_menu_open = False
                                    self.notification = f"Loaded '{sname}'"
                                    self.notification_timer = 2.0
                                    break
                                if del_btn.collidepoint(mx, my):
                                    self.delete_save(sname)
                                    self.notification = f"Deleted '{sname}'"
                                    self.notification_timer = 2.0
                                    break
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.save_menu_open = False
                        elif event.key == pygame.K_RETURN:
                            name = self.save_name_input.strip()
                            if name:
                                self.save_as(name)
                                self.save_name_input = ""
                                self.notification = f"Saved as '{name}'"
                                self.notification_timer = 2.0
                        elif event.key == pygame.K_BACKSPACE:
                            self.save_name_input = self.save_name_input[:-1]
                        elif event.unicode and event.unicode.isprintable():
                            self.save_name_input += event.unicode

                # ── Normal game events ────────────────────────────
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos
                    # right-click delete
                    if event.button == 3:
                        for el in reversed(self.canvas_elements):
                            if el.rect.collidepoint(mx, my):
                                self.canvas_elements.remove(el)
                                break
                        continue

                    if event.button == 1:
                        # hint button
                        if hasattr(self, 'hint_btn') and self.hint_btn.collidepoint(mx, my):
                            if self.hint_cooldown > 0:
                                self.hint_text = f"Hint cooldown: {int(self.hint_cooldown)}s"
                                self.hint_timer = 2.0
                            else:
                                self.hint_text = self.get_hint()
                                self.hint_timer = 4.0
                                self.hint_cooldown = 60.0
                            continue

                        # saves button
                        if hasattr(self, 'saves_btn') and self.saves_btn.collidepoint(mx, my):
                            self.save_menu_open = True
                            self.save_name_input = ""
                            continue

                        # clear button (two-click confirm)
                        if hasattr(self, 'clear_btn') and self.clear_btn.collidepoint(mx, my):
                            if self.clear_confirm:
                                self.discovered = set(BASE_ELEMENTS)
                                self.canvas_elements.clear()
                                for i, n in enumerate(sorted(BASE_ELEMENTS)):
                                    self.canvas_elements.append(Element(n, 100 + i * 180, 250))
                                self.notification = "Reset to base elements"
                                self.notification_timer = 2.0
                                self.clear_confirm = False
                                self.clear_confirm_timer = 0.0
                            else:
                                self.clear_confirm = True
                                self.clear_confirm_timer = 3.0
                            continue

                        # sweep button (clear board, keep inventory)
                        if hasattr(self, 'sweep_btn') and self.sweep_btn.collidepoint(mx, my):
                            self.canvas_elements.clear()
                            self.notification = "Board swept"
                            self.notification_timer = 2.0
                            continue

                        # theme toggle
                        if hasattr(self, 'theme_btn') and self.theme_btn.collidepoint(mx, my):
                            self.dark_mode = not self.dark_mode
                            continue

                        # sidebar click
                        if mx >= CANVAS_W and my < CANVAS_H:
                            for name, chip_rect in self.sidebar_chips:
                                if chip_rect.collidepoint(mx, my):
                                    self.spawn_element(name)
                                    break
                            continue

                        # canvas drag
                        if mx < CANVAS_W and my < CANVAS_H:
                            for el in reversed(self.canvas_elements):
                                if el.rect.collidepoint(mx, my):
                                    el.dragging = True
                                    el.drag_ox = mx - el.x
                                    el.drag_oy = my - el.y
                                    el.vx = 0
                                    el.vy = 0
                                    self.dragged = el
                                    self.canvas_elements.remove(el)
                                    self.canvas_elements.append(el)
                                    break

                    # sidebar scroll
                    if event.button == 4:
                        if mx >= CANVAS_W:
                            self.sidebar_scroll = max(0, self.sidebar_scroll - 30)
                    elif event.button == 5:
                        if mx >= CANVAS_W:
                            self.sidebar_scroll = min(self.sidebar_max_scroll, self.sidebar_scroll + 30)

                elif event.type == pygame.MOUSEWHEEL:
                    mx, _ = pygame.mouse.get_pos()
                    if mx >= CANVAS_W:
                        self.sidebar_scroll -= event.y * 30
                        self.sidebar_scroll = max(0, min(self.sidebar_scroll, self.sidebar_max_scroll))

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1 and self.dragged:
                        self.dragged.dragging = False
                        for other in self.canvas_elements:
                            if other is self.dragged:
                                continue
                            if self.dragged.overlap_pct(other) >= OVERLAP_THRESHOLD:
                                self.try_combine(self.dragged, other)
                                break
                        self.dragged = None

                elif event.type == pygame.MOUSEMOTION:
                    if self.dragged and self.dragged.dragging:
                        mx, my = event.pos
                        self.dragged.x = mx - self.dragged.drag_ox
                        self.dragged.y = my - self.dragged.drag_oy
                        self.dragged.x = max(0, min(self.dragged.x, CANVAS_W - self.dragged.w))
                        self.dragged.y = max(0, min(self.dragged.y, CANVAS_H - self.dragged.h))

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        name = self.input_text.strip().lower()
                        if name in self.discovered:
                            self.spawn_element(name)
                        self.input_text = ""
                        self.autocomplete_suggestion = ""
                    elif event.key == pygame.K_TAB:
                        if self.autocomplete_suggestion:
                            self.input_text = self.autocomplete_suggestion
                            self.autocomplete_suggestion = ""
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                        self.autocomplete_suggestion = self.get_autocomplete()
                    elif event.key == pygame.K_ESCAPE:
                        self.input_text = ""
                        self.autocomplete_suggestion = ""
                    elif event.unicode and event.unicode.isprintable():
                        self.input_text += event.unicode
                        self.autocomplete_suggestion = self.get_autocomplete()

            for el in self.canvas_elements:
                el.update(dt)

            self.draw()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    Game().run()
