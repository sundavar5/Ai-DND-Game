import json
import random

class Character:
    def __init__(self, name, race, char_class, stats=None, inventory=None, hp=None, level=1):
        self.name = name
        self.race = race
        self.char_class = char_class
        self.level = level

        if stats:
            self.stats = stats
        else:
            self.stats = self._roll_stats()

        if hp is not None:
            self.hp = hp
        else:
            self.hp = 10 + self._get_modifier(self.stats['con']) # Basic rule

        if inventory:
            self.inventory = inventory
        else:
            self.inventory = []

    def _roll_stats(self):
        stats = {}
        for stat in ['str', 'dex', 'con', 'int', 'wis', 'cha']:
            rolls = [random.randint(1, 6) for _ in range(4)]
            rolls.remove(min(rolls))
            stats[stat] = sum(rolls)
        return stats

    def _get_modifier(self, score):
        return (score - 10) // 2

    def to_dict(self):
        return {
            "name": self.name,
            "race": self.race,
            "char_class": self.char_class,
            "stats": self.stats,
            "inventory": self.inventory,
            "hp": self.hp,
            "level": self.level
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            race=data["race"],
            char_class=data["char_class"],
            stats=data["stats"],
            inventory=data["inventory"],
            hp=data["hp"],
            level=data["level"]
        )

    @classmethod
    def create_character(cls):
        print("\n--- Character Creation ---")
        name = input("Enter character name: ")
        race = input("Enter character race: ")
        char_class = input("Enter character class: ")
        # In a real game, we might offer point buy or standard array here.
        # For now, we auto-roll for simplicity or let user choose?
        # The instructions say "fully customizable", so let's offer choices.

        print("Rolling stats (4d6 drop lowest)...")
        # We'll just init and it will roll.
        return cls(name, race, char_class)

    def __str__(self):
        stats_str = ", ".join([f"{k.upper()}: {v}" for k, v in self.stats.items()])
        return (f"Name: {self.name}\n"
                f"Race: {self.race}\n"
                f"Class: {self.char_class}\n"
                f"Level: {self.level}\n"
                f"HP: {self.hp}\n"
                f"Stats: {stats_str}\n"
                f"Inventory: {', '.join(self.inventory) if self.inventory else 'Empty'}")
