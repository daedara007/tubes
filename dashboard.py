import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QLabel, QPushButton)

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
        self.setGeometry(150, 150, 300, 200)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Ini adalah jendela untuk melihat tugas."))
        self.setLayout(layout)


class AddTaskWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tambah Tugas")
        self.setGeometry(150, 150, 300, 200)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Ini adalah jendela untuk menambah tugas."))
        self.setLayout(layout)


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
    dashboard = TaskDashboard()
    dashboard.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()