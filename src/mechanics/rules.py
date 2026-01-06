from src.mechanics.dice import Dice

class Rules:
    @staticmethod
    def ability_check(character, ability, difficulty_class=10):
        mod = character._get_modifier(character.stats.get(ability, 10))
        roll, _ = Dice.roll("1d20")
        total = roll + mod
        return total >= difficulty_class, total

    @staticmethod
    def saving_throw(character, ability, dc):
        return Rules.ability_check(character, ability, dc)
