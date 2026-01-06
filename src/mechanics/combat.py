from src.mechanics.dice import Dice
from src.data.monsters import MONSTERS

class Combat:
    def __init__(self, character, monster_name):
        self.character = character
        self.monster_data = MONSTERS.get(monster_name)
        if not self.monster_data:
            raise ValueError(f"Monster {monster_name} not found.")

        self.monster_hp = self.monster_data["hp"]
        self.monster_name = monster_name.capitalize()
        self.is_active = True
        self.log = []

    def start_combat(self):
        # Roll initiative
        player_init = Dice.roll("1d20")[0] + self.character._get_modifier(self.character.stats["dex"])
        monster_init = Dice.roll("1d20")[0] + self.monster_data["stats"]["dex"] // 2 - 5

        self.log.append(f"Initiative: {self.character.name} ({player_init}) vs {self.monster_name} ({monster_init})")
        return player_init >= monster_init

    def player_attack(self, weapon_damage="1d8", attack_bonus=2):
        # Basic attack logic
        roll, details = Dice.roll("1d20")
        total_hit = roll + attack_bonus

        ac = self.monster_data["ac"]
        if total_hit >= ac:
            dmg, dmg_details = Dice.roll(weapon_damage)
            self.monster_hp -= dmg
            self.log.append(f"You hit {self.monster_name} for {dmg} damage! ({dmg_details})")
            if self.monster_hp <= 0:
                self.is_active = False
                self.log.append(f"{self.monster_name} is defeated!")
                return True, f"Hit! {dmg} damage. Target defeated."
            return True, f"Hit! {dmg} damage."
        else:
            self.log.append(f"You missed {self.monster_name}.")
            return False, "Miss."

    def monster_turn(self):
        if not self.is_active:
            return "Combat is over."

        # Pick random action
        action = self.monster_data["actions"][0]
        # Basic attack
        if "attack_bonus" in action:
            roll, _ = Dice.roll("1d20")
            total = roll + action["attack_bonus"]
            ac = 10 + self.character._get_modifier(self.character.stats["dex"]) # Simple AC calc

            if total >= ac:
                dmg, _ = Dice.roll(action["damage"])
                self.character.take_damage(dmg)
                self.log.append(f"{self.monster_name} attacks with {action['name']} and hits for {dmg} damage!")
                return f"{self.monster_name} hits you for {dmg} damage."
            else:
                self.log.append(f"{self.monster_name} attacks with {action['name']} and misses.")
                return f"{self.monster_name} misses you."
        return f"{self.monster_name} does something..."
