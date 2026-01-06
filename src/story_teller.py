from openai import OpenAI
import os

class StoryTeller:
    def __init__(self, api_key, base_url=None):
        if base_url:
            self.client = OpenAI(api_key=api_key, base_url=base_url)
        else:
            self.client = OpenAI(api_key=api_key)
        self.history = []

    def start_campaign(self, character, setting_description):
        system_prompt = (
            "You are a Dungeon Master for a D&D game. "
            "Your goal is to provide an immersive, interactive storytelling experience. "
            "You should describe the environment, NPCs, and events based on the player's actions. "
            "Keep your responses concise but descriptive (around 1-2 paragraphs). "
            "Ask the player what they want to do next at the end of your description."
        )

        char_info = str(character)
        initial_prompt = (
            f"The game is starting. The setting is: {setting_description}\n"
            f"The character is:\n{char_info}\n\n"
            "Please describe the opening scene where the character finds themselves."
        )

        self.history.append({"role": "system", "content": system_prompt})
        self.history.append({"role": "user", "content": initial_prompt})

        return self._get_response()

    def next_turn(self, user_action):
        self.history.append({"role": "user", "content": user_action})
        return self._get_response()

    def _get_response(self):
        try:
            completion = self.client.chat.completions.create(
                model="gpt-3.5-turbo", # Default to a widely available model
                messages=self.history
            )
            response = completion.choices[0].message.content
            self.history.append({"role": "assistant", "content": response})
            return response
        except Exception as e:
            return f"Error connecting to AI: {e}"

    def get_history(self):
        return self.history
