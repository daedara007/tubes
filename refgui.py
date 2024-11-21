import sys
import getpass
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QLabel, QLineEdit, QPushButton, QMessageBox)

USER_DATA_FILE = 'users.txt'

class UserManagementApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("User  Management System")
        self.setGeometry(100, 100, 300, 200)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.username_label = QLabel("Username:", self)
        self.layout.addWidget(self.username_label)

        self.username_input = QLineEdit(self)
        self.layout.addWidget(self.username_input)

        self.password_label = QLabel("Password:", self)
        self.layout.addWidget(self.password_label)

        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.password_input)

        self.login_button = QPushButton("Login", self)
        self.login_button.clicked.connect(self.login)
        self.layout.addWidget(self.login_button)

        self.register_button = QPushButton("Register", self)
        self.register_button.clicked.connect(self.register)
        self.layout.addWidget(self.register_button)

        self.token = ""

    def load_users(self):
        """Membaca pengguna dari file dan mengembalikannya sebagai dictionary."""
        users = {}
        if os.path.exists(USER_DATA_FILE):
            with open(USER_DATA_FILE, 'r') as file:
                for line in file:
                    username, password = line.strip().split(',')
                    users[username] = password
        return users

    def save_user(self, username, password):
        """Menyimpan pengguna baru ke dalam file."""
        with open(USER_DATA_FILE, 'a') as file:
            file.write(f"{username},{password}\n")

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if username == "":
            QMessageBox.warning(self, "Error", "Username tidak boleh kosong")
            return

        users = self.load_users()
        if username in users:
            QMessageBox.warning(self, "Error", "Username sudah ada. Silakan pilih username yang berbeda.")
            return

        if len(password) < 8:
            QMessageBox.warning(self, "Error", "Password minimal 8 karakter")
            return

        self.save_user(username, password)
        QMessageBox.information(self, "Success", "Pendaftaran berhasil!")

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        users = self.load_users()

        if username in users and users[username] == password:
            self.token = username
            QMessageBox.information(self, "Success", f"Selamat datang {self.token} di dashboard")
            self.dashboard(self)
        else:
            QMessageBox.warning(self, "Error", "Username atau password salah.")

    def dashboard(self):
        super().__init__()
        self.setWindowTitle("Simple Dashboard")
        self.setGeometry(100, 100, 400, 300)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.title_label = QLabel("Welcome to the Dashboard", self)
        self.layout.addWidget(self.title_label)

        self.input_label = QLabel("Enter some data:", self)
        self.layout.addWidget(self.input_label)

        self.data_input = QLineEdit(self)
        self.layout.addWidget(self.data_input)

        self.submit_button = QPushButton("Submit", self)
        self.submit_button.clicked.connect(self.submit_data)
        self.layout.addWidget(self.submit_button)

        self.result_label = QLabel("", self)
        self.layout.addWidget(self.result_label)

    def submit_data(self):
        data = self.data_input.text()
        self.result_label.setText(f"You entered: {data}")

def main():
    app = QApplication(sys.argv)
    window = UserManagementApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()