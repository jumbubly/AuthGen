import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QMessageBox, QWidget, QVBoxLayout, QHBoxLayout, QDialog
from PyQt6.QtGui import QIcon, QPixmap, QDesktopServices, QAction
from PyQt6.QtCore import Qt, QUrl, QTimer
from datetime import datetime
import pyperclip
import os
from auth_generator import AuthGenerator

class AuthGeneratorGUI(QMainWindow):
    def __init__(self, auth_generator):
        super().__init__()
        self.auth_generator = auth_generator
        self.setWindowTitle("Authentication Key Generator")
        self.auth_generator.load_config()  # Load the configuration
        
        self.about_dialog = None  # Instance variable to store the About dialog
        self.bitcoin_label = None  # Instance variable for the Bitcoin label

        # Set the window icon using the icon_path
        icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")
        self.setWindowIcon(QIcon(icon_path))

        self.central_widget_layout = QVBoxLayout()
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.central_widget_layout)
        self.setCentralWidget(self.central_widget)

        self.create_labels()
        self.create_buttons()
        self.create_key_label()

        self.create_menu()
        self.create_account_buttons()

        self.version_label = QLabel("Version 1.2")
        self.statusBar().addWidget(self.version_label, stretch=1)

    def create_menu(self):
        menu_bar = self.menuBar()

        # Create the "File" menu
        file_menu = menu_bar.addMenu("File")

        # Create the "About" action and pass the auth_generator instance
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about_dialog)
        file_menu.addAction(about_action)

        # Set the menu bar for the main window
        self.setMenuBar(menu_bar)

    def show_about_dialog(self):
        author_info = self.auth_generator.config.get("author_info", "Your Name")
        bitcoin_code = self.auth_generator.config.get("bitcoin_code", "1ABCxyz")

        about_text = f"Authentication Key Generator\n\nVersion: {self.auth_generator.version}\nAuthor: {author_info}\n\nDonate Bitcoin: {bitcoin_code}"

        self.about_dialog = QDialog(self)
        self.about_dialog.setWindowTitle("About")
        layout = QVBoxLayout(self.about_dialog)

        about_label = QLabel(about_text)
        layout.addWidget(about_label)

        copy_button = QPushButton("Copy")
        layout.addWidget(copy_button)

        def copy_bitcoin_address():
            pyperclip.copy(bitcoin_code)
            copy_button.setText("Copied To Clipboard")

        copy_button.clicked.connect(copy_bitcoin_address)

        self.about_dialog.finished.connect(self.handle_about_dialog_close)  # Connect finished signal
        self.about_dialog.exec()

    def handle_about_dialog_close(self):
        self.about_dialog.close()  # Close the dialog
        QTimer.singleShot(0, self.activateWindow)

    def open_github(self):
        github_url = self.auth_generator.config.get("github_account")
        if github_url:
            QDesktopServices.openUrl(QUrl(github_url))

    def open_cracked(self):
        cracked_url = self.auth_generator.config.get("cracked_account")
        if cracked_url:
            QDesktopServices.openUrl(QUrl(cracked_url))

    def create_labels(self):
        label_widget = QWidget()
        label_layout = QVBoxLayout(label_widget)

        # Icon
        icon_label = QLabel(self)
        icon_path = os.path.join(os.path.dirname(__file__), "AuthGenIcon.png")
        icon_label.setPixmap(QPixmap(icon_path).scaled(128, 128, Qt.AspectRatioMode.KeepAspectRatio))
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_layout.addWidget(icon_label)

        # Authentication Key Generator label
        generator_label = QLabel("Authentication Key Generator", self)
        generator_label.setFont(self.font())
        generator_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_layout.addWidget(generator_label)

        label_layout.addStretch(1)
        self.central_widget_layout.addWidget(label_widget)

    def create_key_label(self):
        self.key_label = QLabel(self)
        self.key_label.setText("")
        self.key_label.setFont(self.font())
        self.key_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.central_widget_layout.addWidget(self.key_label)

    def create_buttons(self):
        button_widget = QWidget()
        button_layout = QVBoxLayout(button_widget)

        # Create buttons for 1-day to 30-day durations
        durations1 = [1, 3, 7, 30]
        button_layout1 = QHBoxLayout()

        for days in durations1:
            button = QPushButton(f"{days}-Days Authentication Key")
            button.setStyleSheet("background-color: #4caf50; color: white;")
            button.clicked.connect(lambda _, d=days: self.generate_key_button_click(d, f'auth_keys_{d}'))
            button_layout1.addWidget(button)

        button_layout.addLayout(button_layout1)

        # Create button for displaying authentication keys
        button_display = QPushButton("Display Authentication Keys")
        button_display.setStyleSheet("background-color: #2196f3; color: white;")
        button_display.clicked.connect(self.display_keys_button_click)
        button_layout.addWidget(button_display)

        # Create buttons for 60-day to 360-day durations
        durations2 = [60, 90, 120, 360]
        button_layout2 = QHBoxLayout()

        for days in durations2:
            button = QPushButton(f"{days}-Days Authentication Key")
            button.setStyleSheet("background-color: #4caf50; color: white;")
            button.clicked.connect(lambda _, d=days: self.generate_key_button_click(d, f'auth_keys_{d}'))
            button_layout2.addWidget(button)

        button_layout.addLayout(button_layout2)

        button_layout.setSpacing(20)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.central_widget_layout.addWidget(button_widget)

    def create_account_buttons(self):
        account_buttons_widget = QWidget()
        account_buttons_layout = QHBoxLayout(account_buttons_widget)

        # Create button for GitHub Account
        button_github = QPushButton("My GitHub Account")
        button_github.setStyleSheet("background-color: #2196f3; color: white;")
        button_github.clicked.connect(self.open_github)
        account_buttons_layout.addWidget(button_github)

        # Create button for Cracked.io Account
        button_cracked = QPushButton("My Cracked.io Account")
        button_cracked.setStyleSheet("background-color: #2196f3; color: white;")
        button_cracked.clicked.connect(self.open_cracked)
        account_buttons_layout.addWidget(button_cracked)

        account_buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.central_widget_layout.addWidget(account_buttons_widget)


    def generate_key_button_click(self, days, table_name):
        auth_key, expiry_date = self.auth_generator.generate_auth_key(days, table_name)
        self.display_auth_key(auth_key, expiry_date)

    def display_auth_key(self, auth_key, expiry_date):
        self.key_label.setText(f"Authentication Key: {auth_key}\nExpires on: {expiry_date}")
        QMessageBox.information(self, "Authentication Key", f"Authentication Key: {auth_key}\nExpires on: {expiry_date}")

    def copy_key(self, key):
        pyperclip.copy(key)

    def delete_key(self, auth_key, table_name):
        self.auth_generator.delete_key(auth_key, table_name)
        self.display_keys_button_click()  # Recreate the display screen
        self.activateWindow()  # Set focus back to the main window

    def display_keys_button_click(self):
        if hasattr(self, "keys_window"):
            self.keys_window.close()  # Destroy the existing keys window if it exists

        self.keys_window = QWidget()
        self.keys_window.setWindowTitle("Authentication Keys")
        layout = QVBoxLayout(self.keys_window)

        durations = [1, 3, 7, 30, 60, 90, 120, 360]

        for days in durations:
            table_name = f'auth_keys_{days}'
            keys = self.auth_generator.get_auth_keys(days)
            key_count = len(keys)

            label_text = f"{days}-Days Authentication Keys"
            label = QLabel(label_text)
            layout.addWidget(label)

            if key_count > 0:
                for i, (auth_key, expiry_date) in enumerate(keys):
                    expiry_date = datetime.strptime(expiry_date.split()[0], "%Y-%m-%d")
                    key_frame = QWidget()
                    key_layout = QHBoxLayout(key_frame)

                    key_label = QLabel(f"{i + 1}. Key: {auth_key}   Expiry Date: {expiry_date.strftime('%Y-%m-%d')}")
                    if datetime.now() > expiry_date:
                        key_label.setStyleSheet("color: red;")
                    key_layout.addWidget(key_label)

                    copy_button = QPushButton("Copy")
                    copy_button.setStyleSheet("background-color: #2196f3; color: white;")
                    copy_button.clicked.connect(lambda _, k=auth_key: self.copy_key(k))
                    key_layout.addWidget(copy_button)

                    delete_button = QPushButton("Delete")
                    delete_button.setStyleSheet("background-color: #f44336; color: white;")
                    delete_button.clicked.connect(lambda _, k=auth_key, t=table_name: self.delete_key(k, t))
                    key_layout.addWidget(delete_button)

                    key_layout.setSpacing(5)
                    key_frame.setLayout(key_layout)
                    layout.addWidget(key_frame)
            else:
                layout.addWidget(QLabel("No keys found"))

        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.keys_window.setLayout(layout)
        self.keys_window.show()


def run_gui():
    app = QApplication(sys.argv)
    auth_generator = AuthGenerator()
    gui = AuthGeneratorGUI(auth_generator)
    gui.show()
    sys.exit(app.exec())

run_gui()