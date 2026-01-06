import random
import re

class Dice:
    @staticmethod
    def roll(expression):
        """
        Rolls dice based on expression like "1d20+5" or "2d6".
        Returns a tuple (total, details).
        """
        expression = expression.lower().replace(" ", "")

        # Simple parser for XdY(+/-Z)
        match = re.match(r"(\d+)d(\d+)([\+\-]\d+)?", expression)
        if not match:
            # Maybe it's just a number
            try:
                val = int(expression)
                return val, f"[Constant: {val}]"
            except ValueError:
                return 0, "[Invalid Dice String]"

        count = int(match.group(1))
        sides = int(match.group(2))
        modifier = 0
        if match.group(3):
            modifier = int(match.group(3))

        rolls = [random.randint(1, sides) for _ in range(count)]
        total = sum(rolls) + modifier

        details = f"[{expression}]: {rolls} {'+' if modifier >= 0 else ''}{modifier} = {total}"
        return total, details

    @staticmethod
    def roll_advantage(expression):
        total1, details1 = Dice.roll(expression)
        total2, details2 = Dice.roll(expression)
        return max(total1, total2), f"Advantage: {details1} vs {details2}"

    @staticmethod
    def roll_disadvantage(expression):
        total1, details1 = Dice.roll(expression)
        total2, details2 = Dice.roll(expression)
        return min(total1, total2), f"Disadvantage: {details1} vs {details2}"
