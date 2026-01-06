import json
import os
from .character import Character
from .story_teller import StoryTeller

class Game:
    def __init__(self, api_key, base_url=None):
        self.api_key = api_key
        self.base_url = base_url
        self.character = None
        self.story_teller = None
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
                print("Commands: /quit, /save, /inventory, /sheet, /help")
                continue

            response = self.story_teller.next_turn(action)
            print(f"\nDM: {response}")
