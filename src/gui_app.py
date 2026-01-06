import tkinter as tk
from tkinter import ttk, scrolledtext, simpledialog, messagebox
import os
from src.game import Game
from src.models.character import Character
from src.data.races import RACES
from src.data.classes import CLASSES

class AI_RPG_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI D&D RPG")
        self.root.geometry("800x600")

        self.game = None
        self.api_key = os.getenv("OPENAI_API_KEY") or os.getenv("DEEPSEEK_API_KEY")
        self.base_url = os.getenv("OPENAI_BASE_URL") or "https://api.deepseek.com"
        self.model_name = "deepseek-chat"

        self._setup_styles()
        self.show_startup_screen()

    def _setup_styles(self):
        style = ttk.Style()
        style.configure("TButton", padding=6)
        style.configure("TLabel", font=("Helvetica", 12))

    def show_startup_screen(self):
        self._clear_window()

        frame = ttk.Frame(self.root, padding="20")
        frame.pack(expand=True, fill='both')

        ttk.Label(frame, text="AI D&D RPG", font=("Helvetica", 24, "bold")).pack(pady=20)

        # API Config
        config_frame = ttk.LabelFrame(frame, text="API Configuration", padding="10")
        config_frame.pack(fill='x', pady=10)

        ttk.Label(config_frame, text="API Key:").grid(row=0, column=0, sticky='w')
        self.api_key_entry = ttk.Entry(config_frame, width=40)
        if self.api_key:
            self.api_key_entry.insert(0, self.api_key)
        self.api_key_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(config_frame, text="Base URL:").grid(row=1, column=0, sticky='w')
        self.base_url_entry = ttk.Entry(config_frame, width=40)
        self.base_url_entry.insert(0, self.base_url)
        self.base_url_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(config_frame, text="Model:").grid(row=2, column=0, sticky='w')
        self.model_entry = ttk.Entry(config_frame, width=40)
        self.model_entry.insert(0, self.model_name)
        self.model_entry.grid(row=2, column=1, padx=5, pady=5)

        # Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=20)

        ttk.Button(btn_frame, text="New Game", command=self.show_char_creation).pack(side='left', padx=10)
        ttk.Button(btn_frame, text="Load Game", command=self.load_game).pack(side='left', padx=10)

    def _get_api_config(self):
        return {
            "api_key": self.api_key_entry.get().strip(),
            "base_url": self.base_url_entry.get().strip(),
            "model_name": self.model_entry.get().strip()
        }

    def show_char_creation(self):
        config = self._get_api_config()
        if not config["api_key"]:
            messagebox.showerror("Error", "API Key is required.")
            return

        self.game = Game(**config)
        self._clear_window()

        frame = ttk.Frame(self.root, padding="20")
        frame.pack(expand=True, fill='both')

        ttk.Label(frame, text="Create Your Character", font=("Helvetica", 18)).pack(pady=10)

        # Name
        ttk.Label(frame, text="Name:").pack(anchor='w')
        name_entry = ttk.Entry(frame)
        name_entry.pack(fill='x', pady=5)

        # Race
        ttk.Label(frame, text="Race:").pack(anchor='w')
        race_var = tk.StringVar()
        race_combo = ttk.Combobox(frame, textvariable=race_var, values=list(RACES.keys()))
        race_combo.pack(fill='x', pady=5)
        race_combo.current(0)

        # Class
        ttk.Label(frame, text="Class:").pack(anchor='w')
        class_var = tk.StringVar()
        class_combo = ttk.Combobox(frame, textvariable=class_var, values=list(CLASSES.keys()))
        class_combo.pack(fill='x', pady=5)
        class_combo.current(0)

        # Setting
        ttk.Label(frame, text="Campaign Setting/Genre:").pack(anchor='w')
        setting_entry = ttk.Entry(frame)
        setting_entry.insert(0, "High Fantasy")
        setting_entry.pack(fill='x', pady=5)

        def start():
            name = name_entry.get().strip()
            race = race_var.get()
            char_class = class_var.get()
            setting = setting_entry.get().strip()

            if not name:
                messagebox.showerror("Error", "Name is required.")
                return

            # Create character logic
            # Note: The original CLI Character.create_character rolled stats.
            # We'll just init character here.
            char = Character(name, race, char_class)

            # Start UI
            self.show_game_screen()

            # Async start campaign to keep UI responsive?
            # Tkinter is single threaded. For MVP we'll block briefly.
            try:
                msg = self.game.initialize_campaign(char, setting)
                self.log_message(msg)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to start game: {e}")
                self.show_startup_screen()

        ttk.Button(frame, text="Start Adventure", command=start).pack(pady=20)
        ttk.Button(frame, text="Back", command=self.show_startup_screen).pack(pady=5)

    def load_game(self):
        config = self._get_api_config()
        if not config["api_key"]:
            messagebox.showerror("Error", "API Key is required.")
            return

        self.game = Game(**config)
        msg = self.game.load_game()
        if "not found" in msg.lower():
            messagebox.showerror("Error", msg)
        else:
            self.show_game_screen()
            self.log_message(msg)

    def show_game_screen(self):
        self._clear_window()

        # Main Layout: Text on left, Sidebar on right
        main_pane = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_pane.pack(fill='both', expand=True)

        # Left: Chat/Log
        left_frame = ttk.Frame(main_pane)
        main_pane.add(left_frame, weight=3)

        self.log_area = scrolledtext.ScrolledText(left_frame, state='disabled', wrap='word', font=("Georgia", 11))
        self.log_area.pack(fill='both', expand=True, padx=5, pady=5)

        # Input area
        input_frame = ttk.Frame(left_frame)
        input_frame.pack(fill='x', padx=5, pady=5)

        self.input_entry = ttk.Entry(input_frame)
        self.input_entry.pack(side='left', fill='x', expand=True)
        self.input_entry.bind("<Return>", lambda e: self.send_command())

        send_btn = ttk.Button(input_frame, text="Send", command=self.send_command)
        send_btn.pack(side='right', padx=5)

        # Right: Stats & Controls
        right_frame = ttk.Frame(main_pane, padding="5")
        main_pane.add(right_frame, weight=1)

        # Stats
        self.stats_label = ttk.Label(right_frame, text=self._get_stats_text(), justify='left')
        self.stats_label.pack(anchor='n', pady=10)

        # Buttons
        ttk.Button(right_frame, text="Inventory", command=lambda: self.send_hidden_command("/inventory")).pack(fill='x', pady=2)
        ttk.Button(right_frame, text="Character Sheet", command=lambda: self.send_hidden_command("/sheet")).pack(fill='x', pady=2)
        ttk.Button(right_frame, text="Save Game", command=lambda: self.send_hidden_command("/save")).pack(fill='x', pady=2)
        ttk.Button(right_frame, text="Quit to Menu", command=self.show_startup_screen).pack(fill='x', pady=20)

    def _get_stats_text(self):
        if not self.game or not self.game.character:
            return ""
        c = self.game.character
        return (f"{c.name}\n"
                f"Lvl {c.level} {c.race} {c.char_class}\n"
                f"HP: {c.current_hp}/{c.max_hp}\n"
                f"XP: {c.xp}")

    def update_stats(self):
        if self.stats_label:
            self.stats_label.config(text=self._get_stats_text())

    def log_message(self, message):
        self.log_area.config(state='normal')
        self.log_area.insert('end', message + "\n\n")
        self.log_area.see('end')
        self.log_area.config(state='disabled')
        self.update_stats()

    def send_command(self):
        text = self.input_entry.get()
        if not text:
            return

        self.log_message(f"> {text}")
        self.input_entry.delete(0, 'end')

        # Run game processing
        try:
            response = self.game.process_action(text)
            self.log_message(response)
        except Exception as e:
             self.log_message(f"Error: {e}")

    def send_hidden_command(self, cmd):
        # Sends a command without echoing the user input (optional, but good for buttons)
        try:
            response = self.game.process_action(cmd)
            self.log_message(response)
        except Exception as e:
             self.log_message(f"Error: {e}")

    def _clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AI_RPG_GUI(root)
    root.mainloop()
