import json
import os
from .models.character import Character
from .story_teller import StoryTeller
from .mechanics.combat import Combat
from .data.items import ITEMS

class Game:
    def __init__(self, api_key, base_url=None):
        self.api_key = api_key
        self.base_url = base_url
        self.character = None
        self.story_teller = None
        self.combat = None
        self.is_running = False

    def new_game(self):
        self.character = Character.create_character()
        print("\n--- Campaign Setup ---")
        setting = input("Describe the setting/genre (e.g., 'Dark Fantasy', 'Cyberpunk', 'High Magic'): ")

        self.story_teller = StoryTeller(self.api_key, self.base_url)
        print("\nGenerated Opening Scene...")
        opening = self.story_teller.start_campaign(self.character, setting)
        print(f"\nDM: {opening}")
        self.is_running = True

    def save_game(self, filename="savegame.json"):
        data = {
            "character": self.character.to_dict(),
            "history": self.story_teller.get_history()
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Game saved to {filename}")

    def load_game(self, filename="savegame.json"):
        if not os.path.exists(filename):
            print("Save file not found.")
            return False

        with open(filename, 'r') as f:
            data = json.load(f)

        self.character = Character.from_dict(data["character"])
        self.story_teller = StoryTeller(self.api_key, self.base_url)
        self.story_teller.history = data["history"]

        print("\nGame loaded.")
        print("Last interaction:")
        if self.story_teller.history:
             last_msg = self.story_teller.history[-1]
             print(f"{last_msg['role'].capitalize()}: {last_msg['content']}")

        self.is_running = True
        return True

    def run(self):
        while self.is_running:
            if self.combat and self.combat.is_active:
                self._handle_combat_loop()
                continue

            action = input("\n> ")

            if action.lower() == "/quit":
                confirm = input("Are you sure you want to quit? (y/n): ")
                if confirm.lower() == 'y':
                    self.is_running = False
                continue
            elif action.lower() == "/save":
                self.save_game()
                continue
            elif action.lower() == "/inventory":
                print(f"Inventory: {self.character.inventory}")
                continue
            elif action.lower() == "/sheet":
                print(self.character)
                continue
            elif action.lower() == "/help":
                print("Commands: /quit, /save, /inventory, /sheet, /help, /equip <item>, /fight <monster>")
                continue
            elif action.lower().startswith("/equip"):
                item_name = action[7:].strip()
                if self.character.equip(item_name):
                    print(f"Equipped {item_name}.")
                else:
                    print("Item not found in inventory.")
                continue
            elif action.lower().startswith("/fight"):
                monster_name = action[7:].strip()
                try:
                    self.combat = Combat(self.character, monster_name)
                    print(f"\n--- Combat Started: {self.character.name} vs {monster_name.capitalize()} ---")
                    is_player_turn = self.combat.start_combat()
                    if is_player_turn:
                        print("You won initiative!")
                    else:
                        print(f"{monster_name.capitalize()} won initiative!")
                        print(self.combat.monster_turn())
                except ValueError as e:
                    print(e)
                continue

            response = self.story_teller.next_turn(action)
            print(f"\nDM: {response}")

    def _handle_combat_loop(self):
        print(f"\nHP: {self.character.current_hp}/{self.character.max_hp}")
        action = input("(Combat) > ")

        if action.lower() == "attack":
            # Simplified attack
            hit, msg = self.combat.player_attack()
            print(msg)
            if self.combat.is_active:
                 print(self.combat.monster_turn())
            else:
                 print("Combat ended. You are victorious!")
                 self.combat = None
        elif action.lower() == "flee":
            print("You flee from combat!")
            self.combat = None
        else:
            print("Combat options: attack, flee")
