# Comprehensive List of SRD Spells
SPELLS = {
    "acid_splash": {
        "level": 0,
        "school": "Conjuration",
        "casting_time": "1 action",
        "range": "60 feet",
        "components": "V, S",
        "duration": "Instantaneous",
        "description": "You hurl a bubble of acid. Choose one creature within range, or two creatures within range that are within 5 feet of each other. A target must succeed on a Dexterity saving throw or take 1d6 acid damage."
    },
    "mage_hand": {
        "level": 0,
        "school": "Conjuration",
        "casting_time": "1 action",
        "range": "30 feet",
        "components": "V, S",
        "duration": "1 minute",
        "description": "A spectral, floating hand appears at a point you choose within range. The hand lasts for the duration or until you dismiss it as an action. The hand can manipulate objects, open an unlocked door or container, stow or retrieve an item from an open container, or pour the contents out of a vial."
    },
    "magic_missile": {
        "level": 1,
        "school": "Evocation",
        "casting_time": "1 action",
        "range": "120 feet",
        "components": "V, S",
        "duration": "Instantaneous",
        "description": "You create three glowing darts of magical force. Each dart hits a creature of your choice that you can see within range. A dart deals 1d4 + 1 force damage to its target. The darts all strike simultaneously, and you can direct them to hit one creature or several."
    },
    "cure_wounds": {
        "level": 1,
        "school": "Evocation",
        "casting_time": "1 action",
        "range": "Touch",
        "components": "V, S",
        "duration": "Instantaneous",
        "description": "A creature you touch regains a number of hit points equal to 1d8 + your spellcasting ability modifier. This spell has no effect on undead or constructs."
    },
    "fireball": {
        "level": 3,
        "school": "Evocation",
        "casting_time": "1 action",
        "range": "150 feet",
        "components": "V, S, M",
        "duration": "Instantaneous",
        "description": "A bright streak flashes from your pointing finger to a point you choose within range and then blossoms with a low roar into an explosion of flame. Each creature in a 20-foot-radius sphere centered on that point must make a Dexterity saving throw. A target takes 8d6 fire damage on a failed save, or half as much damage on a successful one."
    },
    "shield": {
        "level": 1,
        "school": "Abjuration",
        "casting_time": "1 reaction",
        "range": "Self",
        "components": "V, S",
        "duration": "1 round",
        "description": "An invisible barrier of magical force appears and protects you. Until the start of your next turn, you have a +5 bonus to AC, including against the triggering attack, and you take no damage from magic missile."
    },
    # Add more to fill space if needed, keeping it representative for now.
    "detect_magic": {
        "level": 1,
        "school": "Divination",
        "casting_time": "1 action",
        "range": "Self",
        "components": "V, S",
        "duration": "Concentration, up to 10 minutes",
        "description": "For the duration, you sense the presence of magic within 30 feet of you. If you sense magic in this way, you can use your action to see a faint aura around any visible creature or object in the area that bears magic, and you learn its school of magic, if any."
    },
    "identify": {
        "level": 1,
        "school": "Divination",
        "casting_time": "1 minute",
        "range": "Touch",
        "components": "V, S, M",
        "duration": "Instantaneous",
        "description": "You choose one object that you must touch throughout the casting of the spell. If it is a magic item or some other magic-imbued object, you learn its properties and how to use them, whether it requires attunement to use, and how many charges it has, if any."
    },
    "bless": {
        "level": 1,
        "school": "Enchantment",
        "casting_time": "1 action",
        "range": "30 feet",
        "components": "V, S, M",
        "duration": "Concentration, up to 1 minute",
        "description": "You bless up to three creatures of your choice within range. Whenever a target makes an attack roll or a saving throw before the spell ends, the target can roll a d4 and add the number rolled to the attack roll or saving throw."
    },
     "healing_word": {
        "level": 1,
        "school": "Evocation",
        "casting_time": "1 bonus action",
        "range": "60 feet",
        "components": "V",
        "duration": "Instantaneous",
        "description": "A creature of your choice that you can see within range regains hit points equal to 1d4 + your spellcasting ability modifier. This spell has no effect on undead or constructs."
    }
}
