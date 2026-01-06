MONSTERS = {
    "goblin": {
        "size": "Small",
        "type": "Humanoid",
        "alignment": "Neutral Evil",
        "ac": 15,
        "hp": 7,
        "speed": "30 ft.",
        "stats": {"str": 8, "dex": 14, "con": 10, "int": 10, "wis": 8, "cha": 8},
        "cr": "1/4",
        "actions": [
            {"name": "Scimitar", "type": "melee", "attack_bonus": 4, "damage": "1d6+2", "damage_type": "slashing"},
            {"name": "Shortbow", "type": "ranged", "attack_bonus": 4, "damage": "1d6+2", "damage_type": "piercing"}
        ]
    },
    "skeleton": {
        "size": "Medium",
        "type": "Undead",
        "alignment": "Lawful Evil",
        "ac": 13,
        "hp": 13,
        "speed": "30 ft.",
        "stats": {"str": 10, "dex": 14, "con": 15, "int": 6, "wis": 8, "cha": 5},
        "vulnerabilities": ["bludgeoning"],
        "immunities": ["poison"],
        "cr": "1/4",
        "actions": [
            {"name": "Shortsword", "type": "melee", "attack_bonus": 4, "damage": "1d6+2", "damage_type": "piercing"},
            {"name": "Shortbow", "type": "ranged", "attack_bonus": 4, "damage": "1d6+2", "damage_type": "piercing"}
        ]
    },
    "orc": {
        "size": "Medium",
        "type": "Humanoid",
        "alignment": "Chaotic Evil",
        "ac": 13,
        "hp": 15,
        "speed": "30 ft.",
        "stats": {"str": 16, "dex": 12, "con": 16, "int": 7, "wis": 11, "cha": 10},
        "cr": "1/2",
        "actions": [
            {"name": "Greataxe", "type": "melee", "attack_bonus": 5, "damage": "1d12+3", "damage_type": "slashing"},
            {"name": "Javelin", "type": "ranged", "attack_bonus": 5, "damage": "1d6+3", "damage_type": "piercing"}
        ]
    },
    "giant_spider": {
        "size": "Large",
        "type": "Beast",
        "alignment": "Unaligned",
        "ac": 14,
        "hp": 26,
        "speed": "30 ft., climb 30 ft.",
        "stats": {"str": 14, "dex": 16, "con": 12, "int": 2, "wis": 11, "cha": 4},
        "cr": "1",
        "actions": [
            {"name": "Bite", "type": "melee", "attack_bonus": 5, "damage": "1d8+3", "damage_type": "piercing", "effect": "poison DC 11 2d8"}
        ]
    },
    "dragon_red_young": {
        "size": "Large",
        "type": "Dragon",
        "alignment": "Chaotic Evil",
        "ac": 18,
        "hp": 178,
        "speed": "40 ft., fly 80 ft.",
        "stats": {"str": 23, "dex": 10, "con": 21, "int": 14, "wis": 11, "cha": 19},
        "cr": "10",
        "actions": [
            {"name": "Bite", "type": "melee", "attack_bonus": 10, "damage": "2d10+6", "damage_type": "piercing"},
            {"name": "Fire Breath", "type": "area", "save": "dex", "dc": 17, "damage": "16d6", "damage_type": "fire"}
        ]
    }
}
