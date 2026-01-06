import unittest
from unittest.mock import MagicMock, patch
import json
import os
from src.character import Character
from src.game import Game
from src.story_teller import StoryTeller

class TestCharacter(unittest.TestCase):
    def test_character_creation(self):
        char = Character("Hero", "Human", "Fighter")
        self.assertEqual(char.name, "Hero")
        self.assertEqual(char.race, "Human")
        self.assertEqual(char.char_class, "Fighter")
        self.assertTrue(len(char.stats) == 6)
        self.assertTrue(char.hp > 0)

    def test_serialization(self):
        char = Character("Hero", "Human", "Fighter")
        data = char.to_dict()
        char2 = Character.from_dict(data)
        self.assertEqual(char.name, char2.name)
        self.assertEqual(char.stats, char2.stats)

class TestGame(unittest.TestCase):
    @patch('src.story_teller.OpenAI')
    @patch('builtins.input', side_effect=['TestWorld', '/quit', 'y']) # Set world, then quit
    @patch('src.character.Character.create_character')
    def test_new_game_flow(self, mock_create_char, mock_input, mock_openai):
        # Mock character creation
        mock_char = Character("Hero", "Human", "Fighter")
        mock_create_char.return_value = mock_char

        # Mock OpenAI response
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_completion = MagicMock()
        mock_completion.choices[0].message.content = "Welcome to the adventure."
        mock_client.chat.completions.create.return_value = mock_completion

        game = Game("fake-key")
        game.new_game()
        game.run()

        self.assertTrue(mock_create_char.called)
        # Check if API was called for opening scene
        self.assertTrue(mock_client.chat.completions.create.called)

    def test_save_load(self):
        char = Character("Hero", "Human", "Fighter")
        teller = StoryTeller("key")
        teller.history = [{"role": "system", "content": "foo"}]

        game = Game("key")
        game.character = char
        game.story_teller = teller

        game.save_game("test_save.json")

        game2 = Game("key")
        game2.load_game("test_save.json")

        self.assertEqual(game2.character.name, "Hero")
        self.assertEqual(game2.story_teller.history[0]['content'], "foo")

        # Cleanup
        if os.path.exists("test_save.json"):
            os.remove("test_save.json")

if __name__ == '__main__':
    unittest.main()
