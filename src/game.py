import json
import os
from .models.character import Character
from .story_teller import StoryTeller
from .mechanics.combat import Combat
from .data.items import ITEMS

class Game:
    def __init__(self, api_key, base_url=None, model_name="gpt-3.5-turbo"):
        self.api_key = api_key
        self.base_url = base_url
        self.model_name = model_name
        self.character = None
        self.story_teller = None
        self.combat = None
        self.is_running = False

    def initialize_campaign(self, character, setting_description):
        self.character = character
        self.story_teller = StoryTeller(self.api_key, self.base_url, self.model_name)
        opening = self.story_teller.start_campaign(self.character, setting_description)
        self.is_running = True
        return f"Campaign Started!\n\nDM: {opening}"

    def load_game(self, filename="savegame.json"):
        if not os.path.exists(filename):
            return "Save file not found."

        with open(filename, 'r') as f:
            data = json.load(f)

        self.character = Character.from_dict(data["character"])
        self.story_teller = StoryTeller(self.api_key, self.base_url, self.model_name)
        self.story_teller.history = data["history"]
        self.is_running = True

        last_interaction = ""
        if self.story_teller.history:
            last_msg = self.story_teller.history[-1]
            last_interaction = f"{last_msg['role'].capitalize()}: {last_msg['content']}"

        return f"Game loaded.\n{last_interaction}"

    def save_game(self, filename="savegame.json"):
        if not self.character:
             return "No game active to save."
        data = {
            "character": self.character.to_dict(),
            "history": self.story_teller.get_history()
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        return f"Game saved to {filename}"

    def process_action(self, action):
        if not self.is_running:
            return "Game is not running."

        action = action.strip()
        if not action:
             return ""

        # Combat Handling
        if self.combat and self.combat.is_active:
            return self._handle_combat_turn(action)

        # Standard Command Handling
        if action.lower() == "/quit":
            self.is_running = False
            return "Game ended."
        elif action.lower() == "/save":
            return self.save_game()
        elif action.lower() == "/inventory":
            return f"Inventory: {', '.join(self.character.inventory) if self.character.inventory else 'Empty'}"
        elif action.lower() == "/sheet":
            return str(self.character)
        elif action.lower() == "/help":
            return "Commands: /quit, /save, /inventory, /sheet, /help, /equip <item>, /fight <monster>"
        elif action.lower().startswith("/equip "):
            item_name = action[7:].strip()
            if self.character.equip(item_name):
                return f"Equipped {item_name}."
            else:
                return "Item not found in inventory."
        elif action.lower().startswith("/fight "):
            monster_name = action[7:].strip()
            try:
                self.combat = Combat(self.character, monster_name)
                log = [f"\n--- Combat Started: {self.character.name} vs {monster_name.capitalize()} ---"]
                is_player_turn = self.combat.start_combat()
                log.append(self.combat.log[-1]) # Add initiative log

                if is_player_turn:
                    log.append("You won initiative! Your turn.")
                else:
                    log.append(f"{monster_name.capitalize()} won initiative!")
                    log.append(self.combat.monster_turn())

                return "\n".join(log)
            except ValueError as e:
                return str(e)

        # Story Interaction
        response = self.story_teller.next_turn(action)
        return f"DM: {response}"

    def _handle_combat_turn(self, action):
        log = []
        if action.lower() == "attack":
            hit, msg = self.combat.player_attack()
            log.append(msg)
            if self.combat.is_active:
                log.append(self.combat.monster_turn())
            else:
                log.append("Combat ended. You are victorious!")
                self.combat = None
        elif action.lower() == "flee":
            log.append("You flee from combat!")
            self.combat = None
        else:
            log.append("Combat options: attack, flee")

        if self.combat and self.combat.is_active:
             log.append(f"HP: {self.character.current_hp}/{self.character.max_hp}")

        return "\n".join(log)
