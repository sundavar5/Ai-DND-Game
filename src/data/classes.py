CLASSES = {
    "Fighter": {
        "hit_die": 10,
        "primary_ability": "Strength or Dexterity",
        "saves": ["str", "con"],
        "proficiencies": ["All armor", "Shields", "Simple weapons", "Martial weapons"],
        "features": {
            1: ["Fighting Style", "Second Wind"],
            2: ["Action Surge"],
            3: ["Martial Archetype"],
            4: ["Ability Score Improvement"],
            5: ["Extra Attack"]
        }
    },
    "Wizard": {
        "hit_die": 6,
        "primary_ability": "Intelligence",
        "saves": ["int", "wis"],
        "proficiencies": ["Daggers", "Darts", "Slings", "Quarterstaffs", "Light crossbows"],
        "features": {
            1: ["Spellcasting", "Arcane Recovery"],
            2: ["Arcane Tradition"],
            3: [],
            4: ["Ability Score Improvement"],
            5: []
        }
    },
    "Rogue": {
        "hit_die": 8,
        "primary_ability": "Dexterity",
        "saves": ["dex", "int"],
        "proficiencies": ["Light armor", "Simple weapons", "Hand crossbows", "Longswords", "Rapiers", "Shortswords"],
        "features": {
            1: ["Expertise", "Sneak Attack", "Thieves' Cant"],
            2: ["Cunning Action"],
            3: ["Roguish Archetype"],
            4: ["Ability Score Improvement"],
            5: ["Uncanny Dodge"]
        }
    },
    "Cleric": {
        "hit_die": 8,
        "primary_ability": "Wisdom",
        "saves": ["wis", "cha"],
        "proficiencies": ["Light armor", "Medium armor", "Shields", "Simple weapons"],
        "features": {
            1: ["Spellcasting", "Divine Domain"],
            2: ["Channel Divinity", "Divine Domain Feature"],
            3: [],
            4: ["Ability Score Improvement"],
            5: ["Destroy Undead (CR 1/2)"]
        }
    }
}
