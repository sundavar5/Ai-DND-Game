import os
import sys
from dotenv import load_dotenv
from src.game import Game

def main():
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")

    print("Welcome to AI D&D!")
    if not api_key:
        print("No OPENAI_API_KEY found in environment.")
        api_key = input("Please enter your OpenAI API Key: ").strip()
        if not api_key:
            print("API Key is required to play.")
            sys.exit(1)

    game = Game(api_key, base_url)

    while True:
        print("\nMain Menu:")
        print("1. New Game")
        print("2. Load Game")
        print("3. Quit")

        choice = input("Select an option: ")

        if choice == "1":
            game.new_game()
            game.run()
        elif choice == "2":
            if game.load_game():
                game.run()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
