import tkinter as tk
from tkinter import messagebox
import pyperclip
import webbrowser
from datetime import datetime
from auth_generator import AuthGenerator
import os


class AuthGeneratorGUI:
    def __init__(self, auth_generator):
        self.auth_generator = auth_generator
        self.window = tk.Tk()
        self.window.title("Authentication Key Generator")
        self.auth_generator.load_config()  # Load the configuration

        # Set the window icon using the icon_path
        icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")
        self.window.iconbitmap(icon_path)

        self.create_labels()
        self.create_buttons()
        self.create_key_label()

        self.author_label = tk.Label(self.window, text=self.auth_generator.config.get("author_info", ""))
        self.author_label.pack(side=tk.BOTTOM, pady=10)

        self.github_label = tk.Label(self.window, text="GitHub Account: " + self.auth_generator.config.get("github_account", ""),
                                     fg="blue", cursor="hand2")
        self.github_label.pack(side=tk.BOTTOM, pady=5)

        self.cracked_label = tk.Label(self.window, text="Cracked Account: " + self.auth_generator.config.get("cracked_account", ""),
                                      fg="blue", cursor="hand2")
        self.cracked_label.pack(side=tk.BOTTOM, pady=5)

        self.bitcoin_label = tk.Label(self.window, text="Donate Bitcoin: " + self.auth_generator.config.get("bitcoin_code", ""),
                              cursor="xterm")
        self.bitcoin_label.pack(side=tk.BOTTOM, pady=5)
        self.bitcoin_label.bind("<Button-1>", self.copy_bitcoin)

    def copy_bitcoin(self, event):
        bitcoin_code = self.auth_generator.config.get("bitcoin_code", "")
        if bitcoin_code:
         pyperclip.copy(bitcoin_code)
         messagebox.showinfo("Bitcoin Code", "Bitcoin code copied to clipboard.")


        # Make the GitHub and Cracked labels clickable
        self.github_label.bind("<Button-1>", self.open_github)
        self.cracked_label.bind("<Button-1>", self.open_cracked)

    def open_github(self, event):
        github_url = self.auth_generator.config.get("github_account")
        if github_url:
            webbrowser.open_new(github_url)

    def open_cracked(self, event):
        cracked_url = self.auth_generator.config.get("cracked_account")
        if cracked_url:
            webbrowser.open_new(cracked_url)

    def create_labels(self):
        pass

    def create_key_label(self):
        self.key_label = tk.Label(self.window, text="", font=("Arial", 14, "bold"), pady=20)
        self.key_label.pack()

    def create_buttons(self):
        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=20)

        button_1day = tk.Button(button_frame, text="1-Day Authentication Key", bg="#4caf50", fg="white",
                                command=lambda: self.generate_key_button_click(1, 'auth_keys_1'))
        button_1day.pack(side=tk.LEFT, padx=10)

        button_3days = tk.Button(button_frame, text="3-Days Authentication Key", bg="#4caf50", fg="white",
                                 command=lambda: self.generate_key_button_click(3, 'auth_keys_3'))
        button_3days.pack(side=tk.LEFT, padx=10)

        button_7days = tk.Button(button_frame, text="7-Days Authentication Key", bg="#4caf50", fg="white",
                                 command=lambda: self.generate_key_button_click(7, 'auth_keys_7'))
        button_7days.pack(side=tk.LEFT, padx=10)

        button_30days = tk.Button(button_frame, text="30-Days Authentication Key", bg="#4caf50", fg="white",
                                  command=lambda: self.generate_key_button_click(30, 'auth_keys_30'))
        button_30days.pack(side=tk.LEFT, padx=10)

        button_display = tk.Button(self.window, text="Display Authentication Keys", bg="#2196f3", fg="white",
                                   command=self.display_keys_button_click)
        button_display.pack(pady=10)

    def generate_key_button_click(self, days, table_name):
        auth_key, expiry_date = self.auth_generator.generate_auth_key(days, table_name)
        self.display_auth_key(auth_key, expiry_date)

    def display_auth_key(self, auth_key, expiry_date):
        self.key_label.config(text=f"Authentication Key: {auth_key}\nExpires on: {expiry_date}")
        messagebox.showinfo("Authentication Key", f"Authentication Key: {auth_key}\nExpires on: {expiry_date}")

    def copy_key(self, key):
        pyperclip.copy(key)

    def delete_key(self, auth_key, table_name):
        self.auth_generator.delete_key(auth_key, table_name)
        self.display_keys_button_click()  # Recreate the display screen
        self.window.focus_set()  # Set focus back to the main window

    def display_keys_button_click(self):
        if hasattr(self, "keys_window"):
            self.keys_window.destroy()  # Destroy the existing keys window if it exists

        self.keys_window = tk.Toplevel(self.window)
        self.keys_window.title("Authentication Keys")

        for days, label_text in [(1, "1-Day Authentication Keys"),
                                 (3, "3-Days Authentication Keys"),
                                 (7, "7-Days Authentication Keys"),
                                 (30, "30-Days Authentication Keys")]:
            table_name = f'auth_keys_{days}'
            keys = self.auth_generator.get_auth_keys(days)
            key_count = len(keys)

            label = tk.Label(self.keys_window, text=label_text)
            label.pack()

            if key_count > 0:
                for i, (auth_key, expiry_date) in enumerate(keys):
                    expiry_date = datetime.strptime(expiry_date.split()[0], "%Y-%m-%d")
                    key_frame = tk.Frame(self.keys_window)
                    key_frame.pack()

                    key_label = tk.Label(key_frame,
                                         text=f"{i + 1}. Key: {auth_key}   Expiry Date: {expiry_date.strftime('%Y-%m-%d')}")
                    if datetime.now() > expiry_date:
                        key_label.config(fg="red")
                    key_label.pack(side=tk.LEFT)

                    copy_button = tk.Button(key_frame, text="Copy", bg="#2196f3", fg="white",
                                            command=lambda k=auth_key: self.copy_key(k))
                    copy_button.pack(side=tk.LEFT, padx=5)

                    delete_button = tk.Button(key_frame, text="Delete", bg="#f44336", fg="white",
                                              command=lambda k=auth_key, t=table_name: self.delete_key(k, t))
                    delete_button.pack(side=tk.LEFT, padx=5)
            else:
                tk.Label(self.keys_window, text="No keys found").pack()

    def run(self):
        self.window.mainloop()


def run_gui():
    # Create an instance of AuthGenerator
    auth_generator = AuthGenerator()

    # Create an instance of AuthGeneratorGUI and pass the auth_generator instance
    gui = AuthGeneratorGUI(auth_generator)
    gui.run()
