import customtkinter as ctk
import os
import threading
from tkinter import messagebox
from src.game import Game
from src.models.character import Character
from src.data.races import RACES
from src.data.classes import CLASSES

# Set Appearance
ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class AI_RPG_GUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("AI D&D RPG")
        self.geometry("1000x700")

        # Grid layout configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.game = None
        self.api_key = os.getenv("OPENAI_API_KEY") or os.getenv("DEEPSEEK_API_KEY") or ""
        self.base_url = os.getenv("OPENAI_BASE_URL") or "https://api.deepseek.com"

        self.current_frame = None
        self.show_setup_screen()

    def show_frame(self, frame_class, **kwargs):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = frame_class(self, **kwargs)
        self.current_frame.grid(row=0, column=0, sticky="nsew")

    def show_setup_screen(self):
        self.show_frame(SetupFrame, app=self)

    def show_char_creation(self):
        self.show_frame(CharacterCreationFrame, app=self)

    def show_game_screen(self):
        self.show_frame(GameFrame, app=self)


class SetupFrame(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.center_frame = ctk.CTkFrame(self)
        self.center_frame.grid(row=0, column=0)

        # Title
        ctk.CTkLabel(self.center_frame, text="AI RPG Setup", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)

        # Provider Selection
        ctk.CTkLabel(self.center_frame, text="Select Provider:").pack(anchor="w", padx=20)
        self.provider_var = ctk.StringVar(value="DeepSeek")
        self.provider_menu = ctk.CTkOptionMenu(self.center_frame, variable=self.provider_var,
                                             values=["DeepSeek", "OpenAI", "Custom"],
                                             command=self.update_options)
        self.provider_menu.pack(fill="x", padx=20, pady=(0, 10))

        # API Key
        ctk.CTkLabel(self.center_frame, text="API Key:").pack(anchor="w", padx=20)
        self.api_key_entry = ctk.CTkEntry(self.center_frame, show="*", width=300)
        if self.app.api_key:
             self.api_key_entry.insert(0, self.app.api_key)
        self.api_key_entry.pack(fill="x", padx=20, pady=(0, 10))

        # Base URL (Hidden unless Custom)
        self.base_url_label = ctk.CTkLabel(self.center_frame, text="Base URL:")
        self.base_url_entry = ctk.CTkEntry(self.center_frame, width=300)

        # Model Selection
        ctk.CTkLabel(self.center_frame, text="Select Model:").pack(anchor="w", padx=20)
        self.model_var = ctk.StringVar(value="deepseek-chat")
        self.model_menu = ctk.CTkOptionMenu(self.center_frame, variable=self.model_var,
                                          values=["deepseek-chat", "deepseek-reasoner"])
        self.model_menu.pack(fill="x", padx=20, pady=(0, 20))

        # Connect Button
        ctk.CTkButton(self.center_frame, text="Connect & Start", command=self.connect).pack(pady=(20, 10))
        ctk.CTkButton(self.center_frame, text="Load Game", command=self.load_game).pack(pady=10)

        # Initialize visibility
        self.update_options("DeepSeek")

    def update_options(self, choice):
        if choice == "DeepSeek":
            self.model_menu.configure(values=["deepseek-chat", "deepseek-reasoner"])
            self.model_var.set("deepseek-chat")
            self.hide_base_url()
        elif choice == "OpenAI":
            self.model_menu.configure(values=["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"])
            self.model_var.set("gpt-3.5-turbo")
            self.hide_base_url()
        else: # Custom
            self.model_menu.configure(values=[])
            self.model_var.set("")
            self.show_base_url()

    def show_base_url(self):
        self.base_url_label.pack(anchor="w", padx=20)
        self.base_url_entry.pack(fill="x", padx=20, pady=(0, 10))
        if self.app.base_url:
            self.base_url_entry.delete(0, 'end')
            self.base_url_entry.insert(0, self.app.base_url)

    def hide_base_url(self):
        self.base_url_label.pack_forget()
        self.base_url_entry.pack_forget()

    def connect(self, target_frame="char_creation"):
        provider = self.provider_var.get()
        api_key = self.api_key_entry.get().strip()
        model = self.model_var.get().strip()
        base_url = None

        if provider == "DeepSeek":
            base_url = "https://api.deepseek.com"
        elif provider == "Custom":
            base_url = self.base_url_entry.get().strip()

        if not api_key:
            if not os.getenv("DEEPSEEK_API_KEY") and not os.getenv("OPENAI_API_KEY"):
                 pass

        self.app.api_key = api_key
        self.app.base_url = base_url
        self.app.model_name = model

        # Init Game Object here? No, Game is init later.
        # But for Load Game we need Game object.

        if target_frame == "char_creation":
            self.app.show_char_creation()
        elif target_frame == "load_game":
            self.perform_load()

    def load_game(self):
        self.connect(target_frame="load_game")

    def perform_load(self):
        try:
            self.app.game = Game(
                api_key=self.app.api_key,
                base_url=self.app.base_url,
                model_name=self.app.model_name
            )
            msg = self.app.game.load_game() # Loads savegame.json by default

            if "not found" in msg.lower():
                messagebox.showerror("Error", msg)
                return

            self.app.show_game_screen()
            self.app.after(100, lambda: self.app.current_frame.log_message(msg))

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load: {e}")


class CharacterCreationFrame(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.center_frame = ctk.CTkFrame(self)
        self.center_frame.grid(row=0, column=0)

        ctk.CTkLabel(self.center_frame, text="Create Character", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)

        # Name
        ctk.CTkLabel(self.center_frame, text="Name:").pack(anchor="w", padx=20)
        self.name_entry = ctk.CTkEntry(self.center_frame, width=300)
        self.name_entry.pack(padx=20, pady=(0, 10))

        # Race
        ctk.CTkLabel(self.center_frame, text="Race:").pack(anchor="w", padx=20)
        self.race_var = ctk.StringVar(value=list(RACES.keys())[0])
        ctk.CTkOptionMenu(self.center_frame, variable=self.race_var, values=list(RACES.keys())).pack(fill="x", padx=20, pady=(0, 10))

        # Class
        ctk.CTkLabel(self.center_frame, text="Class:").pack(anchor="w", padx=20)
        self.class_var = ctk.StringVar(value=list(CLASSES.keys())[0])
        ctk.CTkOptionMenu(self.center_frame, variable=self.class_var, values=list(CLASSES.keys())).pack(fill="x", padx=20, pady=(0, 10))

        # Setting
        ctk.CTkLabel(self.center_frame, text="Campaign Setting:").pack(anchor="w", padx=20)
        self.setting_entry = ctk.CTkEntry(self.center_frame, width=300)
        self.setting_entry.insert(0, "High Fantasy Adventure")
        self.setting_entry.pack(padx=20, pady=(0, 20))

        ctk.CTkButton(self.center_frame, text="Start Adventure", command=self.start_game).pack(pady=20)
        ctk.CTkButton(self.center_frame, text="Back", fg_color="transparent", border_width=1, command=self.app.show_setup_screen).pack(pady=5)

    def start_game(self):
        name = self.name_entry.get()
        if not name:
             return

        char = Character(name, self.race_var.get(), self.class_var.get())

        # Init Game
        try:
            self.app.game = Game(
                api_key=self.app.api_key,
                base_url=self.app.base_url,
                model_name=self.app.model_name
            )
            # Show game screen first, then load content async to avoid freeze
            self.app.show_game_screen()

            # Run startup in thread
            threading.Thread(target=self.init_campaign_async, args=(char, self.setting_entry.get())).start()

        except Exception as e:
            print(e) # In GUI we might want a popup

    def init_campaign_async(self, char, setting):
        msg = self.app.game.initialize_campaign(char, setting)
        # Update UI from main thread
        self.app.after(0, self.app.current_frame.log_message, msg)


class GameFrame(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app

        # Layout: Sidebar (Left), Main (Right)
        self.grid_columnconfigure(1, weight=3) # Main
        self.grid_columnconfigure(0, weight=1) # Sidebar
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar_label = ctk.CTkLabel(self.sidebar, text="Character", font=ctk.CTkFont(size=20, weight="bold"))
        self.sidebar_label.pack(pady=20)

        self.stats_label = ctk.CTkLabel(self.sidebar, text="", justify="left", font=ctk.CTkFont(family="Courier", size=12))
        self.stats_label.pack(padx=20, pady=10, anchor="w")

        self.update_stats()

        # Action Buttons in Sidebar
        ctk.CTkButton(self.sidebar, text="Inventory", command=lambda: self.send_cmd("/inventory")).pack(padx=20, pady=10)
        ctk.CTkButton(self.sidebar, text="Character Sheet", command=lambda: self.send_cmd("/sheet")).pack(padx=20, pady=10)
        ctk.CTkButton(self.sidebar, text="Save Game", command=lambda: self.send_cmd("/save")).pack(padx=20, pady=10)
        ctk.CTkButton(self.sidebar, text="Quit", fg_color="red", command=self.app.show_setup_screen).pack(padx=20, pady=20, side="bottom")

        # Main Content
        self.main_area = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_area.grid(row=0, column=1, sticky="nsew")
        self.main_area.grid_rowconfigure(0, weight=1)
        self.main_area.grid_columnconfigure(0, weight=1)

        # Chat Log
        self.log_box = ctk.CTkTextbox(self.main_area, font=ctk.CTkFont(family="Georgia", size=14), wrap="word")
        self.log_box.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.log_box.configure(state="disabled")

        # Input Area
        self.input_frame = ctk.CTkFrame(self.main_area, height=50)
        self.input_frame.grid(row=1, column=0, padx=20, pady=20, sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.input_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Type your action...")
        self.input_entry.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.input_entry.bind("<Return>", lambda e: self.send_cmd())

        self.send_btn = ctk.CTkButton(self.input_frame, text="Send", width=100, command=self.send_cmd)
        self.send_btn.grid(row=0, column=1, padx=10, pady=10)

    def update_stats(self):
        if self.app.game and self.app.game.character:
            c = self.app.game.character
            text = (f"Name: {c.name}\n"
                    f"Race: {c.race}\n"
                    f"Class: {c.char_class}\n\n"
                    f"Level: {c.level}\n"
                    f"XP: {c.xp}\n"
                    f"HP: {c.current_hp}/{c.max_hp}")
            self.stats_label.configure(text=text)

    def log_message(self, msg):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", msg + "\n\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")
        self.update_stats()

    def send_cmd(self, cmd=None):
        if cmd:
            text = cmd
        else:
            text = self.input_entry.get()
            self.input_entry.delete(0, 'end')

        if not text:
            return

        self.log_message(f"> {text}")

        # Process in thread to not freeze UI
        threading.Thread(target=self.process_action_async, args=(text,)).start()

    def process_action_async(self, action):
        if self.app.game:
            res = self.app.game.process_action(action)
            self.app.after(0, self.log_message, res)

if __name__ == "__main__":
    app = AI_RPG_GUI()
    app.mainloop()
