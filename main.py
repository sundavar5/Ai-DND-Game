import tkinter as tk
from src.gui_app import AI_RPG_GUI
from dotenv import load_dotenv
import os
import sys

def main():
    load_dotenv()

    # Check if we are in a graphical environment or fallback to CLI?
    # The user asked for a dedicated window, so we assume GUI.
    # But for robustness in headless CI/CD, we might want to handle it?
    # For now, just launch GUI.

    try:
        app = AI_RPG_GUI()
    except Exception as e:
        print(f"Error launching GUI: {e}")
        print("Please ensure you are running in a desktop environment with a display.")
        return

    app.mainloop()

if __name__ == "__main__":
    main()
