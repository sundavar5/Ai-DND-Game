ITEMS = {
    "weapons": {
        "dagger": {"damage": "1d4", "type": "piercing", "properties": ["finesse", "light", "thrown"], "cost": 2},
        "shortsword": {"damage": "1d6", "type": "piercing", "properties": ["finesse", "light"], "cost": 10},
        "longsword": {"damage": "1d8", "type": "slashing", "properties": ["versatile (1d10)"], "cost": 15},
        "greatsword": {"damage": "2d6", "type": "slashing", "properties": ["heavy", "two-handed"], "cost": 50},
        "shortbow": {"damage": "1d6", "type": "piercing", "properties": ["ammunition", "two-handed"], "range": "80/320", "cost": 25},
        "longbow": {"damage": "1d8", "type": "piercing", "properties": ["ammunition", "heavy", "two-handed"], "range": "150/600", "cost": 50},
        "mace": {"damage": "1d6", "type": "bludgeoning", "properties": [], "cost": 5},
        "staff": {"damage": "1d6", "type": "bludgeoning", "properties": ["versatile (1d8)"], "cost": 0.2},
    },
    "armor": {
        "padded": {"ac": 11, "type": "light", "stealth_disadvantage": True, "cost": 5},
        "leather": {"ac": 11, "type": "light", "stealth_disadvantage": False, "cost": 10},
        "studded_leather": {"ac": 12, "type": "light", "stealth_disadvantage": False, "cost": 45},
        "hide": {"ac": 12, "type": "medium", "max_dex": 2, "stealth_disadvantage": False, "cost": 10},
        "chain_shirt": {"ac": 13, "type": "medium", "max_dex": 2, "stealth_disadvantage": False, "cost": 50},
        "scale_mail": {"ac": 14, "type": "medium", "max_dex": 2, "stealth_disadvantage": True, "cost": 50},
        "breastplate": {"ac": 14, "type": "medium", "max_dex": 2, "stealth_disadvantage": False, "cost": 400},
        "half_plate": {"ac": 15, "type": "medium", "max_dex": 2, "stealth_disadvantage": True, "cost": 750},
        "ring_mail": {"ac": 14, "type": "heavy", "stealth_disadvantage": True, "cost": 30},
        "chain_mail": {"ac": 16, "type": "heavy", "stealth_disadvantage": True, "req_str": 13, "cost": 75},
        "splint": {"ac": 17, "type": "heavy", "stealth_disadvantage": True, "req_str": 15, "cost": 200},
        "plate": {"ac": 18, "type": "heavy", "stealth_disadvantage": True, "req_str": 15, "cost": 1500},
        "shield": {"ac_bonus": 2, "type": "shield", "cost": 10}
    },
    "gear": {
        "backpack": {"cost": 2},
        "bedroll": {"cost": 1},
        "rations": {"cost": 0.5, "unit": "day"},
        "rope_hempen": {"cost": 1, "unit": "50ft"},
        "torch": {"cost": 0.01},
        "healing_potion": {"cost": 50, "effect": "heal 2d4+2"},
    }
}
