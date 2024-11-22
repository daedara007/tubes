import sys
import os
import getpass
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

USER_DATA_FILE = 'users.txt'
token = ""

class DashboardWindow(QWidget):
    def __init__(self,username):
        super().__init__()
        self.setWindowTitle("Task Dashboard")
        self.setGeometry(100, 100, 400, 300)

        self.central_widget = QWidget(self)
        self.central_widget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.title_label = QLabel("Task Dashboard", self)
        self.layout.addWidget(self.title_label)

        self.view_tasks_button = QPushButton("Lihat Tugas", self)
        self.view_tasks_button.clicked.connect(self.open_view_tasks)
        self.layout.addWidget(self.view_tasks_button)

        self.add_task_button = QPushButton("Tambah Tugas", self)
        self.add_task_button.clicked.connect(self.open_add_task)
        self.layout.addWidget(self.add_task_button)

        self.delete_task_button = QPushButton("Hapus Tugas", self)
        self.delete_task_button.clicked.connect(self.open_delete_task)
        self.layout.addWidget(self.delete_task_button)

        self.reminder_button = QPushButton("Reminder", self)
        self.reminder_button.clicked.connect(self.open_reminder)
        self.layout.addWidget(self.reminder_button)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("User  Authentication")
        self.setGeometry(100, 100, 400, 300)
        self.initUI()

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Masukkan username")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Masukkan password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.login_button = QPushButton("Login", self)
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        self.register_button = QPushButton("Register", self)
        self.register_button.clicked.connect(self.register)
        layout.addWidget(self.register_button)

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
            QMessageBox.warning(self, "Error", "Username tidak boleh kosong.")
            return

        users = self.load_users()
        if username in users:
            QMessageBox.warning(self, "Error", "Username sudah ada. Silakan pilih username yang berbeda.")
            return

        if len(password) < 8:
            QMessageBox.warning(self, "Error", "Password minimal 8 karakter.")
            return

        self.save_user(username, password)
        QMessageBox.information(self, "Success", "Pendaftaran berhasil!")

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        users = self.load_users()
        if username in users and users[username] == password:
            global token
            token = username
            QMessageBox.information(self, "Success", "Login berhasil!")
            self.open_dashboard(username)
        else:
            QMessageBox.warning(self, "Error", "Username atau password salah.")

    def open_dashboard(self, username):
        self.dashboard_window = DashboardWindow(username)
        self.dashboard_window.show()
        self.close()  # Close the main window after login

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()