import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QLabel, QLineEdit, QPushButton, QMessageBox, QListWidget, QListWidgetItem, QComboBox)

USER_DATA_FILE = 'users.txt'
TASK_DATA_FILE = 'tasks.txt'
token = ""

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout(self)

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
        self.register_button.clicked.connect(self.open_register)
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

    def open_register(self):
        self.register_window = RegisterWindow()
        self.register_window.show()

    def register(self, username, password):
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
            self.open_dashboard()
        else:
            QMessageBox.warning(self, "Error", "Username atau password salah.")

    def open_dashboard(self):
        self.dashboard = TaskDashboard()
        self.dashboard.show()
        self.close()  # Close the login window


class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Register")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout(self)

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Masukkan username")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Masukkan password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.register_button = QPushButton("Register", self)
        self.register_button.clicked.connect(self.register)
        layout.addWidget(self.register_button)

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        login_window = LoginWindow()
        login_window.register(username, password)
        self.close()  # Close the register window


class TaskDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Task Dashboard")
        self.setGeometry(100, 100, 400, 300)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

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

    def open_view_tasks(self):
        self.view_tasks_window = ViewTasksWindow()
        self.view_tasks_window.show()

    def open_add_task(self):
        self.add_task_window = AddTaskWindow()
        self.add_task_window.show()

    def open_delete_task(self):
        self.delete_task_window = DeleteTaskWindow()
        self.delete_task_window.show()

    def open_reminder(self):
        self.reminder_window = ReminderWindow()
        self.reminder_window.show()


class ViewTasksWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lihat Tugas")
        self.setGeometry(150, 150, 400, 300)

        layout = QVBoxLayout(self)

        self.tasks_list = QListWidget(self)
        layout.addWidget(self.tasks_list)

        self.load_tasks()

        self.setLayout(layout)

    def load_tasks(self):
        if os.path.exists(TASK_DATA_FILE):
            with open(TASK_DATA_FILE, 'r') as file:
                tasks = file.readlines()
                self.tasks_list.clear()
                for task in tasks:
                    task_parts = task.strip().split(',')
                    if len(task_parts) != 4:
                        continue  # Skip malformed lines
                    task_name, subject, deadline, status = task_parts
                    
                    # Create a widget for each task
                    item_widget = QWidget()
                    item_layout = QVBoxLayout(item_widget)

                    # Display task details
                    task_label = QLabel(f"Nama Tugas: {task_name}\nMata Kuliah: {subject}\nDeadline: {deadline}")
                    task_label.setStyleSheet("color: black;")  # Atur warna teks ke hitam
                    item_layout.addWidget(task_label)

                    hello_label = QLabel("Hello World")
                    item_layout.addWidget(hello_label)

                    # Create a dropdown for status
                    status_combo = QComboBox()
                    status_combo.addItems(["Belum Dikerjakan", "Sedang Dikerjakan", "Sudah Selesai"])
                    status_combo.setCurrentText(status)
                    status_combo.currentIndexChanged.connect(lambda index, combo=status_combo, task_name=task_name: self.update_task_status(task_name, combo))
                    item_layout.addWidget(status_combo)

                    item_widget.setLayout(item_layout)

                    # Create a QListWidgetItem and set the widget for it
                    list_item = QListWidgetItem(self.tasks_list)
                    self.tasks_list.addItem(list_item)
                    self.tasks_list.setItemWidget(list_item, item_widget)


    def update_task_status(self, task_name, combo):
        new_status = combo.currentText()
        self.update_task_status_in_file(task_name, new_status)

    def update_task_status_in_file(self, task_name, new_status):
        with open(TASK_DATA_FILE, 'r') as file:
            tasks = file.readlines()

        with open(TASK_DATA_FILE, 'w') as file:
            for task in tasks:
                if task_name in task:
                    task_parts = task.strip().split(',')
                    task_parts[3] = new_status  # Update the status
                    file.write(','.join(task_parts) + '\n')
                else:
                    file.write(task)

        self.load_tasks()  # Reload tasks to reflect changes


class AddTaskWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tambah Tugas")
        self.setGeometry(150, 150, 300, 250)

        layout = QVBoxLayout(self)

        self.task_name_input = QLineEdit(self)
        self.task_name_input.setPlaceholderText("Nama Tugas")
        layout.addWidget(self.task_name_input)

        self.subject_input = QLineEdit(self)
        self.subject_input.setPlaceholderText("Mata Kuliah")
        layout.addWidget(self.subject_input)

        self.deadline_input = QLineEdit(self)
        self.deadline_input.setPlaceholderText("Deadline (YYYY-MM-DD)")
        layout.addWidget(self.deadline_input)

        self.status_input = QComboBox(self)
        self.status_input.addItems(["Belum Dikerjakan", "Sedang Dikerjakan", "Sudah Selesai"])
        layout.addWidget(self.status_input)

        self.add_task_button = QPushButton("Tambah Tugas", self)
        self.add_task_button.clicked.connect(self.add_task)
        layout.addWidget(self.add_task_button)

    def add_task(self):
        task_name = self.task_name_input.text()
        subject = self.subject_input.text()
        deadline = self.deadline_input.text()
        status = self.status_input.currentText()

        if not task_name or not subject or not deadline:
            QMessageBox.warning(self, "Error", "Semua field harus diisi.")
            return

        with open(TASK_DATA_FILE, 'a') as file:
            file.write(f"{task_name},{subject},{deadline},{status}\n")
        
        QMessageBox.information(self, "Success", "Tugas berhasil ditambahkan!")
        self.close()  # Close the add task window


class DeleteTaskWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hapus Tugas")
        self.setGeometry(150, 150, 300, 200)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Ini adalah jendela untuk menghapus tugas."))
        self.setLayout(layout)


class ReminderWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reminder")
        self.setGeometry(150, 150, 300, 200)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Ini adalah jendela untuk pengingat."))
        self.setLayout(layout)


def main():
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()