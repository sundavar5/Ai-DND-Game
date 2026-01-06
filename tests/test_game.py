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

class TestGameRefactored(unittest.TestCase):
    @patch('src.story_teller.OpenAI')
    def test_campaign_flow(self, mock_openai):
        # Mock OpenAI
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_completion = MagicMock()
        mock_completion.choices[0].message.content = "Welcome to the dungeon."
        mock_client.chat.completions.create.return_value = mock_completion

        # Init Game
        game = Game(api_key="fake", base_url="fake", model_name="fake-model")
        char = Character("Hero", "Human", "Fighter")

        # Start Campaign
        res = game.initialize_campaign(char, "Dark Fantasy")
        self.assertIn("Campaign Started", res)
        self.assertTrue(game.is_running)

        # Test Command
        res = game.process_action("/inventory")
        self.assertIn("Inventory", res)

        # Test Story Interaction
        res = game.process_action("Look around")
        self.assertIn("DM:", res)

    def test_combat_flow(self):
        # We can test combat logic without mocking OpenAI since /fight doesn't call it immediately
        # unless we need story response? No, process_action handles /fight locally first.

        game = Game(api_key="fake")
        char = Character("Hero", "Human", "Fighter")
        game.character = char
        game.is_running = True

        # Start Fight
        res = game.process_action("/fight goblin")
        # Depending on initiative, output varies, but should contain "Combat Started"
        self.assertIn("Combat Started", res)
        self.assertTrue(game.combat.is_active)

        # Attack
        res = game.process_action("attack")
        self.assertIn("hit", res.lower()) # either you hit or miss, or they hit/miss

        # Flee
        res = game.process_action("flee")
        self.assertIn("flee", res)
        self.assertIsNone(game.combat)

if __name__ == '__main__':
    unittest.main()
