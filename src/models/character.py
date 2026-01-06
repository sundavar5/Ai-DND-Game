import json
import random
from src.data.races import RACES
from src.data.classes import CLASSES
from src.utils.constants import XP_TABLE, PROFICIENCY_BONUS, SKILLS
from src.mechanics.dice import Dice

class Character:
    def __init__(self, name, race, char_class, stats=None, inventory=None, hp=None, level=1, xp=0):
        self.name = name
        self.race = race
        self.char_class = char_class
        self.level = level
        self.xp = xp

        # Initialize Stats
        if stats:
            self.stats = stats
        else:
            self.stats = self._roll_stats()
            # Apply race bonuses
            race_data = RACES.get(race, {})
            bonuses = race_data.get("ability_bonuses", {})
            for stat, bonus in bonuses.items():
                if stat in self.stats:
                    self.stats[stat] += bonus

        # Initialize HP
        self.max_hp = 0
        if hp:
            self.max_hp = hp
            self.current_hp = hp
        else:
            self.max_hp = self._calculate_max_hp()
            self.current_hp = self.max_hp

        if inventory:
            self.inventory = inventory
        else:
            self.inventory = []

        self.equipment = {"main_hand": None, "off_hand": None, "armor": None}
        self.spell_slots = {}
        self.proficiencies = []
        self._initialize_class_features()

    def _roll_stats(self):
        stats = {}
        for stat in ['str', 'dex', 'con', 'int', 'wis', 'cha']:
            rolls = [random.randint(1, 6) for _ in range(4)]
            rolls.remove(min(rolls))
            stats[stat] = sum(rolls)
        return stats

    def _get_modifier(self, score):
        return (score - 10) // 2

    def _calculate_max_hp(self):
        class_data = CLASSES.get(self.char_class, {})
        hit_die = class_data.get("hit_die", 8)
        con_mod = self._get_modifier(self.stats['con'])

        # Level 1 max HP
        hp = hit_die + con_mod

        # Higher levels (average)
        if self.level > 1:
            avg_roll = (hit_die // 2) + 1
            hp += (avg_roll + con_mod) * (self.level - 1)

        return max(hp, 1)

    def _initialize_class_features(self):
        class_data = CLASSES.get(self.char_class, {})
        self.proficiencies.extend(class_data.get("proficiencies", []))
        # Logic for spell slots etc. could go here

    def get_skill_modifier(self, skill_name):
        # Basic implementation
        ability = SKILLS.get(skill_name, "dex")
        mod = self._get_modifier(self.stats.get(ability, 10))
        # Check proficiency (not fully implemented in data yet, assuming generic list)
        if skill_name in self.proficiencies:
             mod += PROFICIENCY_BONUS.get(self.level, 2)
        return mod

    def take_damage(self, amount):
        self.current_hp -= amount
        if self.current_hp < 0:
            self.current_hp = 0
        return self.current_hp

    def heal(self, amount):
        self.current_hp += amount
        if self.current_hp > self.max_hp:
            self.current_hp = self.max_hp
        return self.current_hp

    def equip(self, item_name, slot="main_hand"):
        if item_name in self.inventory:
            self.equipment[slot] = item_name
            return True
        return False

    def to_dict(self):
        return {
            "name": self.name,
            "race": self.race,
            "char_class": self.char_class,
            "stats": self.stats,
            "inventory": self.inventory,
            "hp": self.max_hp, # persist max hp logic
            "current_hp": self.current_hp,
            "level": self.level,
            "xp": self.xp,
            "equipment": self.equipment
        }

    @classmethod
    def from_dict(cls, data):
        char = cls(
            name=data["name"],
            race=data["race"],
            char_class=data["char_class"],
            stats=data["stats"],
            inventory=data["inventory"],
            hp=data["hp"],
            level=data["level"],
            xp=data.get("xp", 0)
        )
        char.current_hp = data.get("current_hp", char.max_hp)
        char.equipment = data.get("equipment", char.equipment)
        return char

    @classmethod
    def create_character(cls):
        print("\n--- Character Creation ---")
        name = input("Enter character name: ")

        print("Available Races:", ", ".join(RACES.keys()))
        race = input("Enter character race: ")
        while race not in RACES:
             print("Invalid race.")
             race = input("Enter character race: ")

        print("Available Classes:", ", ".join(CLASSES.keys()))
        char_class = input("Enter character class: ")
        while char_class not in CLASSES:
            print("Invalid class.")
            char_class = input("Enter character class: ")

        print("Rolling stats (4d6 drop lowest)...")
        return cls(name, race, char_class)

    def __str__(self):
        stats_str = ", ".join([f"{k.upper()}: {v} ({self._get_modifier(v):+})" for k, v in self.stats.items()])
        eq_str = ", ".join([f"{k}: {v}" for k,v in self.equipment.items() if v])
        return (f"Name: {self.name} | {self.race} {self.char_class} {self.level}\n"
                f"HP: {self.current_hp}/{self.max_hp} | XP: {self.xp}\n"
                f"Stats: {stats_str}\n"
                f"Equipped: {eq_str if eq_str else 'None'}\n"
                f"Inventory: {', '.join(self.inventory) if self.inventory else 'Empty'}")
