import secrets
import sqlite3
import json
import os
from datetime import datetime, timedelta
from PyQt6.QtWidgets import QMessageBox

config_file = "config.json"

class AuthGenerator:
    def __init__(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = None
        self.config = None  # Added config attribute
        self.version = "1.2"  # Added version attribute
        self.load_config()
        self.db_path = os.path.join(self.current_dir, self.db_path)
        self.initialize_database()

    def load_config(self):
        config_path = os.path.join(self.current_dir, config_file)
        with open(config_path, "r") as f:
           self.config = json.load(f)  # Update the config attribute
           self.db_path = self.config.get("db_path", "auth.db")

    def initialize_database(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS configuration (config_key text, config_value text)')
            # Add more table creations if needed

    def generate_auth_key(self, days, table_name):
        auth_key = secrets.token_hex(16)
        expiry_date = datetime.now() + timedelta(days=days)
        self.save_auth_key_info(auth_key, expiry_date, table_name)
        return auth_key, expiry_date

    def save_auth_key_info(self, auth_key, expiry_date, table_name):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name} (auth_key text, expiry_date text)')
            cursor.execute(f'INSERT INTO {table_name} VALUES (?, ?)', (auth_key, expiry_date))

    def delete_key(self, auth_key, table_name):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(f'DELETE FROM {table_name} WHERE auth_key = ?', (auth_key,))
        QMessageBox.information(None, "Key Deleted", f"The key {auth_key} has been deleted.")

    def get_auth_keys(self, days):
        table_prefix = self.config.get("table_prefix", "auth_keys_")
        table_name = f'{table_prefix}{days}'

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
            result = cursor.fetchone()

            if result is None:
                return []

            cursor.execute(f'SELECT auth_key, expiry_date FROM {table_name}')
            keys = cursor.fetchall()

        return keys
