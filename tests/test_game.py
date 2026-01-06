import unittest
from unittest.mock import MagicMock, patch
import json
import os
from src.models.character import Character
from src.game import Game
from src.story_teller import StoryTeller
from src.mechanics.dice import Dice

class TestCharacter(unittest.TestCase):
    def test_character_creation(self):
        char = Character("Hero", "Human", "Fighter")
        self.assertEqual(char.name, "Hero")
        self.assertEqual(char.race, "Human")
        self.assertEqual(char.char_class, "Fighter")
        self.assertTrue(char.max_hp > 0)
        # Check stat bonuses
        # Human has +1 to all
        self.assertTrue(all(v >= 0 for v in char.stats.values()))

    def test_serialization(self):
        char = Character("Hero", "Human", "Fighter")
        char.current_hp = 5
        data = char.to_dict()
        char2 = Character.from_dict(data)
        self.assertEqual(char.name, char2.name)
        self.assertEqual(char.current_hp, 5)

class TestDice(unittest.TestCase):
    def test_parsing(self):
        val, _ = Dice.roll("1d1+5")
        self.assertEqual(val, 6)

    def test_invalid(self):
        val, _ = Dice.roll("invalid")
        self.assertEqual(val, 0)

class TestGame(unittest.TestCase):
    @patch('src.story_teller.OpenAI')
    @patch('builtins.input', side_effect=['TestWorld', '/quit', 'y'])
    @patch('src.models.character.Character.create_character')
    def test_new_game_flow(self, mock_create_char, mock_input, mock_openai):
        mock_char = Character("Hero", "Human", "Fighter")
        mock_create_char.return_value = mock_char

        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_completion = MagicMock()
        mock_completion.choices[0].message.content = "Welcome."
        mock_client.chat.completions.create.return_value = mock_completion

        game = Game("fake-key")
        game.new_game()
        game.run()

        self.assertTrue(mock_create_char.called)

if __name__ == '__main__':
    unittest.main()
